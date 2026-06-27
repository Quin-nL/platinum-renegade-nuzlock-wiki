#!/usr/bin/env python3
"""
csv_to_area_changes.py — Import authoritative CSV trainer data into docs/area_changes/*.md
Usage: python csv_to_area_changes.py <CSV_FILE> [--dry-run]

REMATCHES CSV is detected by filename and routes trainer blocks into the
### Rematches subsection of each file instead of the main trainer table.
"""

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

DOCS = Path("docs/area_changes")
SLOT_BASES = [4, 12, 20, 28, 36, 44]

INCLUDES = [
    '--8<-- "includes/abilities.md"',
    '--8<-- "includes/held_items.md"',
    '--8<-- "includes/natures.md"',
]

POKEMON_NAME_FIXES = {
    'Nidoran ♀': 'Nidoran♀',
    'Nidoran ♂': 'Nidoran♂',
}

LOCATION_MAP = {
    "TWINLEAF TOWN": "twinleaf_town",
    "ROUTE 201": "route_201",
    "LAKE VERITY": "lake_verity",
    "SANDGEM TOWN": "sandgem_town",
    "ROUTE 202": "route_202",
    "JUBILIFE CITY": "jubilife_city",
    "JUBILIFE CITY TRAINER SCHOOL": "jubilife_city_trainer_school",
    "JUBILIFE CITY POKEMON CENTER": "jubilife_city",
    "ROUTE 204 ~ SOUTH": "route_204__south",
    "ROUTE 203": "route_203",
    "OREBURGH GATE": "oreburgh_gate",
    "OREBURGH CITY": "oreburgh_city",
    "OREBURGH CITY POKEMON CENTER": "oreburgh_city",
    "OREBURGH MINE": "oreburgh_mine",
    "OREBURGH GYM": "oreburgh_gym",
    "ROUTE 204 ~ NORTH": "route_204__north",
    "FLOAROMA TOWN": "floaroma_town",
    "VALLEY WINDWORKS": "valley_windworks",
    "FLOAROMA MEADOW": "floaroma_meadow",
    "ROUTE 205 ~ SOUTH": "route_205__south",
    "ETERNA FOREST": "eterna_forest",
    "ROUTE 205 ~ NORTH": "route_205__north",
    "ETERNA CITY": "eterna_city",
    "ETERNA GYM": "eterna_gym",
    "ROUTE 206": "route_206",
    "WAYWARD CAVE": "wayward_cave",
    "ROUTE 207": "route_207",
    "MT CORONET ~ R207 ENTRY": "mt_coronet__route_207_entrance",
    "HEARTHOME CITY": "hearthome_city",
    "HEARTHOME GYM": "hearthome_gym",
    "ROUTE 208": "route_208",
    "AMITY SQUARE": "amity_square",
    "ROUTE 209": "route_209",
    "LOST TOWER": "lost_tower",
    "SOLACEON TOWN": "solaceon_town",
    "SOLACEON RUINS": "solaceon_ruins",
    "VEILSTONE CITY": "veilstone_city",
    "VEILSTONE GYM": "veilstone_gym",
    "ROUTE 210 ~ SOUTH": "route_210__south",
    "CELESTIC TOWN": "celestic_town",
    "MT CORONET ~ R211 ENTRY": "mt_coronet__route_211_entrance",
    "PASTORIA CITY": "pastoria_city",
    "GREAT MARSH": "great_marsh",
    "PASTORIA GYM": "pastoria_gym",
    "ROUTE 212 ~ NORTH": "route_212__north",
    "ROUTE 212 ~ SOUTH": "route_212__south",
    "ROUTE 213": "route_213",
    "VALOR LAKEFRONT": "valor_lakefront",
    "LAKE VALOR": "lake_valor",
    "ROUTE 214": "route_214",
    "RUIN MANIAC CAVE": "maniac_tunnel",
    "ROUTE 215": "route_215",
    "CANALAVE CITY": "canalave_city",
    "CANALAVE GYM": "canalave_gym",
    "IRON ISLAND": "iron_island",
    "MT CORONET ~ B1F": "mt_coronet__b1f",
    "MT CORONET ~ SNOW AREA": "mt_coronet__snow_area",
    "MT CORONET ~ R216 ENTRY": "mt_coronet__route_216_entrance",
    "ROUTE 216": "route_216",
    "ROUTE 217": "route_217",
    "ACUITY LAKEFRONT": "acuity_lakefront",
    "LAKE ACUITY": "lake_acuity",
    "SNOWPOINT CITY": "snowpoint_city",
    "SNOWPOINT GYM": "snowpoint_gym",
    "ROUTE 218": "route_218",
    "FUEGO IRONWORKS": "fuego_ironworks",
    "GALACTIC HQ": "galactic_hq",
    "MT CORONET ~ TUNNEL TO ROUTE 211": "mt_coronet__tunnel_to_route_211_entrance",
    "SPEAR PILLAR": "spear_pillar",
    "DISTORTION WORLD": "distortion_world",
    "SUNYSHORE CITY": "sunyshore_city",
    "SUNYSHORE GYM": "sunyshore_gym",
    "ROUTE 219": "route_219",
    "ROUTE 220": "route_220",
    "ROUTE 221": "route_221",
    "ROUTE 222": "route_222",
    "ROUTE 223": "route_223",
    "ROUTE 224": "route_224",
    "VICTORY ROAD ~ 1F": "victory_road__1f",
    "VICTORY ROAD ~ 2F": "victory_road__2f",
    "VICTORY ROAD ~ B1F": "victory_road__b1f",
    "POKEMON LEAGUE": "pokemon_league",
    "FIGHT AREA": "fight_area",
    "ROUTE 225": "route_225",
    "ROUTE 226": "route_226",
    "ROUTE 227": "route_227",
    "ROUTE 228": "route_228",
    "ROUTE 229": "route_229",
    "ROUTE 230": "route_230",
    "PAL PARK": "pal_park",
    "SURVIVAL AREA": "survival_area",
    "RESORT AREA": "resort_area",
    "STARK MOUNTAIN": "stark_mountain",
    "ROUTE 210 ~ NORTH": "route_210__north",
    "ROUTE 211 ~ EAST": "route_211__east",
    "ROUTE 211 ~ WEST": "route_211__west",
}

TRAINER_IMAGES = {
    "GYM LEADER ROARK": "roark",
    "GYM LEADER GARDENIA": "gardenia",
    "GYM LEADER FANTINA": "fantina",
    "GYM LEADER MAYLENE": "maylene",
    "GYM LEADER WAKE": "wake",
    "GYM LEADER BYRON": "byron",
    "GYM LEADER CANDICE": "candice",
    "GYM LEADER VOLKNER": "volkner",
    "ELITE FOUR AARON": "aaron",
    "ELITE FOUR BERTHA": "bertha",
    "ELITE FOUR FLINT": "flint",
    "ELITE FOUR LUCIAN": "lucian",
    "CHAMPION CYNTHIA": "cynthia",
    "RIVAL BARRY": "barry",
    "PKMN TRAINER LUCAS": "lucas",
    "PKMN TRAINER DAWN": "dawn",
    "ACE TRAINER F": "ace_f",
    "ACE TRAINER": "ace_m",
    "AROMA LADY": "aroma_lady",
    "BEAUTY": "beauty",
    "BIRD KEEPER": "bird_keeper",
    "BLACKBELT": "blackbelt",
    "BUG CATCHER": "bug_catcher",
    "CAMPER": "camper",
    "CLOWN": "clown",
    "COLLECTOR": "collector",
    "CYCLIST F": "cyclist_f",
    "CYCLIST M": "cyclist_m",
    "DRAGON TAMER": "dragon_tamer",
    "FISHERMAN": "fisherman",
    "GALACTIC GRUNT F": "galactic_grunt_f",
    "GALACTIC GRUNT": "galactic_grunt_m",
    "GENTLEMAN": "gentleman",
    "GUITARIST": "guitarist",
    "HIKER": "hiker",
    "JOGGER": "jogger",
    "LADY": "lady",
    "LASS": "lass",
    "PICNICKER": "picnicker",
    "POKEFAN F": "pokefan_f",
    "POKEFAN M": "pokefan_m",
    "POKÉMON RANGER F": "ranger_f",
    "POKEMON RANGER F": "ranger_f",
    "POKÉMON RANGER": "ranger_m",
    "POKEMON RANGER": "ranger_m",
    "PSYCHIC F": "psychic_f",
    "PSYCHIC M": "psychic_m",
    "PSYCHIC": "psychic_m",
    "REPORTER": "reporter",
    "RUIN MANIAC": "ruin_maniac",
    "SAILOR": "sailor",
    "SCHOOL KID F": "school_kid_f",
    "SCHOOL KID": "school_kid_m",
    "SCIENTIST": "scientist",
    "SKIER": "skier",
    "SOCIALITE": "socialite",
    "SWIMMER F": "swimmer_f",
    "SWIMMER M": "swimmer_m",
    "TUBER F": "tuber_f",
    "TUBER M": "tuber_m",
    "VETERAN": "veteran",
    "WAITER": "waiter",
    "WAITRESS": "waitress",
    "WORKER": "worker",
    "YOUNGSTER": "youngster",
}

BOSS_PREFIXES = (
    "GYM LEADER", "CHAMPION", "ELITE FOUR", "FRONTIER BRAIN",
    "BATTLE KING", "TOWER TYCOON", "CASTLE VALET", "ARCADE STAR", "FACTORY HEAD",
)

_ANNOTATION_RE = re.compile(
    r'[᠎​‌‍﻿'
    r'឵'
    r'᠋᠌]'
    r'|឵\s*',
    re.UNICODE
)
_PAREN_BANG_RE = re.compile(r'\s*\([!?]\)')

_BADGE_WORD = {
    'ONE': '1', 'TWO': '2', 'THREE': '3', 'FOUR': '4',
    'FIVE': '5', 'SIX': '6', 'SEVEN': '7', 'EIGHT': '8',
}


def clean(s: str) -> str:
    s = _ANNOTATION_RE.sub('', s)
    s = _PAREN_BANG_RE.sub('', s)
    return s.strip()


def get(row, col: int, default: str = '') -> str:
    if col < len(row):
        return clean(row[col])
    return default


def is_location_header(row) -> bool:
    col2 = row[2].strip() if len(row) > 2 else ''
    if not col2 or col2[0] == '(' or col2[0].islower():
        return False
    alpha_only = re.sub(r'[^A-Za-z]', '', col2)
    if not alpha_only or alpha_only != alpha_only.upper():
        return False
    return all(not row[j].strip() for j in range(3, min(len(row), 11)))


def is_trainer_row(row) -> bool:
    return (
        len(row) > 4
        and row[2].strip()
        and not row[2].strip().startswith('(')
        and row[3].strip() == 'HP'
        and row[4].strip() == 'Atk'
    )


def strip_id(name: str) -> str:
    return re.sub(r'\s*\[\d+\]', '', name).strip()


def trainer_img(trainer_name: str):
    name_up = strip_id(trainer_name).upper()
    for prefix in sorted(TRAINER_IMAGES, key=len, reverse=True):
        if name_up.startswith(prefix):
            return TRAINER_IMAGES[prefix]
    return None


def is_boss(trainer_name: str) -> bool:
    name_up = strip_id(trainer_name).upper()
    return any(name_up.startswith(p) for p in BOSS_PREFIXES)


def item_slug(name: str) -> str:
    return re.sub(r"['\",]", '', name).lower().replace(' ', '-')


def parse_level(raw: str) -> str:
    m = re.match(r'Lv\.?\s*(\d+)', raw)
    return f'Lv. {m.group(1)}' if m else raw


def parse_nature(raw: str) -> str:
    m = re.match(r'(\w+)', raw)
    return m.group(1) if m else raw


def parse_condition(val: str):
    """
    Return (condition_str, True) if val is a variant condition, else (None, False).
    Starter: '(IF YOU CHOSE CHIMCHAR)' → 'Chimchar'
    Badge:   '(AFTER THREE BADGES)'    → 'After 3 Badges'
    """
    m = re.match(r'\(IF YOU (?:CHOSE|PICKED)\s+(\w+)\)', val, re.I)
    if m:
        return m.group(1).capitalize(), True
    m = re.match(r'\(AFTER\s+(\w+)\s+BADGES?\)', val, re.I)
    if m:
        word = m.group(1).upper()
        digit = _BADGE_WORD.get(word, word)
        return f'After {digit} Badges', True
    return None, False


def condition_tab_label(condition: str) -> str:
    """'Chimchar' → 'Chose Chimchar', 'After 3 Badges' → 'After 3 Badges'"""
    if condition.startswith('After '):
        return condition
    return f'Chose {condition}'


# ---------------------------------------------------------------------------
# CSV parsing
# ---------------------------------------------------------------------------

def parse_csv(filepath: Path):
    with open(filepath, 'r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))

    max_col = max(len(r) for r in rows) if rows else 0
    rows = [r + [''] * (max_col - len(r)) for r in rows]

    location_data = defaultdict(list)
    current_location = None

    for i, row in enumerate(rows):
        if is_location_header(row):
            loc = row[2].strip()
            if loc not in LOCATION_MAP:
                slug = re.sub(r'\s+', '_', loc.lower())
                slug = re.sub(r'[^a-z0-9_]', '', slug)
                LOCATION_MAP[loc] = slug
            current_location = loc
            continue

        if current_location and is_trainer_row(row):
            block = parse_block(rows, i)
            if block:
                location_data[current_location].append(block)

    return location_data


def parse_block(rows, c: int) -> dict:
    if c < 2:
        return None

    row_a = rows[c - 2]
    row_c = rows[c]

    trainer_raw = get(row_c, 2)
    if not trainer_raw:
        return None

    # Combined block: alternate trainer name in Row A col 2 (e.g. Lucas/Dawn)
    alt_raw = get(row_a, 2)
    alt_name = None
    if alt_raw and re.search(r'\[\d+\]', alt_raw):
        alt_name = strip_id(alt_raw)

    label_fields = []
    condition = None

    for offset in range(1, 9):
        if c + offset >= len(rows):
            break
        val = get(rows[c + offset], 2)
        if not val:
            continue
        cond, is_cond = parse_condition(val)
        if is_cond:
            condition = cond
        else:
            # Format look-direction: '(LOOKS DOWN)' → 'Looks Down'
            looks_m = re.match(r'\(LOOKS\s+(\w+)\)', val, re.I)
            if looks_m:
                label_fields.append(f'Looks {looks_m.group(1).capitalize()}')
            else:
                label_fields.append(val)

    pokemon = []
    for b in SLOT_BASES:
        poke = _parse_slot(rows, c, row_a, b)
        if poke is None:
            break
        pokemon.append(poke)

    if not pokemon:
        return None

    return {
        'trainer_raw': trainer_raw,
        'trainer_name': strip_id(trainer_raw),
        'alt_name': alt_name,
        'condition': condition,
        'label_fields': label_fields,
        'pokemon': pokemon,
    }


def _parse_slot(rows, c, row_a, b) -> dict:
    name_raw = get(row_a, b)
    if not name_raw or '#' not in name_raw:
        return None
    m = re.match(r'#(\d+)\s+(.+)', name_raw)
    if not m:
        return None

    dex = int(m.group(1))
    name = POKEMON_NAME_FIXES.get(clean(m.group(2)), clean(m.group(2)))
    level = parse_level(get(row_a, b + 5))

    row_d = rows[c + 1] if c + 1 < len(rows) else []
    row_e = rows[c + 2] if c + 2 < len(rows) else []
    row_f = rows[c + 3] if c + 3 < len(rows) else []

    hp   = get(row_d, b - 1)
    atk  = get(row_d, b)
    def_ = get(row_d, b + 1)
    spa  = get(row_d, b + 2)
    spd  = get(row_d, b + 3)
    spe  = get(row_d, b + 4)

    item    = get(row_e, b)
    ability = get(row_e, b + 3)
    nature  = parse_nature(get(row_f, b - 1))

    moves = []
    for mi in range(4):
        row_m = rows[c + 4 + mi] if c + 4 + mi < len(rows) else []
        mv = get(row_m, b - 1)
        if mv:
            moves.append(mv)

    return {
        'dex': dex, 'name': name, 'level': level,
        'hp': hp, 'atk': atk, 'def': def_,
        'spa': spa, 'spd': spd, 'spe': spe,
        'item': item, 'ability': ability,
        'nature': nature, 'moves': moves,
    }


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def _poke_cell(poke: dict, boss: bool = False) -> str:
    dex = f'{poke["dex"]:03d}'
    parts = [f'![][{dex}]', f'[{poke["name"]}]', poke['level']]

    item = poke['item']
    if item and item.lower() != 'no item':
        if boss:
            parts.append(f'![][{item_slug(item)}]')
        parts.append(item)

    parts.append(f'{poke["nature"]} / {poke["ability"]}')
    parts.append(f'{poke["hp"]}/{poke["atk"]}/{poke["def"]}/{poke["spa"]}/{poke["spd"]}/{poke["spe"]}')

    moves_html = '<br>'.join(poke['moves'])
    return '<br>'.join(parts) + '<hr>' + moves_html


def _trainer_label(block: dict) -> str:
    name = block['trainer_name']
    img  = trainer_img(name)
    display = name.title()

    parts = []
    if img:
        parts.append(f'![][{img}]')
    parts.append(display)

    base = '<br>'.join(parts) + '<hr>'
    fields = [f for f in block['label_fields'] if f]
    if fields:
        base += '<br>' + '<br>'.join(fields)
    return base


def _regular_table(blocks: list) -> str:
    if not blocks:
        return ''
    max_poke = max(len(b['pokemon']) for b in blocks)
    headers = ['Trainer'] + [str(i + 1) for i in range(max_poke)]
    sep = ['---'] * len(headers)
    lines = [' | '.join(headers), ' | '.join(sep)]

    for block in blocks:
        label = _trainer_label(block)
        cells = [label]
        for poke in block['pokemon']:
            cells.append(_poke_cell(poke, boss=False))
        while len(cells) < len(headers):
            cells.append('&nbsp;')
        lines.append(' | '.join(cells))

    return '\n'.join(lines)


def _boss_table(block: dict) -> str:
    img = trainer_img(block['trainer_name'])
    first_cell = f'![][{img}]' if img else block['trainer_name'].title()

    cells = [first_cell]
    for poke in block['pokemon']:
        cells.append(_poke_cell(poke, boss=True))
    sep = ['---'] * len(cells)

    return ' | '.join(cells) + '\n' + ' | '.join(sep)


def _combined_rival_tabs(combined: list) -> str:
    """Nested outer(rival name) + inner(starter choice) tabs for Lucas/Dawn blocks."""
    if not combined:
        return ''

    by_condition = {b['condition']: b for b in combined}
    STARTER_ORDER = ['Turtwig', 'Chimchar', 'Piplup']
    conditions = sorted(
        by_condition.keys(),
        key=lambda c: STARTER_ORDER.index(c) if c in STARTER_ORDER else 99,
    )

    sample = combined[0]
    rival_names = [sample['alt_name'], sample['trainer_name']]

    def _outer_label(name: str) -> str:
        parts = strip_id(name).split()
        return parts[-1].capitalize() if parts else name.title()

    outer_blocks = []
    for rival_name in rival_names:
        label = _outer_label(rival_name)
        lines = [f'=== "{label}"', '']
        for cond in conditions:
            b = by_condition[cond]
            inner_label = condition_tab_label(cond)
            lines.append(f'    === "{inner_label}"')
            lines.append('')
            fake_block = {**b, 'trainer_name': rival_name, 'alt_name': None}
            table = _regular_table([fake_block])
            for line in table.split('\n'):
                lines.append(f'        {line}')
            lines.append('')
        outer_blocks.append('\n'.join(lines))

    return '\n'.join(outer_blocks)


def generate_location_section(blocks: list) -> str:
    if not blocks:
        return ''

    sections = []

    regular = [b for b in blocks if not is_boss(b['trainer_name'])]
    bosses  = [b for b in blocks if is_boss(b['trainer_name'])]

    combined = [b for b in regular if b['alt_name']]
    simple   = [b for b in regular if not b['alt_name']]

    if combined:
        sections.append(_combined_rival_tabs(combined))

    by_name = defaultdict(list)
    for b in simple:
        by_name[b['trainer_name']].append(b)

    variant_names   = [n for n, bl in by_name.items() if len(bl) > 1 and bl[0]['condition']]
    singleton_names = [n for n in by_name if n not in variant_names]

    for name in variant_names:
        group = by_name[name]
        tab_lines = []
        for b in group:
            label = condition_tab_label(b['condition']) if b['condition'] else name
            tab_lines.append(f'=== "{label}"')
            tab_lines.append('')
            table = _regular_table([b])
            for line in table.split('\n'):
                tab_lines.append(f'    {line}')
            tab_lines.append('')
        sections.append('\n'.join(tab_lines).rstrip())

    singletons = [by_name[n][0] for n in singleton_names]
    if singletons:
        sections.append(_regular_table(singletons))

    for boss in bosses:
        display = boss['trainer_name'].title()
        sections.append(f'## {display}\n\n' + _boss_table(boss))

    return '\n\n'.join(sections)


# ---------------------------------------------------------------------------
# Reference block and includes helpers
# ---------------------------------------------------------------------------

def collect_refs(blocks: list) -> tuple:
    poke_imgs    = set()
    poke_links   = set()
    item_imgs    = set()
    trainer_imgs = set()

    for block in blocks:
        img = trainer_img(block['trainer_name'])
        if img:
            trainer_imgs.add(img)
        if block.get('alt_name'):
            img2 = trainer_img(block['alt_name'])
            if img2:
                trainer_imgs.add(img2)
        boss = is_boss(block['trainer_name'])
        for p in block['pokemon']:
            dex = f'{p["dex"]:03d}'
            poke_imgs.add(dex)
            poke_links.add((dex, p['name']))
            if boss and p['item'] and p['item'].lower() != 'no item':
                item_imgs.add(item_slug(p['item']))

    return poke_imgs, poke_links, item_imgs, trainer_imgs


def merge_refs(existing_content: str, blocks: list) -> str:
    poke_imgs, poke_links, item_imgs, trainer_imgs = collect_refs(blocks)
    existing_refs = set(re.findall(r'^\[([^\]]+)\]:', existing_content, re.MULTILINE))

    new_lines = []
    for dex in sorted(poke_imgs):
        if dex not in existing_refs:
            new_lines.append(f'[{dex}]: ../img/pokemon/{dex}.png')
    for dex, name in sorted(poke_links):
        if name not in existing_refs:
            new_lines.append(f'[{name}]: ../../pokemons/{dex}/')
    for slug in sorted(item_imgs):
        if slug not in existing_refs:
            new_lines.append(f'[{slug}]: ../img/items/{slug}.png')
    for img in sorted(trainer_imgs):
        if img not in existing_refs:
            new_lines.append(f'[{img}]: ../img/trainer/{img}.png')

    if not new_lines:
        return existing_content
    return existing_content.rstrip() + '\n' + '\n'.join(new_lines) + '\n'


def ensure_includes(content: str) -> str:
    """Inject missing --8<-- include lines before the reference block."""
    missing = [inc for inc in INCLUDES if inc not in content]
    if not missing:
        return content
    inject = '\n'.join(missing) + '\n\n'
    ref_m = re.search(r'^\[[^\]]+\]:', content, re.MULTILINE)
    if ref_m:
        return content[:ref_m.start()] + inject + content[ref_m.start():]
    return content.rstrip() + '\n\n' + inject


# ---------------------------------------------------------------------------
# File update logic
# ---------------------------------------------------------------------------

def update_file(filepath: Path, location_blocks: dict, is_rematches: bool = False, dry_run: bool = False):
    if not filepath.exists():
        print(f"  [SKIP] File not found: {filepath}")
        return

    content = filepath.read_text(encoding='utf-8')

    all_blocks = []
    for blocks in location_blocks.values():
        all_blocks.extend(blocks)

    if not all_blocks:
        print(f"  [SKIP] No trainer blocks for {filepath.name}")
        return

    new_trainer_md = generate_location_section(all_blocks)
    if not new_trainer_md.strip():
        print(f"  [SKIP] Empty trainer section generated for {filepath.name}")
        return

    if is_rematches:
        content = _replace_rematches_section(content, new_trainer_md)
    else:
        has_trainers_header = bool(re.search(r'^## Trainers\s*$', content, re.MULTILINE))
        if has_trainers_header:
            content = _replace_trainers_section(content, new_trainer_md)
        else:
            content = _replace_gym_trainers(content, new_trainer_md, all_blocks)

    content = merge_refs(content, all_blocks)
    content = ensure_includes(content)

    if dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN: {filepath}")
        print('='*60)
        print(content[:3000])
        if len(content) > 3000:
            print(f"... [{len(content) - 3000} more chars]")
        return

    filepath.write_text(content, encoding='utf-8')
    print(f"  [UPDATED] {filepath}")


def _replace_trainers_section(content: str, new_md: str) -> str:
    """Replace content inside ## Trainers, preserving ### subsections."""
    m = re.search(r'^## Trainers\s*\n', content, re.MULTILINE)
    if not m:
        wild_m = re.search(r'^## Wild', content, re.MULTILINE)
        if wild_m:
            insert = wild_m.start()
            return content[:insert] + '## Trainers\n\n' + new_md + '\n\n' + content[insert:]
        return content

    section_start = m.end()
    next_h2 = re.search(r'^## ', content[section_start:], re.MULTILINE)
    section_end = section_start + next_h2.start() if next_h2 else len(content)
    section_body = content[section_start:section_end]

    # Preserve ### subsections (Rematches, Master Trainer)
    sub_m = re.search(r'^### ', section_body, re.MULTILINE)
    if sub_m:
        keep_tail = section_body[sub_m.start():]
        new_body = new_md + '\n\n' + keep_tail
    else:
        new_body = new_md + '\n\n'

    return content[:section_start] + new_body + content[section_end:]


def _replace_rematches_section(content: str, new_md: str) -> str:
    """Replace or create the ### Rematches subsection."""
    rematch_m = re.search(r'^### Rematches\s*\n', content, re.MULTILINE)

    if rematch_m:
        section_start = rematch_m.end()
        # End at next ### or ## header
        next_section = re.search(r'^#{2,3} ', content[section_start:], re.MULTILINE)
        section_end = section_start + next_section.start() if next_section else len(content)
        return content[:section_start] + new_md + '\n\n' + content[section_end:]

    # No ### Rematches yet — append inside ## Trainers before the next ## header
    trainers_m = re.search(r'^## Trainers\s*\n', content, re.MULTILINE)
    if trainers_m:
        section_start = trainers_m.end()
        next_h2 = re.search(r'^## ', content[section_start:], re.MULTILINE)
        insert_pos = section_start + next_h2.start() if next_h2 else len(content)
    else:
        insert_pos = len(content)

    rematches_block = '### Rematches\n\n' + new_md + '\n\n'
    return content[:insert_pos] + rematches_block + content[insert_pos:]


def _replace_gym_trainers(content: str, new_md: str, all_blocks: list) -> str:
    """Update gym file: replace pre-boss trainer table and ## Leader section."""
    regular_blocks = [b for b in all_blocks if not is_boss(b['trainer_name'])]
    boss_blocks    = [b for b in all_blocks if is_boss(b['trainer_name'])]

    first_h2 = re.search(r'^## ', content, re.MULTILINE)

    if boss_blocks and regular_blocks:
        regular_md = _regular_table([b for b in regular_blocks if not b['alt_name']])
        leader_m = re.search(r'^## (?:Leader|Boss|Gym Leader) .+\n', content, re.MULTILINE)

        if leader_m:
            after_leader_start = leader_m.end()
            end_m = re.search(r'^(## |--8<--)', content[after_leader_start:], re.MULTILINE)
            leader_content_end = after_leader_start + end_m.start() if end_m else len(content)
            rest = content[leader_content_end:]

            boss_sections = [_boss_table(boss) for boss in boss_blocks]
            return (
                regular_md + '\n\n'
                + leader_m.group(0)
                + '\n'.join(boss_sections) + '\n\n'
                + rest
            )
        else:
            return regular_md + '\n\n' + content

    elif boss_blocks:
        boss_md = '\n\n'.join(_boss_table(boss) for boss in boss_blocks)
        if first_h2:
            return boss_md + '\n\n' + content[first_h2.start():]
        return boss_md + '\n\n' + content

    else:
        regular_md = _regular_table([b for b in regular_blocks if not b['alt_name']])
        if first_h2:
            return regular_md + '\n\n' + content[first_h2.start():]
        return regular_md + '\n\n' + content


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    args = [a for a in args if not a.startswith('--')]

    if not args:
        print(f'Usage: {sys.argv[0]} <CSV_FILE> [--dry-run]')
        sys.exit(1)

    csv_path = Path(args[0])
    if not csv_path.exists():
        print(f'Error: {csv_path} not found')
        sys.exit(1)

    is_rematches = 'REMATCHES' in csv_path.name.upper()

    print(f'Parsing {csv_path.name}{"  [REMATCHES mode]" if is_rematches else ""}...')
    location_data = parse_csv(csv_path)

    file_to_locations = defaultdict(dict)
    for loc_key, blocks in location_data.items():
        if not blocks:
            continue
        stem = LOCATION_MAP.get(loc_key)
        if not stem:
            print(f'  [WARN] No file mapping for location: {repr(loc_key)}')
            continue
        file_to_locations[stem][loc_key] = blocks

    for stem, loc_map in sorted(file_to_locations.items()):
        filepath = DOCS / f'{stem}.md'
        total_trainers = sum(len(b) for b in loc_map.values())
        print(f'\nProcessing {filepath.name} ({total_trainers} trainer blocks)...')
        for loc, blocks in loc_map.items():
            print(f'  Location: {loc!r} → {len(blocks)} blocks')
        update_file(filepath, loc_map, is_rematches=is_rematches, dry_run=dry_run)

    print('\nDone.')


if __name__ == '__main__':
    main()
