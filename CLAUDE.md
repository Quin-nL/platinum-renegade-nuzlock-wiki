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
- `docs/trainer_changes/` — one page per route/location listing trainer rosters; starter-choice variants use MkDocs `===` tab syntax
- `docs/wild_pokemon/` — one page per area listing wild encounter tables with time-of-day slots
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


