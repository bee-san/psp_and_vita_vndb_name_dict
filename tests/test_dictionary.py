import copy
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from vndb_names.dictionary import build, kana_reading, name_variants, qualifying_games


def release(rid="r1", vn_id="v1", platform="psp", released="2010-01-01", rtype="complete", **extra):
    return {"id": rid, "title": f"Release {rid}", "alttitle": None,
            "released": released, "patch": False, "platforms": [platform],
            "vns": [{"id": vn_id, "title": f"Game {vn_id}", "alttitle": None, "rtype": rtype}], **extra}


def character(cid="c1", original="古河 渚", name="Furukawa Nagisa", vn_id="v1", **extra):
    return {"id": cid, "name": name, "original": original, "aliases": [],
            "vns": [{"id": vn_id, "spoiler": 0, "role": "primary", "release": None}], **extra}


def snapshot(releases=None, characters=None):
    return {"schema_version": 1, "as_of": "2026-10-22",
            "releases": [release()] if releases is None else releases,
            "characters": [character()] if characters is None else characters}


def load_terms(directory, filename="VNDB-Names-PSP-PSVita.zip"):
    with zipfile.ZipFile(Path(directory) / filename) as archive:
        return [row for member in archive.namelist() if member.startswith("term_bank_")
                for row in json.loads(archive.read(member))]


class ScopeTests(unittest.TestCase):
    def test_other_platform_future_unknown_patch_and_trials_are_excluded(self):
        releases = [release(), release("r2", "v2", "win"),
                    release("r3", "v3", released="2026-10-23"),
                    release("r4", "v4", released="TBA"),
                    release("r5", "v5", released="unknown"),
                    release("r6", "v6", patch=True),
                    release("r7", "v7", rtype="trial"),
                    release("r8", "v8", rtype="partial")]
        self.assertEqual(list(qualifying_games(snapshot(releases))), ["v1"])

    def test_partial_dates_only_after_last_possible_day(self):
        releases = [release("r1", "v1", released="2025"),
                    release("r2", "v2", released="2026"),
                    release("r3", "v3", released="2026-09"),
                    release("r4", "v4", released="2026-10"),
                    release("r5", "v5", released="2026-02-30"),
                    release("r6", "v6", released="2026-13")]
        self.assertEqual(list(qualifying_games(snapshot(releases))), ["v1", "v3"])

    def test_bundle_complete_status_checked_per_game(self):
        bundled = release(vns=[{"id": "v1", "title": "Complete", "rtype": "complete"},
                                {"id": "v2", "title": "Trial", "rtype": "trial"}])
        self.assertEqual(list(qualifying_games(snapshot([bundled]))), ["v1"])

    def test_separate_platforms_and_release_evidence(self):
        releases = [release(), release("r2", "v1", "psv"), release("r3", "v2", "psv")]
        chars = [character(), character("c2", "鈴木 花子", "Suzuki Hanako", "v2")]
        with tempfile.TemporaryDirectory() as out:
            summary = build(snapshot(releases, chars), out)
            combined, psp, vita = summary["generated_dictionaries"]
            self.assertEqual((combined["game_count"], psp["game_count"], vita["game_count"]), (2, 1, 2))
            self.assertEqual((combined["character_count"], psp["character_count"], vita["character_count"]), (2, 1, 2))
            manifest = json.loads((Path(out) / "games.json").read_text())
            self.assertEqual(manifest[0]["platforms"], ["psp", "psv"])
            self.assertEqual([r["id"] for r in manifest[0]["releases"]], ["r1", "r2"])
            self.assertFalse(any(row[0] == "花子" for row in load_terms(out, "VNDB-Names-PSP.zip")))

    def test_specific_release_does_not_leak_from_pc(self):
        c = character(vns=[{"id": "v1", "spoiler": 0, "release": {"id": "r999"}}])
        with tempfile.TemporaryDirectory() as out:
            build(snapshot(characters=[c]), out)
            self.assertEqual(load_terms(out), [])

    def test_specific_release_qualifies_only_for_its_own_platform(self):
        c = character(vns=[{"id": "v1", "spoiler": 0, "release": {"id": "r2"}}])
        with tempfile.TemporaryDirectory() as out:
            build(snapshot([release(), release("r2", "v1", "psv")], [c]), out)
            self.assertEqual(load_terms(out, "VNDB-Names-PSP.zip"), [])
            self.assertTrue(load_terms(out, "VNDB-Names-PSVita.zip"))
            self.assertTrue(all("[PS Vita]" in row[5][0] for row in load_terms(out)))

    def test_spoilers_removed_and_generic_association_can_still_qualify(self):
        c = character(vns=[{"id": "v1", "spoiler": 1, "release": None}])
        with tempfile.TemporaryDirectory() as out:
            build(snapshot(characters=[c]), out)
            self.assertEqual(load_terms(out), [])
            c["vns"].append({"id": "v1", "spoiler": 0, "release": None})
            build(snapshot(characters=[c]), out)
            self.assertTrue(load_terms(out))

    def test_out_of_scope_character_associations_not_in_gloss(self):
        c = character(vns=[{"id": "v1", "spoiler": 0, "release": None},
                            {"id": "v999", "spoiler": 0, "release": None}])
        with tempfile.TemporaryDirectory() as out:
            build(snapshot(characters=[c]), out)
            self.assertTrue(all("v999" not in gloss for row in load_terms(out) for gloss in row[5]))


class NameTests(unittest.TestCase):
    def test_full_compact_and_name_parts(self):
        self.assertEqual(name_variants("古河　渚"), ["古河", "古河 渚", "古河渚", "渚"])
        self.assertEqual(name_variants("アリス・エクレール"), ["アリス", "アリスエクレール", "アリス・エクレール", "エクレール"])
        self.assertEqual(name_variants("Alice"), [])

    def test_one_or_two_kana_parts_are_not_searchable(self):
        self.assertEqual(name_variants("ファナ=デ・ラ・ウィーヴェル"),
                         ["ウィーヴェル", "ファナ", "ファナ=デ・ラ・ウィーヴェル", "ファナデラウィーヴェル"])
        self.assertEqual(name_variants("村上 さん"), ["村上", "村上 さん", "村上さん"])
        self.assertEqual(name_variants("氷川 マイ"), ["氷川", "氷川 マイ", "氷川マイ"])
        # A one-kanji part and a whole short kana name stay.
        self.assertIn("渚", name_variants("古河 渚"))
        self.assertEqual(name_variants("ユイ"), ["ユイ"])
        self.assertEqual(name_variants("ﾕｲ"), ["ユイ", "ﾕｲ"])

    def test_source_glyphs_and_halfwidth_kana_survive_normalization(self):
        variants = name_variants("神崎 ｱﾘｽ")
        self.assertIn("神崎 ｱﾘｽ", variants)
        self.assertIn("神崎ｱﾘｽ", variants)
        self.assertIn("神崎 アリス", variants)
        self.assertIn("ｱﾘｽ", variants)
        self.assertEqual(kana_reading("ｱﾘｽ"), "ありす")

    def test_only_kana_readings_are_supplied(self):
        self.assertEqual(kana_reading("アリス・エクレール"), "ありすえくれーる")
        self.assertEqual(kana_reading("なぎさ"), "なぎさ")
        self.assertEqual(kana_reading("古河 渚"), "")

    def test_japanese_aliases_and_japanese_primary_name(self):
        chars = [character(aliases=["だんごちゃん", "Dango"]),
                 character("c2", None, "ことみ")]
        with tempfile.TemporaryDirectory() as out:
            build(snapshot(characters=chars), out)
            expressions = {row[0] for row in load_terms(out)}
            self.assertIn("だんごちゃん", expressions)
            self.assertIn("ことみ", expressions)
            self.assertNotIn("Dango", expressions)

    def test_homonyms_keep_both_identities_without_duplicate_glosses(self):
        chars = [character(), character("c2", "古河 渚", "Different Nagisa"), character()]
        with tempfile.TemporaryDirectory() as out:
            build(snapshot(characters=chars), out)
            terms = load_terms(out)
            row = next(row for row in terms if row[0] == "渚")
            self.assertEqual(len(row[5]), 2)
            self.assertTrue(any("https://vndb.org/c1" in gloss for gloss in row[5]))
            self.assertTrue(any("https://vndb.org/c2" in gloss for gloss in row[5]))
            self.assertEqual(len(terms), len({row[0] for row in terms}))


class FormatTests(unittest.TestCase):
    def test_import_format_banks_tags_and_counts(self):
        with tempfile.TemporaryDirectory() as out:
            with patch("vndb_names.dictionary.BANK_SIZE", 2):
                summary = build(snapshot(), out)
            with zipfile.ZipFile(Path(out) / "VNDB-Names-PSP-PSVita.zip") as archive:
                index = json.loads(archive.read("index.json"))
                tags = json.loads(archive.read("tag_bank_1.json"))
                self.assertEqual(index["format"], 3)
                self.assertTrue(index["sequenced"])
                self.assertEqual(tags[0][0], "name")
                self.assertEqual(len(tags[0]), 5)
                banks = [json.loads(archive.read(p)) for p in archive.namelist() if p.startswith("term_bank_")]
                self.assertEqual(len(banks), 2)
                self.assertTrue(all(len(bank) <= 2 for bank in banks))
            terms = load_terms(out)
            self.assertTrue(all(len(row) == 8 and isinstance(row[5], list) and row[7] == "name" for row in terms))
            self.assertEqual([row[6] for row in terms], [1, 2, 3, 4])
            self.assertEqual(summary["generated_dictionaries"][0]["entry_count"], len(terms))

    def test_output_is_reproducible_and_input_order_independent(self):
        original = snapshot([release(), release("r2", "v2", "psv")],
                            [character(), character("c2", "鈴木 花子", "Suzuki Hanako", "v2")])
        shuffled = copy.deepcopy(original)
        shuffled["releases"].reverse()
        shuffled["characters"].reverse()
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self.assertEqual(build(original, a), build(shuffled, b))
            for path in Path(a).iterdir():
                self.assertEqual(path.read_bytes(), (Path(b) / path.name).read_bytes())

    def test_unsupported_schema_fails(self):
        data = snapshot()
        data["schema_version"] = 2
        with tempfile.TemporaryDirectory() as out:
            with self.assertRaises(ValueError):
                build(data, out)


if __name__ == "__main__":
    unittest.main()
