"""How many qualifying VNs can be tied to the PSP/Vita title ID a console reports.

Fetches catalog numbers and PlayStation Store links for the snapshot's release scope, then
extracts title IDs:
  - a PlayStation Store product ID is a content ID, JP0741-PCSG00415_00-..., whose middle
    part is the title ID;
  - a PSP UMD catalog number (ULJM-05889) is the disc ID Adrenaline reports;
  - a Vita card's catalog number (VLJM-35xxx) is NOT its title ID (PCSGxxxxx): counted apart.
Writes title-id-coverage.json and prints a summary (also as workflow notices).
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vndb_names.fetch import KanaClient, release_filter  # noqa: E402

CONTENT_ID = re.compile(r"^[A-Z]{2}\d{4}-([A-Z]{4}\d{5})_\d{2}-")
PSP_DISC = re.compile(r"^(?:U[LC][A-Z]{2}|NP[UEJHAK][HGZ])\d{5}$")
VITA_TITLE = re.compile(r"^PCS[A-H]\d{5}$")
VITA_RETAIL = re.compile(r"^V[A-Z]{3}\d{5}$")


def catalog_ids(catalog: str | None) -> list[str]:
    if not catalog:
        return []
    out = []
    for part in re.split(r"[/,;、]|\s{2,}", catalog.upper()):
        norm = re.sub(r"[\s\-_]", "", part)
        if norm:
            out.append(norm)
    return out


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    snapshot = json.loads((root / "data/snapshot.json").read_text(encoding="utf-8"))
    games = json.loads((root / "dist/games.json").read_text(encoding="utf-8"))
    qualifying = {g["id"]: {r["id"] for r in g["releases"]} for g in games}
    client = KanaClient(root / ".cache/kana")
    rows = client.all("release", release_filter(snapshot["as_of"]),
                      "platforms,catalog,gtin,extlinks{name,id},vns{id,rtype}")
    by_release = {r["id"]: r for r in rows}

    per_vn, shapes = {}, Counter()
    for vn, releases in qualifying.items():
        ids = {"psp": set(), "psv": set()}
        retail = set()
        for rid in releases:
            r = by_release.get(rid)
            if not r:
                continue
            for link in r.get("extlinks") or []:
                if str(link.get("name", "")).startswith("playstation"):
                    m = CONTENT_ID.match(str(link.get("id", "")))
                    if m:
                        tid = m.group(1)
                        ids["psv" if VITA_TITLE.match(tid) else "psp"].add(tid)
                        shapes["store:" + tid[:4]] += 1
            for c in catalog_ids(r.get("catalog")):
                if PSP_DISC.match(c) and "psp" in r["platforms"]:
                    ids["psp"].add(c); shapes["catalog-psp:" + c[:4]] += 1
                elif VITA_TITLE.match(c):
                    ids["psv"].add(c); shapes["catalog-vita-title:" + c[:4]] += 1
                elif VITA_RETAIL.match(c) and "psv" in r["platforms"]:
                    retail.add(c); shapes["catalog-vita-retail:" + c[:4]] += 1
                else:
                    shapes["catalog-other"] += 1
        per_vn[vn] = {"psp": sorted(ids["psp"]), "psv": sorted(ids["psv"]), "vita_retail_catalog": sorted(retail)}

    # characters per VN, as the builder scopes them (any non-spoiler appearance in a qualifying VN)
    chars = Counter()
    for c in snapshot["characters"]:
        for v in {a["id"] for a in c.get("vns", []) if a["id"] in qualifying and not a.get("spoiler")}:
            chars[v] += 1

    platforms = {g["id"]: set(g["platforms"]) for g in games}
    def tally(pred):
        vns = [v for v in qualifying if pred(v)]
        return len(vns), sum(chars[v] for v in vns)
    total = tally(lambda v: True)
    any_id = tally(lambda v: per_vn[v]["psp"] or per_vn[v]["psv"])
    psp_need = tally(lambda v: "psp" in platforms[v])
    psp_have = tally(lambda v: "psp" in platforms[v] and per_vn[v]["psp"])
    psv_need = tally(lambda v: "psv" in platforms[v])
    psv_have = tally(lambda v: "psv" in platforms[v] and per_vn[v]["psv"])
    psv_retail_only = tally(lambda v: "psv" in platforms[v] and not per_vn[v]["psv"] and per_vn[v]["vita_retail_catalog"])
    summary = {
        "vns_total": total, "vns_with_any_title_id": any_id,
        "psp_vns": psp_need, "psp_vns_with_psp_id": psp_have,
        "vita_vns": psv_need, "vita_vns_with_vita_title_id": psv_have,
        "vita_vns_with_only_retail_catalog": psv_retail_only,
        "id_sources": dict(shapes.most_common()),
        "note": "pairs are (VNs, characters with a non-spoiler appearance)",
    }
    (root / "title-id-coverage.json").write_text(
        json.dumps({"summary": summary, "per_vn": per_vn}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))
    for key in ("vns_with_any_title_id", "psp_vns_with_psp_id", "vita_vns_with_vita_title_id",
                "vita_vns_with_only_retail_catalog"):
        print(f"::notice title={key}::{summary[key]} of {summary['vns_total'] if key == 'vns_with_any_title_id' else summary['psp_vns' if 'psp' in key else 'vita_vns']}")
    top = ", ".join(f"{k}={v}" for k, v in shapes.most_common(12))
    print(f"::notice title=id sources::{top}")
    sample = [f"{v}:{'/'.join(per_vn[v]['psp'] + per_vn[v]['psv']) or '-'}" for v in ("v4", "v36", "v4060", "v19")]
    print(f"::notice title=samples::{' '.join(sample)}")


if __name__ == "__main__":
    main()
