# VNDB Names for Yomitan — PSP & PS Vita

A compact Japanese character-name dictionary for visual novels released on
**PlayStation Portable or PlayStation Vita**. Inspired by
[kaanium/VNDB-Names-for-Yomitan](https://github.com/kaanium/VNDB-Names-for-Yomitan).

## Downloads

Snapshot cutoff: **22 October 2026**.

| Dictionary | VNs | Characters | Searchable entries | ZIP size |
| --- | ---: | ---: | ---: | ---: |
| [PSP + PS Vita](https://github.com/bee-san/psp_and_vita_vndb_name_dict/raw/refs/heads/main/dist/VNDB-Names-PSP-PSVita.zip) | 1,202 | 12,151 | 30,713 | 1.51 MB |
| [PSP](https://github.com/bee-san/psp_and_vita_vndb_name_dict/raw/refs/heads/main/dist/VNDB-Names-PSP.zip) | 751 | 7,218 | 19,258 | 0.87 MB |
| [PS Vita](https://github.com/bee-san/psp_and_vita_vndb_name_dict/raw/refs/heads/main/dist/VNDB-Names-PSVita.zip) | 618 | 7,136 | 19,092 | 0.82 MB |

## Install

Import **`dist/VNDB-Names-PSP-PSVita.zip`** in Yomitan's dictionary settings.
Leave the ZIP compressed. Alternatively, import `VNDB-Names-PSP.zip` or
`VNDB-Names-PSVita.zip` for one platform. Choose either the combined dictionary
or the individual platform dictionaries to avoid duplicate results.

Full names, separator-free names, family/given-name parts, and Japanese aliases
are searchable. A part of one or two kana is not: those are the particles of
foreign names (the デ and ラ of ファナ=デ・ラ・…) and honorifics (村上 さん), which
would otherwise match ordinary words such as で and だ. Definitions show the full original/romanized character name,
source game, handheld platform, and VNDB character link. Distinct characters
sharing a name retain separate definitions. No pictures or biographies are
included.

## Per-game names (for Rubi)

`dist/VNDB-Names-Games.zip` holds one name list per game, keyed by the title ID a console reports:
a Vita game's (`PCSG00415`) or a PSP disc's (`ULJM05338`). An app that knows the running game can
show its characters first: in CLANNAD, 渚 is Furukawa Nagisa, not a beach. It is not a Yomitan
dictionary: `games.json` lists each game set's VNDB IDs, title, title IDs and Yomitan term rows.

- IDs come from VNDB's catalog numbers (a PSP UMD's product code is its disc ID) and PlayStation
  Store links, and from [Vita3K's compatibility list](https://github.com/Vita3K/compatibility),
  whose issues pair a Vita title ID with its game: an ID is taken when the name matches exactly
  one qualifying Vita game's VNDB titles, and never against an ID VNDB gives another game. VNDB
  records a Vita card's box code (VLJM-35xxx), not its title ID, so most Vita retail games need it.
- A bundle's ID names all its games. Within an entry, a character whose own name has the
  spelling comes before one known by it as an alias, then main characters before side ones.
- Games with no ID have no per-game list. Coverage is in `dist/build-summary.json` (`per_game`).

`python -m vndb_names fetch-ids` refreshes `data/title-ids.json`; `build` uses it when present.

## Scope

The build fetches current data from VNDB's public
[Kana API](https://api.vndb.org/kana). `dist/games.json` lists every qualifying VN
and the exact release records used to include it.

- A VN needs a **complete, non-patch PSP (`psp`) or Vita (`psv`) release** dated
  on or before the snapshot cutoff. Trials, partial releases, future/TBA dates,
  unknown dates, and other platforms are excluded. For a partial date such as
  `2015`, the latest possible day must be no later than the cutoff.
- This uses the console release's date, rather than the VN's first release on
  another platform. Bundle releases are checked per VN.
- Official and unofficial full releases qualify when VNDB records them with
  the PSP/Vita platform. A PC game merely playable through an emulator/engine
  port does not automatically qualify. PS1 Classics are not added unless VNDB
  records the relevant release under PSP/Vita.
- Only non-spoiler character appearances in a qualifying VN/release qualify.
  An appearance restricted to a different release, such as a PC edition, does
  not qualify. Generic VN-level appearances are accepted: VNDB does not provide
  a complete per-console character roster.
- Japanese-script names only. Aliases have no individual spoiler flags in
  VNDB, so this is **not a guarantee against name/alias spoilers**.
- Kana-only headwords have normalized hiragana readings. Kanji readings are
  left empty; the source romanization is shown in the definition. No guessed
  kana readings are generated from romanized names.

Counts and ZIP sizes are in `dist/build-summary.json`. “Games” counts qualifying
VNDB VN records, including records without any usable Japanese character names;
“characters” counts included VNDB character IDs; “entries” counts distinct
searchable spellings, including name parts.

## Rebuild

Python **3.10+**, standard library only. From this directory:

```sh
# Exact offline rebuild from the bundled snapshot:
python -m vndb_names build

# Fetch a new snapshot, then rebuild:
python -m vndb_names fetch --as-of 2026-10-22
python -m vndb_names build

# Tests (no network):
python -m unittest discover -s tests -v
```

Omit `--as-of` to use the current date. Fetches are rate-limited, automatically
retry temporary failures and throttling, and cache each successful response in
`.cache/kana/`. Rerun the same command after interruption to resume. Delete the
cache to force a fresh fetch with the same cutoff. A cutoff limits release dates;
it does not reconstruct the historical database as it existed on that date.

The snapshot contains the full API name/appearance responses required to rebuild,
not images or descriptions. The three dictionary ZIPs are deterministic for a
fixed snapshot. Banks contain at most 10,000 entries and use Yomitan format 3.

The included GitHub Actions workflow runs tests and an offline build on pushes
and pull requests. Its manual **Refresh** option fetches VNDB data and uploads
new ZIPs and the snapshot as workflow artifacts; it does not overwrite source
or publish a release automatically.

## Attribution and licences

Character names and release metadata: **VNDB contributors**,
[VNDB](https://vndb.org/), via [Kana](https://api.vndb.org/kana).
The resulting database is offered under the **Open Database License 1.0**;
individual database contents are covered by the **Database Contents License 1.0**.
See `LICENSE-DATA-ODbL.txt`, `LICENSE-DATA-DbCL.txt`, and
[VNDB's data licence](https://vndb.org/d17#3). Preserve this attribution when
redistributing the data or dictionaries.

Builder code: [MIT](LICENSE). The original project is credited as inspiration;
this build fetches a new platform-filtered dataset rather than filtering its
old all-VN dictionary.
