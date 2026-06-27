# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A MkDocs-based wiki for Pokémon Renegade Platinum (a Platinum ROM hack by Drayano). It documents all 493 Pokémon with their modified stats, moves, abilities, and encounter locations, plus trainer rosters, wild Pokémon tables, and game-change documentation.

## Setup and development

```sh
pip install -r requirements.txt   # mkdocs, mkdocs-material, numpy, tqdm
python -m mkdocs serve            # local dev server
```

## Utility scripts

These scripts generate or repair content in the `docs/` directory. They pull data from PokeAPI (cached in `temp/`) and from existing wiki pages:

| Script | Purpose |
|---|---|
| `download_pokemon.py` | Seeds the `temp/` cache from PokeAPI (run first) |
| `create_level_up_table.py` | Adds level-up move tables to Pokémon pages |
| `create_stat_table.py` | Adds base stat tables to Pokémon pages |
| `create_encounter_table.py` | Adds encounter location tables to Pokémon pages |
| `create_ability_table.py` | Adds ability tables to Pokémon pages |
| `create_learnable_table.py` | Adds TM/HM learnable move tables |
| `create_held_item_md.py` | Generates held item markdown |
| `fix_table_formatting.py` | Normalizes column widths in markdown tables |
| `fix_links.py` | Fixes relative link paths across files |

Run `fix_table_formatting.py` and `fix_links.py` on a range of files:

```sh
python fix_table_formatting.py ./docs/*.md ./docs/*/*.md
python fix_links.py /pokemons/*.md   # add new link definitions to links.txt first
```

## Content structure

- `docs/pokemons/NNN.md` — one page per Pokémon (001–493), containing type/defense chart, abilities, base stats, level-up moves, learnable moves, and encounter locations
- `docs/area_changes/` — one page per area combining trainers, wild encounter tables (with time-of-day slots), items, and Pokémon events
- `docs/` — game-change overview pages (move_changes, type_changes, evolution_changes, item_changes, npc_changes, etc.)
- `includes/` — reusable snippets for ability tooltips (`abilities.md`), held items (`held_items.md`), and natures (`natures.md`); these are injected via MkDocs `include` directives

## Markdown conventions

- Pokémon images use reference-style links: `![][001]` with `[001]: ../img/pokemon/001.png` at the bottom of the file
- Type/damage-class icons follow the same pattern: `![][grass]`, `![][physical]`
- Move tables include `{: data-sort="..."}` attributes on type and damage-class cells to enable JS sorting
- Pokémon name links resolve to their page: `[Bulbasaur]: ../../pokemons/001/`
- Trainer roster tables use `<br>` within cells to stack the trainer sprite, name, level, and Pokémon
- Link definitions (bottom of each file) must use paths relative to that file's depth; `fix_links.py` and `links.txt` automate this

## MkDocs config

The site uses the Material theme (`mkdocs.yml`). Nav is fully enumerated — adding a new page requires a corresponding entry in the `nav:` section. The `docs/config.json` is a legacy MDwiki config and is not used by MkDocs.

## Working Style

- Make sure that clarifying questions are asked before making changes.
- Be certain that any changes adhere to style guidelines
- Changes should support an expansion or restructuring of the wiki.

# Plan: Import Authoritative CSV Trainer Data into area_changes

## Context

8 "split" CSVs in `AutoriativeCSV/` document every trainer from game-start through each gym leader (Oreburgh → Volkner). They are the authoritative source for trainer data. The existing `docs/area_changes/` files already have trainer tables, but they're missing:
- Held items and abilities for regular (non-boss) trainers
- Base stats on all trainer Pokémon cards
- Any corrections to wrong Pokémon/moves

Goal: update each `area_changes/*.md` file with the CSV data spread across the correct location files (not consolidated into one gym file). Starter-choice variants use the existing `===` tab syntax already present in some files.

---

## CSV Structure

Each trainer occupies a fixed block of ~10 rows. Pokémon fit into up to 6 "slots" at column bases **4, 12, 19, 28, 36, 44** (8 cols each). Within each slot:

| Offset | Row A (pokemon) | Row B (types) | Row C (trainer/stat hdr) | Row D (stats) | Row E (items) | Row F (nature) | Rows G–J (moves)|
|--------|-----------------|---------------|--------------------------|---------------|---------------|----------------|-----------------|
| +0     | —               | —             | HP header                | HP            | —             | Nature         | Move            | 
| +1     | `#NNN Pokemon`  | —             | Atk header               | Atk           | —             | —              | —               |
| +2     | —               | TYPE I        | Def header               | Def           | Held Item     | —              | —               |
| +4     | —               | —             | SpA header               | SpA           | —             | —              | Power           |
| +5     | —               | TYPE II       | SpD header               | SpD           | Abiltiy       | —              | Accuracy        |
| +6     | Level (`Lv.XX`) | —             | Spe header               | Spe           | —             | —              | PP              |
| +7     | —               | —             | Total header             | Total         | —             | IVs            | —               |

- **Col 1** of the Trainer row = `TRAINER NAME [ID]`; subsequent rows in the block are specific to the Trainer Label Cell
- **Col 2** of the Trainer row = variant condition, e.g. `(IF YOU CHOSE PIPLUP)`
- **Location sections** = all-caps, col 1 only, empty col 2+

### Special markers to strip
- `(!)` suffix = new/changed ability or move — strip from output
- Zero-width/superscript Unicode chars (᠋, ᠎, ឵ space) = annotated changes — strip from output
- `Lv.XX` in slot = shown with a space in md: `Lv. XX`

### Trainer Label. 
Each trainer has 8 pieces of specific data 
They appear in the column before the first Pokemon on a team ctolumn base **3** 

| Offset |  A (pokemon) | Row B (types) | Row C (trainer/stat hdr) | Row D (stats)     | Row E (items) | Row F (nature) | Row G | Row H | Row I |  Row J | Row K |  
|--------|--------------|---------------|--------------------------|-------------------|---------------|----------------|-------|-------|-------|--------|-------|
| -0     | —            | —             | trainer name in col 1    | MandatoryOptional | Conditions    | Situated       |Use    |Action |Info   |Gifts   |Spin   | 


---

## Target Card Format

### Trainer Label (first cell)

```markdown
![][Trainer Name]<br>Trainer Name<hr><br>MandatoryOptional<br>Conditions<br>Situated<br>Use<br>Action<br>Info<br>Gifts<br>Spinning

```
- Use trainer image where one exists![][Trainer Name], Leave image empty if there is not one. 


### Regular Pokemon (new — adds item, ability, stats)

```markdown
![][NNN]<br>[Pokemon]<br>Lv. XX<br>Item Name<br>Nature / Ability<br>HP/Atk/Def/SpA/SpD/Spe<hr><ul><li>Move1</li><li>Move2</li><li>Move3</li><li>Move4</li></ul> | &nbsp; --- | --- | ---
```

- If "No Item" → omit the item line entirely (blank looks cleaner)
Stats compact inline: `45/49/49/65/65/45` (HP/Atk/Def/SpA/SpD/Spe, no Total)
- Nature includes all details: 'Modest (+SpA, -Atk)` — wait, check existing files. **Keep full nature string** to match existing gym leader card convention.

### Starter-choice variants

Multiple trainer blocks in the CSV with the same trainer name but different `(IF YOU CHOSE X)` conditions → wrap in MkDocs tab syntax:

```markdown
=== "Chose Turtwig"

    Trainer Name | ![][NNN]<br>...
    --- | ---

=== "Chose Chimchar"

    Trainer Name | ![][NNN]<br>...
    --- | ---
```

---

## Script: `csv_to_area_changes.py`

**Single script**, accepts one CSV path as argument. Run it once per CSV file.

### Algorithm

```
1. Read CSV into rows list
2. Scan for location headers (col 0 == '', col 1 all-caps, cols 2+ empty)
3. For each location section:
   a. Identify all trainer blocks between this header and the next header/end
   b. Parse each trainer block into a Trainer object:
      - Trainer_Label (strip [ID])
      - per_pokemon: [{ dex, name, level, types, stats, item, ability, nature, moves }]
   c. Generate trainer table markdown (with tabs if variants)
4. Map location name → area_changes filename (lookup dict + fallback slug)
5. Open the target .md file:
   a. Find the `## Trainers` section (or create it)
   b. Replace content up to the next `##` section or end-of-file
   c. Write updated file
6. Check image/link refs needed and merge into the file's reference block if missing.
```

### Location name → filename mapping

Build a dict for the non-obvious cases:

```python
LOCATION_MAP = {
    "TWINLEAF TOWN": "twinleaf_town",
    "ROUTE 201": "route_201",
    "ROUTE 202": "route_202",
    "JUBILIFE CITY TRAINER SCHOOL": "jubilife_city_trainer_school",
    "JUBILIFE CITY": "jubilife_city",
    "OREBURGH GATE": "oreburgh_gate",
    "OREBURGH CITY POKEMON CENTER": "pokemon_center",  # shared?
    "OREBURGH MINE": "oreburgh_mine",
    "OREBURGH GYM": "oreburgh_gym",
    "MT CORONET ~ R207 ENTRY": "mt_coronet__route_207_entrance",
    "MT CORONET ~ R211 ENTRY": "mt_coronet__route_211_entrance",
    "MT CORONET ~ R216 ENTRY": "mt_coronet__route_216_entrance",
    "MT CORONET ~ B1F": "mt_coronet__b1f",
    "MT CORONET ~ SNOW AREA": "mt_coronet__snow_area",
    "MT CORONET ~ TUNNEL TO ROUTE 211": "mt_coronet__tunnel_to_route_211_entrance",
    # ... etc for each CSV's locations
}
```

Default fallback: lowercase, replace spaces with `_`, `~` and special chars stripped → `route_202`.

### Reference block handling

After writing the trainer table, collect all `[NNN]`, `[Pokemon]`, `[item-name]` refs needed and merge them with the existing reference block at file bottom duplicate where possible.

---

## Files Modified

- **`csv_to_area_changes.py`** — new script (write once, run per CSV)
- **`docs/area_changes/*.md`** — Trainers sections updated for every location covered by the CSVs:

## Verification

After running the script on each CSV:

1. `python -m mkdocs build --strict` — confirms no broken links or bad markdown
2. Spot-check 2–3 updated files against the CSV to verify stat/move accuracy
3. Check that starter-choice tab files render correctly in `python -m mkdocs serve`
