from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path
from .fetch import fetch_snapshot


def main():
    parser = argparse.ArgumentParser(description="PSP/PS Vita VNDB names for Yomitan")
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch", help="Fetch VNDB data, resuming cached requests")
    fetch.add_argument("--as-of", default=date.today().isoformat(), type=date.fromisoformat)
    fetch.add_argument("--snapshot", type=Path, default=Path("data/snapshot.json"))
    fetch.add_argument("--cache", type=Path, default=Path(".cache/kana"))
    fetch.add_argument("--delay", type=float, default=1.6)
    ids = sub.add_parser("fetch-ids", help="Fetch the title IDs consoles report (VNDB and Vita3K)")
    ids.add_argument("--output", type=Path, default=Path("data/title-ids.json"))
    ids.add_argument("--cache", type=Path, default=Path(".cache/kana"))
    ids.add_argument("--delay", type=float, default=1.6)
    build = sub.add_parser("build", help="Build importable ZIPs without network access")
    build.add_argument("--title-ids", type=Path, default=Path("data/title-ids.json"),
                       help="per-game names keyed by title ID, when this file exists")
    build.add_argument("--snapshot", type=Path, default=Path("data/snapshot.json"))
    build.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    if args.command == "fetch":
        snapshot = fetch_snapshot(args.as_of.isoformat(), args.snapshot, args.cache, args.delay)
        print(f"Saved {len(snapshot['releases'])} releases, {len(snapshot['characters'])} characters")
    elif args.command == "fetch-ids":
        from .games import fetch_title_ids
        data = fetch_title_ids(args.output, args.cache, args.delay)
        print(f"Saved {len(data['releases'])} releases, {len(data['vita3k'])} Vita3K entries")
    else:
        from .dictionary import build
        title_ids = (json.loads(args.title_ids.read_text(encoding="utf-8"))
                     if args.title_ids.is_file() else None)
        summary = build(json.loads(args.snapshot.read_text(encoding="utf-8")), args.output, title_ids)
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
