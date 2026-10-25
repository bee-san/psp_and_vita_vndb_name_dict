"""Build compact, reproducible Yomitan name dictionaries from a VNDB snapshot.

Only non-spoiler character associations to eligible releases are included. Names
come from VNDB, not a language model; kanji readings are deliberately left blank.
"""
from __future__ import annotations

import calendar
import hashlib
import json
import re
import unicodedata
import zipfile
from datetime import date
from pathlib import Path
from typing import Any

PLATFORMS = {"psp": "PSP", "psv": "PS Vita"}
BANK_SIZE = 10_000
_JAPANESE = re.compile(r"[\u3041-\u3096\u30a1-\u30fa\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0003134f]")
_SEPARATORS = re.compile(r"[\s=＝・]+")
_KANA = re.compile(r"[\u3041-\u3096\u309d\u309e\u30a1-\u30f6\u30fd\u30feー]+\Z")


def _id_key(value: str) -> tuple[str, int]:
    match = re.fullmatch(r"([a-z]+)([0-9]+)", value)
    return (match[1], int(match[2])) if match else (value, 0)


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


def _known_past_date(value: str, as_of: date) -> bool:
    """A partial date is eligible only after its last possible day has passed."""
    try:
        if re.fullmatch(r"\d{4}", value):
            last = date(int(value), 12, 31)
        elif re.fullmatch(r"\d{4}-\d{2}", value):
            year, month = map(int, value.split("-"))
            last = date(year, month, calendar.monthrange(year, month)[1])
        elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            last = date.fromisoformat(value)
        else:
            return False
        return last <= as_of
    except (ValueError, TypeError):
        return False


def qualifying_games(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return games with complete, dated, non-patch PSP/Vita release evidence."""
    as_of = date.fromisoformat(snapshot["as_of"])
    games: dict[str, dict[str, Any]] = {}
    for release in sorted(snapshot["releases"], key=lambda r: _id_key(r["id"])):
        platforms = sorted(set(release.get("platforms", [])) & PLATFORMS.keys())
        if (not platforms or release.get("patch", False)
                or not _known_past_date(release.get("released", ""), as_of)):
            continue
        for vn in release.get("vns", []):
            if vn.get("rtype") != "complete":
                continue
            game = games.setdefault(vn["id"], {
                "id": vn["id"], "title": vn["title"],
                "alttitle": vn.get("alttitle"), "platforms": [], "releases": [],
            })
            game["platforms"] = sorted(set(game["platforms"]) | set(platforms))
            evidence = {
                "id": release["id"], "title": release["title"],
                "released": release["released"], "platforms": platforms,
                "url": "https://vndb.org/" + release["id"],
            }
            if evidence not in game["releases"]:
                game["releases"].append(evidence)
    return dict(sorted(games.items(), key=lambda pair: _id_key(pair[0])))


def _searchable_part(part: str) -> bool:
    """A name part of one or two kana is no name to look up: such parts are the
    particles of foreign names (デ and ラ in ファナ=デ・ラ・…, リ in コーネリア・リ・…)
    and honorifics (さん in 村上 さん), and they match ordinary words (で, だ, する)."""
    compact = unicodedata.normalize("NFKC", part)
    return len(compact) > 2 or not _KANA.fullmatch(compact)


def name_variants(name: str) -> list[str]:
    """Keep the source name, its separator-free form, and Japanese name parts."""
    source = " ".join(name.split())
    normalized = unicodedata.normalize("NFKC", source)
    if not _JAPANESE.search(normalized):
        return []
    # Preserve literal source spellings, including compatibility ideographs and
    # halfwidth kana, so exact text from an older game remains searchable.
    variants = set()
    for spelling in (source, normalized):
        variants.update((spelling, _SEPARATORS.sub("", spelling)))
        variants.update(filter(_searchable_part, _SEPARATORS.split(spelling)))
    return sorted(v for v in variants if v and _JAPANESE.search(unicodedata.normalize("NFKC", v)))


def kana_reading(expression: str) -> str:
    """Return a hiragana reading for kana-only expressions; never guess kanji."""
    compact = _SEPARATORS.sub("", unicodedata.normalize("NFKC", expression))
    if not _KANA.fullmatch(compact):
        return ""
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" or c in "ヽヾ" else c
                   for c in compact)


def _character_games(character: dict[str, Any], games: dict[str, dict[str, Any]],
                     platforms: set[str]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for association in character.get("vns", []):
        if association.get("spoiler", 0) != 0:
            continue
        game = games.get(association["id"])
        if game is None:
            continue
        specific = association.get("release")
        release_id = specific.get("id") if specific else None
        matching = set()
        for release in game["releases"]:
            if release_id is None or release["id"] == release_id:
                matching.update(set(release["platforms"]) & platforms)
        if matching:
            found.setdefault(game["id"], set()).update(matching)
    return found


def _terms(characters: list[dict[str, Any]], games: dict[str, dict[str, Any]],
           platforms: set[str]) -> tuple[list[list[Any]], int]:
    glosses: dict[str, set[str]] = {}
    character_ids: set[str] = set()
    for character in sorted(characters, key=lambda c: _id_key(c["id"])):
        appearances = _character_games(character, games, platforms)
        if not appearances:
            continue
        names = [character.get("original") or "", *character.get("aliases", [])]
        # Some characters' primary names are already in Japanese script.
        names.append(character.get("name") or "")
        variants = {variant for name in names for variant in name_variants(name)}
        if not variants:
            continue
        character_ids.add(character["id"])
        full_name = character.get("name") or character.get("original") or character["id"]
        original = character.get("original")
        if original and original != full_name:
            full_name += f" ({original})"
        definitions = set()
        for vn_id, available in sorted(appearances.items(), key=lambda pair: _id_key(pair[0])):
            game = games[vn_id]
            title = game["title"]
            if game.get("alttitle") and game["alttitle"] != title:
                title += f" / {game['alttitle']}"
            labels = ", ".join(PLATFORMS[p] for p in sorted(available))
            definitions.add(f"{full_name}\n{title} [{labels}]\nhttps://vndb.org/{character['id']}")
        for expression in variants:
            glosses.setdefault(expression, set()).update(definitions)
    terms = [
        [expression, kana_reading(expression), "", "", 0, sorted(glosses[expression]), sequence, "name"]
        for sequence, expression in enumerate(sorted(glosses), 1)
    ]
    return terms, len(character_ids)


def _write_zip(path: Path, index: dict[str, Any], terms: list[list[Any]]) -> None:
    members: list[tuple[str, Any]] = [
        ("index.json", index),
        ("tag_bank_1.json", [["name", "name", 0, "Visual novel character name", 0]]),
    ]
    members.extend((f"term_bank_{i // BANK_SIZE + 1}.json", terms[i:i + BANK_SIZE])
                   for i in range(0, len(terms), BANK_SIZE))
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, value in members:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, _json_bytes(value), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(snapshot: dict[str, Any], output_dir: str | Path) -> dict[str, Any]:
    """Write three importable dictionaries, release evidence and build counts."""
    if snapshot.get("schema_version") != 1:
        raise ValueError("Unsupported snapshot schema_version; expected 1")
    games = qualifying_games(snapshot)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "snapshot_as_of": snapshot["as_of"],
        "total_qualifying_games": len(games),
        "games_file": "games.json",
        "generated_dictionaries": [],
    }
    variants = [
        ("VNDB-Names-PSP-PSVita.zip", "VNDB Names — PSP & PS Vita", {"psp", "psv"}),
        ("VNDB-Names-PSP.zip", "VNDB Names — PSP", {"psp"}),
        ("VNDB-Names-PSVita.zip", "VNDB Names — PS Vita", {"psv"}),
    ]
    for filename, title, platforms in variants:
        terms, character_count = _terms(snapshot["characters"], games, platforms)
        index = {
            "title": title, "format": 3, "revision": snapshot["as_of"], "sequenced": True,
            "sourceLanguage": "ja", "targetLanguage": "en",
            "author": "VNDB contributors; PSP / PS Vita dictionary builder",
            "url": "https://vndb.org/",
            "description": "Japanese character names from visual novels with a complete, released PSP or PS Vita edition. Non-spoiler associations only. Kana-only readings are normalized; kanji readings are not guessed.",
            "attribution": "VNDB contributors (https://vndb.org/). VNDB database: Open Database License 1.0 (https://opendatacommons.org/licenses/odbl/1-0/); database contents: Database Contents License 1.0 (https://opendatacommons.org/licenses/dbcl/1-0/). Inspired by kaanium/VNDB-Names-for-Yomitan (MIT).",
        }
        path = output / filename
        _write_zip(path, index, terms)
        summary["generated_dictionaries"].append({
            "file": filename, "title": title, "platforms": sorted(platforms),
            "game_count": sum(bool(set(g["platforms"]) & platforms) for g in games.values()),
            "character_count": character_count, "entry_count": len(terms),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "size_bytes": path.stat().st_size,
        })
    (output / "games.json").write_bytes(_json_bytes(list(games.values())))
    (output / "build-summary.json").write_bytes(_json_bytes(summary))
    return summary
