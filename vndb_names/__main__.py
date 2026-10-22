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
    build = sub.add_parser("build", help="Build importable ZIPs without network access")
    build.add_argument("--snapshot", type=Path, default=Path("data/snapshot.json"))
    build.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    if args.command == "fetch":
        snapshot = fetch_snapshot(args.as_of.isoformat(), args.snapshot, args.cache, args.delay)
        print(f"Saved {len(snapshot['releases'])} releases, {len(snapshot['characters'])} characters")
    else:
        from .dictionary import build
        summary = build(json.loads(args.snapshot.read_text(encoding="utf-8")), args.output)
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
