import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from vndb_names.dictionary import build, qualifying_games
from vndb_names.games import catalog_ids, game_terms, title_id_games, title_key, vita3k_entries

from test_dictionary import character, release, snapshot


def ids_data(releases=(), vn_titles=None, vita3k=()):
    return {"schema_version": 1, "releases": list(releases), "vn_titles": vn_titles or {}, "vita3k": list(vita3k)}


def id_row(rid, vns, platforms, ids=(), titles=()):
    return {"id": rid, "vns": list(vns), "platforms": list(platforms), "ids": list(ids), "titles": list(titles)}


class TitleKeyTests(unittest.TestCase):
    def test_width_case_punctuation_and_edition_words(self):
        self.assertEqual(title_key("ＣＬＡＮＮＡＤ"), "clannad")
        self.assertEqual(title_key("シュタインズ・ゲート　ゼロ"), "シュタインズゲートゼロ")
        self.assertEqual(title_key("ｼｭﾀｲﾝｽﾞ･ｹﾞｰﾄ"), "シュタインズゲート")
        self.assertEqual(title_key("Fate/stay night [Réalta Nua]"), "fatestaynightrealtanua")
        self.assertEqual(title_key("D.C.Ⅱ P.S."), "dciips")
        self.assertEqual(title_key("AMNESIA V Edition Download Edition"), "amnesiavedition")
        self.assertEqual(title_key("NORN9 LAST ERA DL版"), "norn9lastera")
        self.assertEqual(title_key("White Album 2 Aqua Price 2800"), "whitealbum2")

    def test_catalog_numbers(self):
        self.assertEqual(catalog_ids("ULJM-05350 / ULJM-05351"), {"ULJM05350", "ULJM05351"})
        self.assertEqual(catalog_ids("PCSG-00415"), {"PCSG00415"})
        self.assertEqual(catalog_ids("VLJM-35123"), set())  # a Vita card's box code is no title ID
        self.assertEqual(catalog_ids(None), set())

    def test_vita3k_issue_titles(self):
        issues = [{"number": 2, "title": "CLANNAD [PCSG00415]"}, {"number": 3, "title": "PCSE00120 - Persona 4"},
                  {"number": 4, "title": "Two IDs PCSG00001 PCSG00002"}, {"number": 5, "title": "No ID"}]
        self.assertEqual(vita3k_entries(issues), [{"id": "PCSE00120", "name": "Persona 4", "issue": 3},
                                                  {"id": "PCSG00415", "name": "CLANNAD", "issue": 2}])


class TitleIdTests(unittest.TestCase):
    def games(self):
        return qualifying_games(snapshot([release("r1", "v1", "psp"), release("r2", "v2", "psv"),
                                          release("r3", "v3", "psv"), release("r4", "v4", "psv")]))

    def test_catalog_ids_on_their_platform_only(self):
        data = ids_data([id_row("r1", ["v1"], ["psp"], ["ULJM05338", "PCSG00001"]),
                         id_row("r2", ["v2"], ["psv"], ["PCSG00002"])])
        self.assertEqual(title_id_games(self.games(), data), {"PCSG00002": ["v2"], "ULJM05338": ["v1"]})

    def test_a_bundle_names_each_of_its_games(self):
        data = ids_data([id_row("r2", ["v2", "v3", "v9"], ["psv"], ["PCSG00009"])])
        # v9 has no qualifying release; v3 has its own (r3)
        self.assertEqual(title_id_games(self.games(), data), {"PCSG00009": ["v2", "v3"]})
        bundle = qualifying_games(snapshot([release("r2", "v2", "psv",
                                                    vns=[{"id": "v2", "title": "A", "rtype": "complete"},
                                                         {"id": "v3", "title": "B", "rtype": "complete"}])]))
        self.assertEqual(title_id_games(bundle, data), {"PCSG00009": ["v2", "v3"]})

    def test_vita3k_names_one_game_or_none(self):
        data = ids_data([id_row("r2", ["v2"], ["psv"], titles=["Clannad"]),
                         id_row("r3", ["v3"], ["psv"], ["PCSG00003"], titles=["Shared"]),
                         id_row("r4", ["v4"], ["psv"], titles=["Shared"])],
                        vita3k=[{"id": "PCSG00415", "name": "CLANNAD", "issue": 1},
                                {"id": "PCSG00005", "name": "Shared", "issue": 2},
                                {"id": "PCSG00003", "name": "Clannad", "issue": 3},
                                {"id": "PCSG00006", "name": "Unknown", "issue": 4}])
        # Shared names two games; PCSG00003 is VNDB's for v3, whatever Vita3K calls it.
        self.assertEqual(title_id_games(self.games(), data), {"PCSG00003": ["v3"], "PCSG00415": ["v2"]})

    def test_vn_titles_count_and_psp_games_never_take_vita_ids(self):
        data = ids_data(vn_titles={"v1": ["Portable"], "v2": ["Kanon"]},
                        vita3k=[{"id": "PCSG00007", "name": "Portable", "issue": 1},
                                {"id": "PCSG00008", "name": "KANON", "issue": 2}])
        self.assertEqual(title_id_games(self.games(), data), {"PCSG00008": ["v2"]})


class GameTermTests(unittest.TestCase):
    def test_own_name_before_alias_then_role(self):
        chars = [character("c1", "古河 渚", "Furukawa Nagisa", aliases=["岡崎 渚"]),
                 character("c2", "岡崎 直幸", "Okazaki Naoyuki",
                           vns=[{"id": "v1", "spoiler": 0, "role": "side", "release": None}]),
                 character("c3", "岡崎 朋也", "Okazaki Tomoya",
                           vns=[{"id": "v1", "spoiler": 0, "role": "main", "release": None}]),
                 character("c4", "渚", "Other Nagisa", vn_id="v2")]
        games = qualifying_games(snapshot([release("r1", "v1"), release("r2", "v2")]))
        terms = {t[0]: t[5] for t in game_terms(chars, games, ["v1"])}
        self.assertEqual([d.split("\n")[0] for d in terms["岡崎"]],
                         ["Okazaki Tomoya (岡崎 朋也)", "Okazaki Naoyuki (岡崎 直幸)", "Furukawa Nagisa (古河 渚)"])
        self.assertEqual([d.split("\n")[0] for d in terms["渚"]], ["Furukawa Nagisa (古河 渚)"])
        self.assertEqual(terms["渚"][0].split("\n")[1:], ["Game v1 [PSP]", "https://vndb.org/c1"])

    def test_spoilers_stay_out(self):
        chars = [character("c1", vns=[{"id": "v1", "spoiler": 1, "role": "main", "release": None}])]
        games = qualifying_games(snapshot())
        self.assertEqual(game_terms(chars, games, ["v1"]), [])


class BuildTests(unittest.TestCase):
    def test_per_game_zip_and_unchanged_combined_dictionaries(self):
        snap = snapshot([release("r1", "v1", "psv"), release("r2", "v2", "psp")],
                        [character("c1", vn_id="v1"), character("c2", "春原 陽平", "Sunohara Youhei", vn_id="v2"),
                         character("c3", "藤林 杏", "Fujibayashi Kyou", vn_id="v1")])
        data = ids_data([id_row("r1", ["v1"], ["psv"], ["PCSG00415"]), id_row("r2", ["v2"], ["psp"], ["ULJM05338"])])
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            plain = build(snap, a)
            with_ids = build(snap, b, data)
            self.assertEqual(plain["generated_dictionaries"], with_ids["generated_dictionaries"])
            self.assertNotIn("per_game", plain)
            self.assertEqual(with_ids["per_game"]["game_sets"], 2)
            with zipfile.ZipFile(Path(b) / "VNDB-Names-Games.zip") as archive:
                entries = json.loads(archive.read("games.json"))
                self.assertIn("attribution", json.loads(archive.read("index.json")))
        self.assertEqual([(e["vns"], e["title_ids"]) for e in entries], [(["v1"], ["PCSG00415"]), (["v2"], ["ULJM05338"])])
        self.assertEqual(sorted(t[0] for t in entries[0]["terms"]), ["古河", "古河 渚", "古河渚", "杏", "渚", "藤林", "藤林 杏", "藤林杏"])


if __name__ == "__main__":
    unittest.main()
