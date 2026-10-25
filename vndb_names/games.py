"""Per-game name dictionaries, keyed by the title ID a PSP or PS Vita reports.

A console reports a Vita game's title ID (PCSG00415) and a PSP disc's ID (ULJM05338). This module
finds those IDs for the qualifying games, then builds one name list per set of games an ID names
(a bundle names several), so an app can show the running game's characters first.

Where the IDs come from (data/title-ids.json, written by `fetch-ids`):
  - VNDB release catalog numbers: a PSP UMD's product code is its disc ID; a Vita digital release's
    is its title ID. A Vita card's code (VLJM-35xxx) is not, so most Vita retail games have none;
  - VNDB's PlayStation Store links, whose content IDs hold a title ID;
  - Vita3K's compatibility list, whose issues name a Vita title ID with its game: an ID is taken
    when the name matches exactly one qualifying Vita game's VNDB titles, and never against an ID
    VNDB gives another game.
Games with no ID get no per-game list; they keep the combined dictionary only.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

VITA_ID = re.compile(r"PCS[A-H]\d{5}\Z")
PSP_ID = re.compile(r"(?:U[LC][A-Z]{2}|NP[UEJHAK][HGZ])\d{5}\Z")
_TITLE_ID_IN_TEXT = re.compile(r"\b(PCS[A-H]\d{5})\b")
_CONTENT_ID = re.compile(r"[A-Z]{2}\d{4}-([A-Z]{4}\d{5})_\d{2}-")
_ROMAN = {chr(base + i): r for base in (0x2160, 0x2170)
          for i, r in enumerate("i ii iii iv v vi vii viii ix x xi xii".split())}
_HALFWIDTH_KANA = re.compile(r"[｡-ﾟ]+")
# Edition words a release title adds and a console title leaves out (normalized; stripped from the
# end, repeatedly): VNDB's "... Download Edition", "... パッケージ版".
_EDITIONS = ("firstpresslimitededition", "downloadedition", "packageedition", "limitededition",
             "regularedition", "specialedition", "deluxeedition", "standardedition", "premiumedition",
             "valueedition", "firstpressedition", "normaledition", "dledition", "ダウンロード版", "パッケージ版",
             "初回限定版", "完全生産限定版", "限定版", "通常版", "特装版", "豪華版", "廉価版", "dl版", "ベスト版",
             "playstationvitathebest", "psvitathebest", "pspthebest", "thebest", "bestprice",
             "forplaystationvita", "forpsvita", "forpsp")
_AQUA_PRICE = re.compile(r"aquaprice\d+\Z")
_ROLES = {"main": 0, "primary": 1, "side": 2, "appears": 3}


def title_key(text: str) -> str:
    """A title compared by letters only: case, width, diacritics, punctuation and edition words go."""
    text = _HALFWIDTH_KANA.sub(lambda m: unicodedata.normalize("NFKC", m.group()), text or "")
    out = []
    for ch in text:
        c = ord(ch)
        if 0xFF01 <= c <= 0xFF5E:
            ch, c = chr(c - 0xFEE0), c - 0xFEE0
        if ch in _ROMAN:
            out.append(_ROMAN[ch])
        elif ch.isascii() and ch.isalnum():
            out.append(ch.lower())
        elif 0xC0 <= c <= 0x24F and c not in (0xD7, 0xF7):
            base = unicodedata.normalize("NFD", ch)[0]
            out.append(base.lower() if base.isascii() else ch.lower())
        elif (0x3041 <= c <= 0x3096 or 0x30A1 <= c <= 0x30FA or c in (0x3005, 0x3006, 0x309D, 0x309E, 0x30FC,
              0x30FD, 0x30FE) or 0x3400 <= c <= 0x4DBF or 0x4E00 <= c <= 0x9FFF or 0xF900 <= c <= 0xFAFF
              or c >= 0x20000):
            out.append(ch)
    key = "".join(out)
    changed = True
    while changed:
        changed = False
        match = _AQUA_PRICE.search(key)
        if match and match.start() > 2:
            key, changed = key[:match.start()], True
        for word in _EDITIONS:
            if key.endswith(word) and len(key) > len(word) + 2:
                key, changed = key[:-len(word)], True
    return key


def catalog_ids(catalog: str | None) -> set[str]:
    """Title and disc IDs in a VNDB catalog field ("ULJM-05350 / ULJM-05351")."""
    found = set()
    for part in re.split(r"[/,;、]|\s{2,}", (catalog or "").upper()):
        compact = re.sub(r"[\s\-_]", "", part)
        if VITA_ID.match(compact) or PSP_ID.match(compact):
            found.add(compact)
    return found


def _github_issues(repo: str) -> list[dict]:
    token = os.environ.get("GITHUB_TOKEN", "")
    rows, page = [], 1
    while True:
        request = Request(f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}",
                          headers={"Accept": "application/vnd.github+json",
                                   "User-Agent": "VNDB-Handheld-Names/1.0",
                                   **({"Authorization": f"Bearer {token}"} if token else {})})
        with urlopen(request, timeout=60) as response:
            batch = json.load(response)
        if not batch:
            return rows
        rows.extend(issue for issue in batch if "pull_request" not in issue)
        page += 1


def vita3k_entries(issues: list[dict]) -> list[dict]:
    """Vita3K compatibility issues as (title ID, name): one ID in the issue title."""
    entries = []
    for issue in issues:
        title = issue.get("title") or ""
        ids = _TITLE_ID_IN_TEXT.findall(title)
        if len(ids) != 1:
            continue
        name = re.sub(r"^[\s\[\]()\-–—|:]+|[\s\[\]()\-–—|:]+$", "", _TITLE_ID_IN_TEXT.sub("", title))
        if name:
            entries.append({"id": ids[0], "name": name, "issue": issue["number"]})
    return sorted(entries, key=lambda e: (e["id"], e["issue"]))


def fetch_title_ids(output: Path, cache_dir: Path, delay: float = 1.6) -> dict:
    from .fetch import KanaClient
    client = KanaClient(cache_dir, delay=delay)
    scope = ["or", ["platform", "=", "psp"], ["platform", "=", "psv"]]
    releases = client.all("release", scope, "title,alttitle,platforms,catalog,languages{title,latin},"
                                            "extlinks{name,id},vns{id}")
    vns = client.all("vn", scope, "title,alttitle,titles{title,latin},aliases")
    rows = []
    for r in releases:
        ids = catalog_ids(r.get("catalog"))
        for link in r.get("extlinks") or []:
            match = _CONTENT_ID.match(str(link.get("id", "")))
            if str(link.get("name", "")).startswith("playstation") and match:
                ids.add(match.group(1))
        titles = {r.get("title"), r.get("alttitle")}
        for lang in r.get("languages") or []:
            titles.update((lang.get("title"), lang.get("latin")))
        rows.append({"id": r["id"], "platforms": sorted(r.get("platforms", [])), "vns": [v["id"] for v in r["vns"]],
                     "ids": sorted(ids), "titles": sorted(t for t in titles if t)})
    vn_titles = {}
    for v in vns:
        titles = {v.get("title"), v.get("alttitle"), *(v.get("aliases") or [])}
        for t in v.get("titles") or []:
            titles.update((t.get("title"), t.get("latin")))
        vn_titles[v["id"]] = sorted(t for t in titles if t)
    data = {"schema_version": 1, "fetched_at": datetime.now(timezone.utc).isoformat(),
            "sources": ["https://api.vndb.org/kana", "https://github.com/Vita3K/compatibility/issues"],
            "releases": sorted(rows, key=lambda r: int(r["id"][1:])),
            "vn_titles": dict(sorted(vn_titles.items(), key=lambda kv: int(kv[0][1:]))),
            "vita3k": vita3k_entries(_github_issues("Vita3K/compatibility"))}
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    temporary.replace(output)
    return data


def title_id_games(games: dict[str, dict[str, Any]], title_ids: dict) -> dict[str, list[str]]:
    """Each title ID a console may report, and the qualifying games it names (sorted VN IDs)."""
    qualifying_releases = {r["id"] for g in games.values() for r in g["releases"]}
    named: dict[str, set[str]] = defaultdict(set)
    for r in title_ids["releases"]:
        if r["id"] not in qualifying_releases:
            continue
        vns = [v for v in r["vns"] if v in games]
        for tid in r["ids"]:
            platform = "psv" if VITA_ID.match(tid) else "psp"
            if platform in r["platforms"]:
                named[tid].update(v for v in vns if platform in games[v]["platforms"])
    vndb_ids = {tid for tid, vns in named.items() if vns}
    # Vita3K: a name matching exactly one qualifying Vita game's titles, for an ID VNDB has not given.
    keys: dict[str, set[str]] = defaultdict(set)
    for r in title_ids["releases"]:
        if r["id"] in qualifying_releases and "psv" in r["platforms"]:
            for v in r["vns"]:
                if v in games and "psv" in games[v]["platforms"]:
                    for t in r["titles"]:
                        keys[title_key(t)].add(v)
    for v, game in games.items():
        if "psv" in game["platforms"]:
            for t in title_ids["vn_titles"].get(v, []):
                keys[title_key(t)].add(v)
    keys.pop("", None)
    for entry in title_ids["vita3k"]:
        if entry["id"] in vndb_ids:
            continue
        found = keys.get(title_key(entry["name"]), set())
        if len(found) == 1:
            named[entry["id"]].update(found)
    return {tid: sorted(vns, key=lambda v: int(v[1:])) for tid, vns in sorted(named.items()) if vns}


def game_terms(characters: list[dict[str, Any]], games: dict[str, dict[str, Any]],
               vn_ids: list[str]) -> list[list[Any]]:
    """One game set's names, as Yomitan term rows. Within an entry, a character whose own name has
    the spelling comes before one known by it as an alias, then by role (main, primary, side,
    appears), so 岡崎 is Okazaki Tomoya before Nagisa's married name."""
    from .dictionary import PLATFORMS, _character_games, _id_key, kana_reading, name_variants
    subset = {v: games[v] for v in vn_ids}
    ranked: dict[str, dict[str, tuple]] = defaultdict(dict)
    for character in sorted(characters, key=lambda c: _id_key(c["id"])):
        appearances = _character_games(character, subset, {"psp", "psv"})
        if not appearances:
            continue
        own = {v for name in (character.get("original") or "", character.get("name") or "")
               for v in name_variants(name)}
        aliases = {v for name in character.get("aliases", []) for v in name_variants(name)} - own
        if not own and not aliases:
            continue
        role = min((_ROLES.get(a.get("role"), 4) for a in character.get("vns", [])
                    if a["id"] in appearances and not a.get("spoiler")), default=4)
        full_name = character.get("name") or character.get("original") or character["id"]
        if character.get("original") and character["original"] != full_name:
            full_name += f" ({character['original']})"
        lines = []
        for vn_id, available in sorted(appearances.items(), key=lambda pair: _id_key(pair[0])):
            game = subset[vn_id]
            title = game["title"] + (f" / {game['alttitle']}" if game.get("alttitle") and
                                     game["alttitle"] != game["title"] else "")
            lines.append(f"{title} [{', '.join(PLATFORMS[p] for p in sorted(available))}]")
        definition = "\n".join([full_name, *lines, f"https://vndb.org/{character['id']}"])
        for expression, alias in [(e, 0) for e in own] + [(e, 1) for e in aliases]:
            order = (alias, role, _id_key(character["id"]))
            if definition not in ranked[expression] or order < ranked[expression][definition]:
                ranked[expression][definition] = order
    return [[expression, kana_reading(expression), "", "", 0,
             [d for d, _ in sorted(ranked[expression].items(), key=lambda kv: kv[1])], sequence, "name"]
            for sequence, expression in enumerate(sorted(ranked), 1)]


def build_games(snapshot: dict[str, Any], games: dict[str, dict[str, Any]], title_ids: dict,
                path: Path, index: dict[str, Any]) -> dict[str, Any]:
    """VNDB-Names-Games.zip: index.json and games.json, one entry per game set with its title IDs,
    its title and its term rows (the rows of a Yomitan term bank)."""
    import zipfile
    from .dictionary import _json_bytes
    by_set: dict[tuple, list[str]] = defaultdict(list)
    for tid, vns in title_id_games(games, title_ids).items():
        by_set[tuple(vns)].append(tid)
    entries = []
    for vns, tids in sorted(by_set.items(), key=lambda kv: (int(kv[0][0][1:]), kv[0])):
        terms = game_terms(snapshot["characters"], games, list(vns))
        if not terms:
            continue
        entries.append({"vns": list(vns), "title": " / ".join(games[v]["title"] for v in vns),
                        "title_ids": sorted(tids), "terms": terms})
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, value in (("index.json", index), ("games.json", entries)):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, _json_bytes(value), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return {"game_sets": len(entries), "title_ids": sum(len(e["title_ids"]) for e in entries),
            "vita_title_ids": sum(1 for e in entries for t in e["title_ids"] if VITA_ID.match(t)),
            "psp_disc_ids": sum(1 for e in entries for t in e["title_ids"] if PSP_ID.match(t)),
            "games_with_an_id": len({v for e in entries for v in e["vns"]})}
