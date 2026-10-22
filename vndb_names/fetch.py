"""Resumable, rate-limited fetches from VNDB's public Kana API."""
from __future__ import annotations
import hashlib
import http.client
import json
import math
import time
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://api.vndb.org/kana"


def _validate_response(result: object) -> dict:
    if (not isinstance(result, dict)
            or not isinstance(result.get("results"), list)
            or not isinstance(result.get("more"), bool)):
        raise ValueError("Unexpected VNDB response; expected results list and more boolean.")
    return result


def release_filter(as_of: str) -> list:
    date.fromisoformat(as_of)
    return ["and", ["or", ["platform", "=", "psp"], ["platform", "=", "psv"]],
            ["released", "<=", as_of], ["rtype", "=", "complete"], ["patch", "!=", 1]]


class KanaClient:
    def __init__(self, cache_dir: Path, delay: float = 1.6, timeout: float = 120):
        if delay < 1.5:
            raise ValueError("Use at least 1.5 seconds between requests (VNDB rate limit).")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.delay, self.timeout = delay, timeout
        self.last_request = float("-inf")

    def query(self, endpoint: str, payload: dict) -> dict:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        key = hashlib.sha256(endpoint.encode() + b"\n" + encoded).hexdigest()
        path = self.cache_dir / f"{endpoint}-{key}.json"
        if path.exists():
            try:
                return _validate_response(json.loads(path.read_text(encoding="utf-8")))
            except (ValueError, OSError) as exc:
                raise RuntimeError(f"Invalid VNDB response cache: {path}. Remove this file and rerun.") from exc
        for attempt in range(9):
            wait = self.delay - (time.monotonic() - self.last_request)
            if wait > 0:
                time.sleep(wait)
            request = Request(f"{API_URL}/{endpoint}", data=encoded, headers={
                "Content-Type": "application/json",
                "User-Agent": "VNDB-Handheld-Names/1.0 (PSP and PS Vita Yomitan dictionary)",
            })
            try:
                self.last_request = time.monotonic()
                with urlopen(request, timeout=self.timeout) as response:
                    result = json.load(response)
            except HTTPError as exc:
                if exc.code != 429 and not 500 <= exc.code < 600:
                    raise RuntimeError(f"VNDB HTTP {exc.code}: {exc.read().decode(errors='replace')}") from exc
                retry_after = exc.headers.get("Retry-After")
                try:
                    retry = float(retry_after) if retry_after else 0
                except ValueError:
                    try:
                        retry = parsedate_to_datetime(retry_after).timestamp() - time.time()
                    except (TypeError, ValueError, OverflowError):
                        retry = 0
                if not math.isfinite(retry):
                    retry = 0
                wait = max(retry, min(300, 10 * 2 ** attempt))
                if attempt == 8:
                    break
                print(f"VNDB HTTP {exc.code}; retrying in {wait:.0f}s", flush=True)
                time.sleep(wait)
            except (URLError, OSError, http.client.IncompleteRead, json.JSONDecodeError) as exc:
                wait = min(120, 5 * 2 ** attempt)
                if attempt == 8:
                    break
                print(f"VNDB connection problem: {exc}; retrying in {wait}s", flush=True)
                time.sleep(wait)
            else:
                _validate_response(result)
                temporary = path.with_suffix(".tmp")
                temporary.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
                temporary.replace(path)
                return result
        raise RuntimeError("VNDB retries exhausted. Rerun to resume from the response cache.")

    def all(self, endpoint: str, filters: list, fields: str) -> list[dict]:
        # Keyset pagination avoids VNDB's maximum page depth and handles ID gaps.
        rows, cursor = [], None
        while True:
            current = filters if cursor is None else ["and", filters, ["id", ">", cursor]]
            response = self.query(endpoint, {"filters": current, "fields": fields,
                                             "sort": "id", "results": 100})
            page = response["results"]
            if not page:
                if response["more"]:
                    raise RuntimeError("VNDB returned an empty page with more=true")
                return rows
            new_cursor = page[-1]["id"]
            if cursor is not None and int(new_cursor[1:]) <= int(cursor[1:]):
                raise RuntimeError("VNDB cursor did not advance")
            rows.extend(page)
            print(f"{endpoint}: {len(rows)} records (through {new_cursor})", flush=True)
            if not response["more"]:
                return rows
            cursor = new_cursor


def fetch_snapshot(as_of: str, output: Path, cache_dir: Path, delay: float = 1.6) -> dict:
    scope = release_filter(as_of)
    client = KanaClient(cache_dir, delay=delay)
    releases = client.all("release", scope,
                          "title,alttitle,released,patch,platforms,vns{id,title,alttitle,rtype}")
    # Platform availability is a cheaper superset of the qualifying releases.
    # The builder applies the exact release/VN scope locally, including dates,
    # release completeness, patches, and release-specific character appearances.
    character_scope = ["vn", "=", ["or", ["platform", "=", "psp"], ["platform", "=", "psv"]]]
    characters = client.all("character", character_scope,
                            "name,original,aliases,vns{id,spoiler,role,release.id}")
    snapshot = {"schema_version": 1, "as_of": as_of,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "api": API_URL, "release_filter": scope, "character_filter": character_scope,
                "releases": releases, "characters": characters}
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp")
    temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)
    return snapshot
