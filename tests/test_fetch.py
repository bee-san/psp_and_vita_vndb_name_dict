import http.client
import io
import json
import tempfile
import unittest
from datetime import datetime, timezone
from email.message import Message
from email.utils import format_datetime
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from vndb_names.fetch import KanaClient, fetch_snapshot, release_filter


def response(value):
    return io.BytesIO(json.dumps(value).encode("utf-8"))


def http_error(code, retry_after=None):
    headers = Message()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return HTTPError("https://api.vndb.org/kana/vn", code, "test", headers,
                     io.BytesIO(b'{"message":"test API error"}'))


class FetchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.client = KanaClient(self.root / "cache")
        # Advance the clock between calls without making real network requests or waits.
        self.clock = patch("vndb_names.fetch.time.monotonic", side_effect=range(0, 10000, 10))
        self.clock.start()
        self.addCleanup(self.clock.stop)
        sleep_patch = patch("vndb_names.fetch.time.sleep")
        self.sleep = sleep_patch.start()
        self.addCleanup(sleep_patch.stop)

    def test_release_scope_correlates_platform_date_and_complete_nonpatch_release(self):
        self.assertEqual(release_filter("2026-10-22"), [
            "and", ["or", ["platform", "=", "psp"], ["platform", "=", "psv"]],
            ["released", "<=", "2026-10-22"], ["rtype", "=", "complete"],
            ["patch", "!=", 1],
        ])
        with self.assertRaises(ValueError):
            release_filter("2026-02-30")
        with self.assertRaises(ValueError):
            KanaClient(self.root / "too-fast", delay=1)

    def test_keyset_pagination_handles_id_gaps_and_numeric_order(self):
        scope = ["platform", "=", "psp"]
        pages = [
            {"results": [{"id": "c2"}, {"id": "c9"}], "more": True},
            {"results": [{"id": "c14"}], "more": False},
        ]
        with patch.object(self.client, "query", side_effect=pages) as query:
            rows = self.client.all("character", scope, "name")
        self.assertEqual([row["id"] for row in rows], ["c2", "c9", "c14"])
        self.assertEqual(query.call_args_list[1].args[1], {
            "filters": ["and", scope, ["id", ">", "c9"]],
            "fields": "name", "sort": "id", "results": 100,
        })

    def test_pagination_rejects_nonadvancing_and_empty_continuation(self):
        for second_page, error in [
            ({"results": [{"id": "c9"}], "more": True}, "did not advance"),
            ({"results": [], "more": True}, "empty page"),
        ]:
            with self.subTest(second_page=second_page):
                with patch.object(self.client, "query", side_effect=[
                    {"results": [{"id": "c9"}], "more": True}, second_page,
                ]):
                    with self.assertRaisesRegex(RuntimeError, error):
                        self.client.all("character", [], "name")

    def test_cache_resumes_without_network_and_uses_canonical_query(self):
        expected = {"results": [{"id": "v17"}], "more": False}
        with patch("vndb_names.fetch.urlopen", return_value=response(expected)) as network:
            self.assertEqual(self.client.query("vn", {"fields": "title", "results": 100}), expected)
            self.assertEqual(self.client.query("vn", {"results": 100, "fields": "title"}), expected)
        self.assertEqual(network.call_count, 1)
        self.assertEqual(len(list((self.root / "cache").glob("*.json"))), 1)
        self.assertFalse(list((self.root / "cache").glob("*.tmp")))

    def test_invalid_success_response_is_not_cached(self):
        for bad in [[], {"results": [], "more": "false"}, {"results": {}, "more": False}]:
            with self.subTest(bad=bad):
                with patch("vndb_names.fetch.urlopen", return_value=response(bad)) as network:
                    with self.assertRaisesRegex(ValueError, "Unexpected VNDB response"):
                        self.client.query("vn", {})
                self.assertEqual(network.call_count, 1)
                self.assertFalse(list((self.root / "cache").glob("*.json")))

    def test_successive_network_queries_respect_minimum_interval(self):
        with patch("vndb_names.fetch.time.monotonic", side_effect=[0, 0, 1, 1]), patch(
            "vndb_names.fetch.urlopen", side_effect=[
                response({"results": [], "more": False}),
                response({"results": [], "more": False}),
            ],
        ):
            self.client.query("vn", {"fields": "title"})
            self.client.query("vn", {"fields": "alttitle"})
        self.sleep.assert_called_once()
        self.assertAlmostEqual(self.sleep.call_args.args[0], 0.6)

    def test_corrupt_cache_fails_with_recovery_path_without_refetching(self):
        with patch("vndb_names.fetch.urlopen", return_value=response({"results": [], "more": False})):
            self.client.query("vn", {})
        cache = next((self.root / "cache").glob("*.json"))
        for bad in ['{"results":', '[1,2]', '{"results":[],"more":null}']:
            with self.subTest(bad=bad):
                cache.write_text(bad, encoding="utf-8")
                with patch("vndb_names.fetch.urlopen") as network:
                    with self.assertRaisesRegex(RuntimeError, "Invalid VNDB response cache.*Remove this file"):
                        self.client.query("vn", {})
                network.assert_not_called()

    def test_rate_limit_honors_numeric_and_http_date_retry_after(self):
        for retry_after in ["37", format_datetime(datetime.fromtimestamp(1037, timezone.utc), usegmt=True)]:
            with self.subTest(retry_after=retry_after):
                cache_dir = self.root / ("numeric" if retry_after == "37" else "http-date")
                client = KanaClient(cache_dir)
                self.sleep.reset_mock()
                with patch("vndb_names.fetch.time.time", return_value=1000), patch(
                    "vndb_names.fetch.urlopen", side_effect=[
                        http_error(429, retry_after), response({"results": [], "more": False}),
                    ],
                ) as network:
                    client.query("vn", {})
                self.assertEqual(network.call_count, 2)
                self.sleep.assert_called_once_with(37)

    def test_invalid_retry_after_uses_backoff(self):
        for invalid in ["not a date", "NaN", "Infinity"]:
            with self.subTest(invalid=invalid):
                client = KanaClient(self.root / invalid.replace(" ", "-"))
                self.sleep.reset_mock()
                with patch("vndb_names.fetch.urlopen", side_effect=[
                    http_error(429, invalid), response({"results": [], "more": False}),
                ]):
                    client.query("vn", {})
                self.sleep.assert_called_once_with(10)

    def test_temporary_server_and_response_failures_retry(self):
        failures = [http_error(503), URLError("offline"), TimeoutError("slow"),
                    OSError("connection reset"), http.client.IncompleteRead(b"partial", 8),
                    io.BytesIO(b'{"results":')]
        for number, failure in enumerate(failures):
            with self.subTest(failure=failure):
                client = KanaClient(self.root / f"retry-{number}")
                with patch("vndb_names.fetch.urlopen", side_effect=[
                    failure, response({"results": [], "more": False}),
                ]) as network:
                    self.assertEqual(client.query("vn", {}), {"results": [], "more": False})
                self.assertEqual(network.call_count, 2)

    def test_permanent_error_is_reported_without_retry(self):
        with patch("vndb_names.fetch.urlopen", side_effect=http_error(400)) as network:
            with self.assertRaisesRegex(RuntimeError, "VNDB HTTP 400.*test API error"):
                self.client.query("vn", {})
        self.assertEqual(network.call_count, 1)
        self.sleep.assert_not_called()

    def test_retries_are_bounded_and_failed_queries_are_not_cached(self):
        with patch("vndb_names.fetch.urlopen", side_effect=URLError("offline")) as network:
            with self.assertRaisesRegex(RuntimeError, "retries exhausted"):
                self.client.query("vn", {})
        self.assertEqual(network.call_count, 9)
        self.assertEqual(self.sleep.call_count, 8)
        self.assertFalse(list((self.root / "cache").glob("*.json")))

    def test_snapshot_records_exact_release_scope_and_broader_character_candidates(self):
        releases = [{"id": "r1", "vns": [{"id": "v17", "rtype": "complete"}]}]
        characters = [{"id": "c1", "name": "Test"}]
        output = self.root / "data" / "snapshot.json"
        with patch("vndb_names.fetch.KanaClient") as client_class:
            client_class.return_value.all.side_effect = [releases, characters]
            snapshot = fetch_snapshot("2026-10-22", output, self.root / "cache")
            character_call = client_class.return_value.all.call_args_list[1]
        # Broad platform candidates avoid an expensive nested release query.
        # They remain a superset; the builder enforces exact eligibility locally.
        candidate_scope = ["vn", "=", ["or", ["platform", "=", "psp"], ["platform", "=", "psv"]]]
        self.assertEqual(character_call.args[1], candidate_scope)
        self.assertEqual(snapshot["character_filter"], candidate_scope)
        self.assertEqual(snapshot["release_filter"], release_filter("2026-10-22"))
        self.assertEqual(snapshot["characters"], characters)
        self.assertEqual(snapshot["releases"], releases)
        self.assertEqual(json.loads(output.read_text(encoding="utf-8")), snapshot)
        self.assertFalse(output.with_suffix(".tmp").exists())


if __name__ == "__main__":
    unittest.main()
