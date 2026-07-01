# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A MkDocs-based wiki for Pokémon Renegade Platinum (a Platinum ROM hack by Drayano). It documents all 493 Pokémon with their modified stats, moves, abilities, and encounter locations, plus trainer rosters, wild Pokémon tables, and game-change documentation.

## Setup and development

```sh
pip install -r requirements.txt   # mkdocs, mkdocs-material, numpy, tqdm
python -m mkdocs serve            # local dev server
```

```sh
python fix_table_formatting.py ./docs/*.md ./docs/*/*.md
python fix_links.py /pokemons/*.md   # add new link definitions to links.txt first
```

## Content structure

- `docs/pokemons/NNN.md` — one page per Pokémon (001–493), containing type/defense chart, abilities, base stats, level-up moves, learnable moves, and encounter locations
- `docs/area_changes/` — one page per area combining trainers, wild encounter tables (with time-of-day slots), items, and Pokémon events
- `docs/` — game-change overview pages (move_changes, type_changes, evolution_changes, item_changes, npc_changes, etc.)
- `includes/` — reusable snippets for ability tooltips (`abilities.md`), held items (`held_items.md`), moves (`moves.md`) and natures (`natures.md`); these are injected via MkDocs `include` directives

## Markdown conventions

- Pokémon images use reference-style links: `![][001]` with `[001]: ../img/pokemon/001.png` at the bottom of the file
- Type/damage-class icons follow the same pattern: `![][grass]`, `![][physical]`
- Move tables include `{: data-sort="..."}` attributes on type and damage-class cells to enable JS sorting
- Pokémon name links resolve to their page: `[Bulbasaur]: ../../pokemons/001/`
- Link definitions (bottom of each file) must use paths relative to that file's depth; `fix_links.py` and `links.txt` automate this

## MkDocs config

The site uses the Material theme (`mkdocs.yml`). Nav is fully enumerated — adding a new page requires a corresponding entry in the `nav:` section. The `docs/config.json` is a legacy MDwiki config and is not used by MkDocs.

## Working Style

- Make sure that clarifying questions are asked before making changes.
- Be certain that any changes adhere to style guidelines
- Changes should support an expansion or restructuring of the wiki.

# Plan: CSV to box

The files in AuthoriatveCSV have all been added to area_changes. Now we need to add trainer battles to my_box. For this we will create a .md for each .csv with trainer information only. Then in my_box section the user view trainers from a given section easily.

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

