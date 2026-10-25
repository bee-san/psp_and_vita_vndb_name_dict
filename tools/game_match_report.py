"""Can Rubi tell which VNDB game is running? Matching by title ID and by on-console title.

Sources:
  - VNDB's Kana API: PSP/Vita releases (catalog numbers, PlayStation Store content IDs,
    titles in every language) and the titles and aliases of their VNs;
  - Vita3K's compatibility list: GitHub issues, each a Vita title ID with the game's name.

The title normalization is the one Rubi would run on a console (light_norm): ASCII and
full-width letters folded, half-width kana widened, diacritics dropped, Roman numerals
spelled, and everything but letters, digits, kana and kanji removed. No NFKC tables.

Writes reports/game-match.json (summary and per-game detail) and reports/game-match.md.
"""
from __future__ import annotations
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vndb_names.fetch import KanaClient  # noqa: E402

TITLE_ID = re.compile(r"\b(PCS[A-H]\d{5})\b")
CONTENT_ID = re.compile(r"^[A-Z]{2}\d{4}-([A-Z]{4}\d{5})_\d{2}-")
VITA_ID = re.compile(r"^PCS[A-H]\d{5}$")
PSP_ID = re.compile(r"^(?:U[LC][A-Z]{2}|NP[UEJHAK][HGZ])\d{5}$")
ROMAN = {chr(0x2160 + i): r for i, r in enumerate("i ii iii iv v vi vii viii ix x xi xii".split())}
ROMAN.update({chr(0x2170 + i): r for i, r in enumerate("i ii iii iv v vi vii viii ix x xi xii".split())})
HALFWIDTH_KANA = re.compile(r"[｡-ﾟ]+")
# Edition words a release title adds and a console title leaves out (normalized; stripped from the end,
# repeatedly): VNDB's "... Download Edition", "... パッケージ版".
SUFFIXES = ("firstpresslimitededition", "downloadedition", "packageedition", "limitededition", "regularedition",
            "specialedition", "deluxeedition", "standardedition", "premiumedition", "valueedition", "firstpressedition",
            "normaledition", "dledition", "ダウンロード版", "パッケージ版", "初回限定版", "完全生産限定版", "限定版",
            "通常版", "特装版", "豪華版", "廉価版", "dl版", "ベスト版", "playstationvitathebest", "psvitathebest",
            "pspthebest", "thebest", "bestprice", "forplaystationvita", "forpsvita", "forpsp")
AQUA_PRICE = re.compile(r"aquaprice\d+$")


def light_norm(text: str) -> str:
    text = HALFWIDTH_KANA.sub(lambda m: unicodedata.normalize("NFKC", m.group()), text or "")
    out = []
    for ch in text:
        c = ord(ch)
        if 0xFF01 <= c <= 0xFF5E:
            ch = chr(c - 0xFEE0)
            c = ord(ch)
        if ch in ROMAN:
            out.append(ROMAN[ch])
        elif "A" <= ch <= "Z" or "a" <= ch <= "z" or "0" <= ch <= "9":
            out.append(ch.lower())
        elif 0xC0 <= c <= 0x24F and c not in (0xD7, 0xF7):
            base = unicodedata.normalize("NFD", ch)[0]
            out.append(base.lower() if base.isascii() else ch.lower())
        elif (0x3041 <= c <= 0x3096 or 0x30A1 <= c <= 0x30FA or c in (0x3005, 0x3006, 0x309D, 0x309E,
              0x30FC, 0x30FD, 0x30FE) or 0x3400 <= c <= 0x4DBF or 0x4E00 <= c <= 0x9FFF
              or 0xF900 <= c <= 0xFAFF or c >= 0x20000):
            out.append(ch)
    return "".join(out)


def strip_suffix(norm: str) -> str:
    changed = True
    while changed:
        changed = False
        m = AQUA_PRICE.search(norm)
        if m and m.start() > 2:
            norm, changed = norm[: m.start()], True
        for s in SUFFIXES:
            if norm.endswith(s) and len(norm) > len(s) + 2:
                norm, changed = norm[: -len(s)], True
    return norm


def github_issues(repo: str) -> list[dict]:
    token = os.environ.get("GITHUB_TOKEN", "")
    rows, page = [], 1
    while True:
        req = Request(f"https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}",
                      headers={"Accept": "application/vnd.github+json", "User-Agent": "rubi-game-match",
                               **({"Authorization": f"Bearer {token}"} if token else {})})
        with urlopen(req, timeout=60) as r:
            batch = json.load(r)
        if not batch:
            return rows
        rows.extend(i for i in batch if "pull_request" not in i)
        page += 1


def vita3k_entries() -> list[dict]:
    out = []
    for issue in github_issues("Vita3K/compatibility"):
        title = issue.get("title") or ""
        ids = TITLE_ID.findall(title)
        if len(ids) != 1:
            continue
        name = TITLE_ID.sub("", title)
        name = re.sub(r"^[\s\[\]()\-–—|:]+|[\s\[\]()\-–—|:]+$", "", name)
        out.append({"id": ids[0], "name": name, "issue": issue["number"],
                    "labels": [l["name"] for l in issue.get("labels", [])]})
    return out


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    games = json.loads((root / "dist/games.json").read_text(encoding="utf-8"))
    snapshot = json.loads((root / "data/snapshot.json").read_text(encoding="utf-8"))
    qualifying = {g["id"]: g for g in games}
    client = KanaClient(root / ".cache/kana")
    scope = ["or", ["platform", "=", "psp"], ["platform", "=", "psv"]]
    releases = client.all("release", scope, "title,alttitle,platforms,catalog,languages{lang,title,latin},"
                                            "extlinks{name,id},vns{id,rtype}")
    vns = client.all("vn", scope, "title,alttitle,titles{lang,title,latin},aliases")
    vn_by_id = {v["id"]: v for v in vns}

    # Characters per VN, as the builder scopes them.
    chars = Counter()
    for c in snapshot["characters"]:
        for v in {a["id"] for a in c.get("vns", []) if a["id"] in qualifying and not a.get("spoiler")}:
            chars[v] += 1

    ids = {p: defaultdict(set) for p in ("psp", "psv")}       # VN -> title IDs from VNDB
    titles = {p: defaultdict(set) for p in ("psp", "psv")}    # VN -> normalized titles
    for r in releases:
        plats = [p for p in ("psp", "psv") if p in r.get("platforms", [])]
        names = {r.get("title"), r.get("alttitle")}
        for lang in r.get("languages") or []:
            names.update((lang.get("title"), lang.get("latin")))
        found = set()
        for link in r.get("extlinks") or []:
            if str(link.get("name", "")).startswith("playstation"):
                m = CONTENT_ID.match(str(link.get("id", "")))
                if m:
                    found.add(m.group(1))
        for part in re.split(r"[/,;、]|\s{2,}", (r.get("catalog") or "").upper()):
            norm = re.sub(r"[\s\-_]", "", part)
            if VITA_ID.match(norm) or PSP_ID.match(norm):
                found.add(norm)
        for v in r.get("vns") or []:
            if v["id"] not in qualifying:
                continue
            for p in plats:
                titles[p][v["id"]].update(n for n in map(light_norm, filter(None, names)) if len(n) >= 2)
                ids[p][v["id"]].update(t for t in found if (VITA_ID if p == "psv" else PSP_ID).match(t))
    for vid in qualifying:
        v = vn_by_id.get(vid, {})
        names = {v.get("title"), v.get("alttitle"), *(v.get("aliases") or [])}
        for t in v.get("titles") or []:
            names.update((t.get("title"), t.get("latin")))
        normed = {n for n in map(light_norm, filter(None, names)) if len(n) >= 2}
        for p in ("psp", "psv"):
            if p in qualifying[vid]["platforms"]:
                titles[p][vid].update(normed)

    # One normalized title, which Vita VNs: a title shared by several is ambiguous.
    title_vns = defaultdict(set)
    for vid, ts in titles["psv"].items():
        for t in ts:
            title_vns[t].add(vid)
            title_vns[strip_suffix(t)].add(vid)
    id_vn = defaultdict(set)
    for vid, ts in ids["psv"].items():
        for t in ts:
            id_vn[t].add(vid)

    v3k = vita3k_entries()
    v3k_by_id = defaultdict(list)
    for e in v3k:
        v3k_by_id[e["id"]].append(e)

    # 1. On-console title matching, estimated where the answer is known: a Vita3K entry whose
    #    title ID VNDB gives for a VN. Does its name match one of that VN's titles?
    pairs, exact_ok, suffix_ok, unique_ok, misses = 0, 0, 0, 0, []
    for vid, tids in ids["psv"].items():
        for tid in tids:
            for e in v3k_by_id.get(tid, []):
                pairs += 1
                n = light_norm(e["name"])
                hit = n in titles["psv"][vid]
                shit = hit or strip_suffix(n) in {strip_suffix(t) for t in titles["psv"][vid]}
                exact_ok += hit
                suffix_ok += shit
                unique_ok += shit and (title_vns.get(n) or title_vns.get(strip_suffix(n))) == {vid}
                if not shit and len(misses) < 60:
                    misses.append({"vn": vid, "tid": tid, "vita3k": e["name"],
                                   "vndb": sorted(titles["psv"][vid])[:6]})

    # 2. Build-time enrichment: Vita3K titles that match exactly one Vita VN give it title IDs.
    enriched = defaultdict(set)
    conflicts = []
    for e in v3k:
        n = light_norm(e["name"])
        cands = title_vns.get(n) or title_vns.get(strip_suffix(n)) or set()
        if len(cands) == 1:
            vid = next(iter(cands))
            known = id_vn.get(e["id"])
            if known and vid not in known:
                conflicts.append({"tid": e["id"], "vita3k": e["name"], "title_vn": vid, "id_vns": sorted(known)})
                continue
            enriched[vid].add(e["id"])

    def tally(vids):
        vids = list(vids)
        return {"games": len(vids), "characters": sum(chars[v] for v in vids)}

    psv = [v for v in qualifying if "psv" in qualifying[v]["platforms"]]
    psp = [v for v in qualifying if "psp" in qualifying[v]["platforms"]]
    psv_vndb = [v for v in psv if ids["psv"].get(v)]
    psv_v3k = [v for v in psv if enriched.get(v)]
    psv_either = [v for v in psv if ids["psv"].get(v) or enriched.get(v)]
    psv_in_v3k = [v for v in psv if any(t in v3k_by_id for t in ids["psv"].get(v, ())) or enriched.get(v)]
    ambiguous = {t: sorted(vs) for t, vs in title_vns.items() if len(vs) > 1}
    prefixes = Counter(e["id"][:4] for e in v3k)
    summary = {
        "vita3k_entries": len(v3k), "vita3k_distinct_ids": len(v3k_by_id),
        "vita3k_id_prefixes": dict(prefixes.most_common()),
        "psp_games": tally(psp), "psp_with_vndb_disc_id": tally(v for v in psp if ids["psp"].get(v)),
        "vita_games": tally(psv),
        "vita_with_vndb_title_id": tally(psv_vndb),
        "vita_with_vita3k_title_match": tally(psv_v3k),
        "vita_with_either": tally(psv_either),
        "vita_games_listed_in_vita3k": tally(psv_in_v3k),
        "title_check_pairs": pairs,
        "title_check_exact": exact_ok, "title_check_with_suffixes": suffix_ok,
        "title_check_unique_game": unique_ok,
        "enrichment_conflicts": len(conflicts),
        "ambiguous_vita_titles": len(ambiguous),
        "clannad_v4": {"vndb_ids": sorted(ids["psv"].get("v4", ())), "vita3k_ids": sorted(enriched.get("v4", ())),
                       "vita3k_names": [e["name"] for t in ("PCSG00415",) for e in v3k_by_id.get(t, [])]},
    }
    unmatched = sorted((v for v in psv if not (ids["psv"].get(v) or enriched.get(v))), key=lambda v: -chars[v])
    unmatched_sample = [{"vn": v, "title": qualifying[v]["title"], "characters": chars[v],
                         "titles": sorted({strip_suffix(t) for t in titles["psv"][v]})[:5]} for v in unmatched[:60]]
    out = root / "reports"
    out.mkdir(exist_ok=True)
    detail = {"summary": summary, "misses": misses, "unmatched_vita": unmatched_sample, "conflicts": conflicts[:80],
              "ambiguous": dict(sorted(ambiguous.items())[:200]),
              "vita": {v: {"title": qualifying[v]["title"], "characters": chars[v],
                           "vndb_ids": sorted(ids["psv"].get(v, ())), "vita3k_ids": sorted(enriched.get(v, ()))}
                       for v in psv},
              "psp": {v: {"title": qualifying[v]["title"], "characters": chars[v],
                          "vndb_ids": sorted(ids["psp"].get(v, ()))} for v in psp}}
    (out / "game-match.json").write_text(json.dumps(detail, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = ["# Game matching report", "", "```json", json.dumps(summary, ensure_ascii=False, indent=1), "```", "",
             "## Title misses (Vita3K name vs VNDB titles, normalized)", ""]
    lines += [f"- {m['vn']} {m['tid']}: `{m['vita3k']}` vs {', '.join('`'+t+'`' for t in m['vndb'])}" for m in misses]
    lines += ["", "## Vita games with no title ID (most characters first)", ""]
    lines += [f"- {u['vn']} {u['title']} ({u['characters']} characters): {', '.join('`'+t+'`' for t in u['titles'])}"
              for u in unmatched_sample]
    lines += ["", "## Conflicts", ""] + [f"- {c}" for c in conflicts[:40]]
    (out / "game-match.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
