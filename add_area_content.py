#!/usr/bin/env python3
"""
Add Items, TMs & HMs, and Pokémon Events sections to area_changes/*.md files.
Sources: docs/item_changes.md, docs/special_events.md
"""
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).parent
DOCS = REPO / "docs"
AREA_DIR = DOCS / "area_changes"
ITEM_IMGS = DOCS / "img" / "items"
PKMN_IMGS = DOCS / "img" / "pokemon"

# ============================================================
# AREA NAME → FILE STEM(S) MAPPING
# Keys are location strings as they appear in item_changes.md / special_events.md
# ============================================================
AREA_MAP = {
    # Cities
    "Oreburgh City": ["oreburgh_city"],
    "Oreburgh City Pokémon Center": ["oreburgh_city"],
    "Oreburgh Gate": ["oreburgh_gate"],
    "Oreburgh Mine": ["oreburgh_mine"],
    "Oreburgh Gym": ["oreburgh_gym"],
    "Jubilife City": ["jubilife_city"],
    "Jubilife City Trainer School": ["jubilife_city_trainer_school"],
    "Jubilife City Pokémon Center": ["jubilife_city"],
    "Floaroma Town": ["floaroma_town"],
    "Floaroma Town Pokémon Center": ["floaroma_town"],
    "Floaroma Meadow": ["floaroma_meadow"],
    "Eterna City": ["eterna_city"],
    "Eterna Forest": ["eterna_forest"],
    "Eterna Forest Outside": ["eterna_forest_(outside)"],
    "Eterna Forest (Outside)": ["eterna_forest_(outside)"],
    "Eterna Forest (Moss Rock)": ["eterna_forest"],
    "Eterna Galactic Building": ["team_galactic_eterna_building"],
    "Eterna Galactic Bldg": ["team_galactic_eterna_building"],
    "Galactic Eterna Building": ["team_galactic_eterna_building"],
    "Eterna Gym": ["eterna_gym"],
    "Celestic Town": ["celestic_town"],
    "Veilstone City": ["veilstone_city"],
    "Veilstone City Dept. Store": ["veilstone_city"],
    "Veilstone Dept. Store": ["veilstone_city"],
    "Veilstone Galactic HQ": ["galactic_hq"],
    "Galactic HQ": ["galactic_hq"],
    "Galactic Warehouse": ["galactic_hq"],
    "Veilstone Gym": ["veilstone_gym"],
    "Pastoria City": ["pastoria_city"],
    "Pastoria Gym": ["pastoria_gym"],
    "Canalave City": ["canalave_city"],
    "Canalave Gym": ["canalave_gym"],
    "Sunyshore City": ["sunyshore_city"],
    "Sunyshore Gym": ["sunyshore_gym"],
    "Snowpoint City": ["snowpoint_city"],
    "Snowpoint Temple": ["snowpoint_temple"],
    "Twinleaf Town": ["twinleaf_town"],
    "Sandgem Town": [],
    "Solaceon Town": [],
    "Solaceon Ruins": ["solaceon_ruins"],
    "Valley Windworks": ["valley_windworks"],
    "Fuego Ironworks": ["fuego_ironworks"],
    "Iron Island": ["iron_island"],
    "Iron Island (B3F)": ["iron_island"],
    "Pokémon League": ["pokemon_league"],
    "Pokemon League": ["pokemon_league"],
    "Fight Area": ["fight_area"],
    "Resort Area": ["resort_area"],
    "Survival Area": ["battleground"],
    "Survival Area - Battleground": ["battleground"],
    "Valor Lakefront": ["valor_lakefront"],
    "Acuity Lakefront": ["acuity_lakefront"],
    "Lake Acuity": ["lake_acuity"],
    "Lake Valor": ["lake_valor"],
    "Lake Verity": ["lake_verity"],
    "Acuity Cavern": ["lake_acuity"],
    "Valor Cavern": ["lake_valor"],
    "Verity Cavern": ["lake_verity"],
    "Lost Tower": ["lost_tower"],
    "Old Chateau": ["old_chateau_(all_rooms)"],
    "Wayward Cave": ["wayward_cave"],
    "Ravaged Path": ["ravaged_path"],
    "Maniac Tunnel": ["maniac_tunnel"],
    "Spear Pillar": ["spear_pillar"],
    "Hall of Origin": ["spear_pillar"],
    "Distortion World": ["distortion_world"],
    "Distortion World / Turnback Cave": ["distortion_world", "turnback_cave"],
    "Sendoff Spring": ["sendoff_spring"],
    "Turnback Cave": ["turnback_cave"],
    "Trophy Garden": ["trophy_garden"],
    "Pokémon Mansion": ["trophy_garden"],
    "Great Marsh": ["great_marsh__area_1_2", "great_marsh__area_3_4", "great_marsh__area_5_6"],
    "Mt. Coronet": [
        "mt_coronet__2f", "mt_coronet__3f", "mt_coronet__4f", "mt_coronet__5f",
        "mt_coronet__6f", "mt_coronet__7f", "mt_coronet__b1f", "mt_coronet__snow_area",
        "mt_coronet__summit",
    ],
    "Mt. Coronet (Route 207 entrance)": ["mt_coronet__route_207_entrance"],
    "Mt. Coronet (Route 211 entrance)": ["mt_coronet__route_211_entrance"],
    "Mt. Coronet (Route 216 Entrance)": ["mt_coronet__route_216_entrance"],
    "Mt. Coronet (B1F)": ["mt_coronet__b1f"],
    "Mt. Coronet (Summit)": ["mt_coronet__summit"],
    "Victory Road": [
        "victory_road", "victory_road__1f", "victory_road__2f", "victory_road__b1f",
        "victory_road__east", "victory_road__1f_back_1", "victory_road__1f_back_2",
        "victory_road__1f_back_3",
    ],
    "Game Corner": ["veilstone_city"],
    "Hotel Grand Lake (Route 213)": ["route_213"],
    "Pokémon Center": ["pokemon_center"],
    "Pokémon Center Basement": ["pokemon_center"],
    "Fullmoon Island": [],
    "Newmoon Island": [],
    "Flower Paradise": [],
    "Pal Park": ["pal_park"],
    "Stark Mountain": ["stark_mountain__interior"],
    "Stark Mountain (Interior)": ["stark_mountain__interior"],
    "Stark Mountain (Furthest Room - Interior)": ["stark_mountain__interior"],
    "Stark Mountain (Outside)": ["stark_mountain__outside"],
    "Amity Square": [],
    # Routes
    "Route 201": ["route_201"],
    "Route 202": ["route_202"],
    "Route 203": ["route_203"],
    "Route 204": ["route_204__north", "route_204__south"],
    "Route 204 (North)": ["route_204__north"],
    "Route 204 (South)": ["route_204__south"],
    "Route 205": ["route_205__north", "route_205__south"],
    "Route 205 (North)": ["route_205__north"],
    "Route 205 (South)": ["route_205__south"],
    "Route 206": ["route_206"],
    "Route 207": ["route_207"],
    "Route 208": ["route_208"],
    "Route 209": ["route_209"],
    "Route 210": ["route_210__north", "route_210__south"],
    "Route 210 (North)": ["route_210__north"],
    "Route 210 (South)": ["route_210__south"],
    "Route 211": ["route_211__east", "route_211__west"],
    "Route 211 (East)": ["route_211__east"],
    "Route 211 (West)": ["route_211__west"],
    "Route 212": ["route_212__north", "route_212__south"],
    "Route 212 (North)": ["route_212__north"],
    "Route 212 (South)": ["route_212__south"],
    "Route 213": ["route_213"],
    "Route 214": ["route_214"],
    "Route 215": ["route_215"],
    "Route 216": ["route_216"],
    "Route 217": ["route_217"],
    "Route 218": ["route_218"],
    "Route 219": ["route_219"],
    "Route 220": ["route_220"],
    "Route 221": ["route_221"],
    "Route 222": ["route_222"],
    "Route 223": ["route_223"],
    "Route 224": ["route_224"],
    "Route 225": ["route_225"],
    "Route 226": ["route_226"],
    "Route 227": ["route_227"],
    "Route 228": ["route_228"],
    "Route 229": ["route_229"],
    "Route 230": ["route_230"],
}

# ============================================================
# LOCATION PARSING
# ============================================================

def _try_map(key):
    return AREA_MAP.get(key, None)

def parse_location(raw):
    """
    Map a raw location string to (list_of_stems, note).
    Note may be 'Hidden', 'Buyable', 'Gift from X', etc. or None.
    Returns ([], None) if unmapped.
    """
    raw = raw.strip()

    # 1. Direct match
    result = _try_map(raw)
    if result is not None:
        return result, None

    # 2. Strip last parenthetical as a qualifier
    m = re.match(r'^(.*?)\s+\(([^)]+)\)$', raw)
    if m:
        base, qualifier = m.group(1).strip(), m.group(2).strip()
        result = _try_map(base)
        if result is not None:
            return result, qualifier

    # 3. Handle " - sublocation" suffix (e.g. "Celestic Town - Ruins")
    m = re.match(r'^(.*?)\s+-\s+(.+)$', raw)
    if m:
        base = m.group(1).strip()
        result = _try_map(base)
        if result is not None:
            return result, None

    return [], None


def split_locations(loc_str):
    """Split a comma-separated location string, respecting parentheses."""
    parts = []
    cur = ""
    depth = 0
    for ch in loc_str:
        if ch == '(':
            depth += 1
            cur += ch
        elif ch == ')':
            depth -= 1
            cur += ch
        elif ch == ',' and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


# ============================================================
# ITEM CHANGES PARSER
# ============================================================

def strip_footnotes(s):
    return re.sub(r'\s*\[\^[^\]]+\]', '', s).strip()


def strip_link_markup(s):
    """Turn '[Scald]' → 'Scald', '[Gift from NPC](## "...")' → 'Gift from NPC'."""
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]', r'\1', s)
    return s.strip()


def parse_icon(cell):
    """Extract icon name from '![][fire-stone]' or return None."""
    m = re.match(r'!\[\]\[([^\]]+)\]', cell.strip())
    return m.group(1) if m else None


def icon_exists(icon_name):
    return (ITEM_IMGS / f"{icon_name}.png").exists()


def parse_table_row(line):
    """Parse a markdown table row into cells (strips leading/trailing |)."""
    line = line.strip().lstrip('|').rstrip('|')
    return [c.strip() for c in line.split('|')]


def is_table_row(line):
    return line.strip().startswith('|') or ('|' in line and not line.strip().startswith('#'))


def is_separator(line):
    return re.match(r'^[\s|:-]+$', line.strip()) is not None


def parse_item_section(lines, section_name):
    """
    Parse a table from item_changes.md.
    Returns list of (icon_or_None, name, locations_str, obtained_or_None)
    """
    in_section = False
    in_table = False
    results = []
    for line in lines:
        if line.strip().startswith('## ') or line.strip().startswith('# '):
            if section_name in line:
                in_section = True
                in_table = False
                continue
            elif in_section:
                break
        if not in_section:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('---') and not in_table:
            in_table = True
            continue
        if '|' not in stripped:
            if in_table:
                break
            continue
        cells = parse_table_row(stripped)
        if len(cells) < 2:
            continue
        if is_separator(stripped):
            continue
        if cells[0].lower().replace(' ', '') in ('item', 'tm', '---', 'olditem'):
            continue
        results.append(cells)
    return results


# ---- Items (Item Locations) ----

def parse_items(filepath):
    """Returns dict[stem] = list of (icon, name, note)."""
    lines = filepath.read_text().splitlines()
    rows = parse_item_section(lines, "Item Locations")
    by_area = defaultdict(list)
    for cells in rows:
        if len(cells) < 3:
            continue
        icon = parse_icon(cells[0])
        name = cells[1].strip()
        loc_str = cells[2].strip()
        for loc in split_locations(loc_str):
            stems, note = parse_location(loc)
            for stem in stems:
                by_area[stem].append((icon, name, note))
    return by_area


# ---- TMs & HMs ----

def parse_tms(filepath):
    """Returns dict[stem] = list of (tm_num, name, obtained)."""
    lines = filepath.read_text().splitlines()
    rows = parse_item_section(lines, "TM Locations")
    by_area = defaultdict(list)
    for cells in rows:
        if len(cells) < 4:
            continue
        tm_num = cells[0].strip()
        if not re.match(r'^(TM|HM)\d+', tm_num):
            continue
        name = strip_link_markup(strip_footnotes(cells[1]))
        location = cells[2].strip()
        obtained = strip_link_markup(strip_footnotes(cells[3]))
        stems, _ = parse_location(location)
        for stem in stems:
            by_area[stem].append((tm_num, name, obtained))
    return by_area


# ---- Plates ----

def parse_plates(filepath):
    """Returns dict[stem] = list of (icon, name, 'Master Trainer')."""
    lines = filepath.read_text().splitlines()
    rows = parse_item_section(lines, "Plate Locations")
    by_area = defaultdict(list)
    for cells in rows:
        if len(cells) < 3:
            continue
        icon = parse_icon(cells[0])
        name = cells[1].strip()
        loc_str = cells[2].strip()
        # Location format: "Celestic Town - Ruins"
        stems, _ = parse_location(loc_str)
        for stem in stems:
            by_area[stem].append((icon, name, "Master Trainer"))
    return by_area


# ---- Key Items ----

def parse_key_items(filepath):
    """Returns dict[stem] = list of (icon, name, obtained)."""
    lines = filepath.read_text().splitlines()
    rows = parse_item_section(lines, "Key Items")
    by_area = defaultdict(list)
    for cells in rows:
        if len(cells) < 4:
            continue
        icon = parse_icon(cells[0])
        name = cells[1].strip()
        loc_str = cells[2].strip()
        obtained = strip_link_markup(strip_footnotes(cells[3]))
        stems, note = parse_location(loc_str)
        for stem in stems:
            final_note = note or obtained
            by_area[stem].append((icon, name, final_note))
    return by_area


# ============================================================
# SPECIAL EVENTS PARSER
# ============================================================

PKMN_CELL_RE = re.compile(r'!\[\]\[(\d+)\]<br>\[([^\]]+)\]')


def parse_pokemon_cells(cells):
    """Extract list of (num_str, name) from a row of cells."""
    result = []
    for cell in cells:
        cell = cell.strip()
        if cell in ('&nbsp;', '', 'Pokémon', 'Level', 'Location', 'Title'):
            continue
        m = PKMN_CELL_RE.match(cell)
        if m:
            result.append((m.group(1).zfill(3), m.group(2)))
    return result


def parse_events(filepath):
    """
    Returns dict[stem] = list of (num_str, name, level, event_type, note).
    num_str may be None for egg events.
    """
    text = filepath.read_text()
    lines = text.splitlines()
    by_area = defaultdict(list)

    event_type = "Gift"
    cur_title = None
    pkmn_list = []
    location = None
    level = None
    notes = []
    in_table = False

    def flush():
        nonlocal cur_title, pkmn_list, location, level, notes, in_table
        if not pkmn_list or not location:
            cur_title = pkmn_list = []
            location = level = None
            notes = []
            in_table = False
            return
        stems, _ = parse_location(location)
        note = notes[0] if notes else ""
        note = re.sub(r'\[[^\]]+\]', lambda m: m.group(0)[1:-1], note)  # strip link brackets
        note = note.strip('- ').strip()
        for stem in stems:
            for num, name in pkmn_list:
                by_area[stem].append((num, name, level or "?", event_type, note))
        cur_title = None
        pkmn_list = []
        location = None
        level = None
        notes = []
        in_table = False

    for line in lines:
        stripped = line.strip()

        # Section type headers
        if stripped == '## Gift Pokémon':
            flush()
            event_type = "Gift"
            continue
        if stripped == '## Special Encounters':
            flush()
            event_type = "Encounter"
            continue
        if stripped == '## Legendary Encounters':
            flush()
            event_type = "Legendary"
            continue

        # Event subsection
        if stripped.startswith('### '):
            flush()
            cur_title = stripped[4:].strip()
            continue

        if cur_title is None:
            continue

        # Table rows
        if '|' in stripped and not stripped.startswith('---'):
            cells = parse_table_row(stripped)
            if not cells:
                continue
            first = cells[0].strip()

            if first == 'Pokémon' or first == '&nbsp;':
                pkmn_list.extend(parse_pokemon_cells(cells[1:] if first == 'Pokémon' else cells))
                in_table = True
                continue

            if first == 'Location':
                # First non-&nbsp; value
                for c in cells[1:]:
                    c = c.strip()
                    if c and c != '&nbsp;':
                        location = c
                        break
                continue

            if first == 'Level':
                for c in cells[1:]:
                    c = c.strip()
                    if c and c != '&nbsp;':
                        level = c
                        break
                continue

            # Separator row or header row
            if is_separator(stripped) or first in ('Title', '---'):
                continue

        # Bullet points after table
        if stripped.startswith('- ') and in_table:
            notes.append(stripped[2:])

    flush()  # Final event
    return by_area


# ============================================================
# MARKDOWN GENERATION
# ============================================================

def make_items_section(items_list, key_items_list, plates_list):
    """items_list, key_items_list, plates_list each: list of (icon, name, note)."""
    all_items = list(items_list) + list(key_items_list) + list(plates_list)
    if not all_items:
        return "", []

    lines = ["## Items", "", "Item | Name | Obtained", "--- | --- | ---"]
    new_defs = []

    for icon, name, note in all_items:
        if icon and icon_exists(icon):
            cell = f"![][{icon}]"
            new_defs.append((icon, f"../img/items/{icon}.png"))
        else:
            cell = "&nbsp;"
        note_cell = note if note else "&nbsp;"
        lines.append(f"{cell} | {name} | {note_cell}")

    return "\n".join(lines) + "\n", new_defs


def make_tms_section(tms_list):
    if not tms_list:
        return ""
    lines = ["## TMs & HMs", "", "TM | Name | Obtained", "--- | --- | ---"]
    for tm_num, name, obtained in tms_list:
        lines.append(f"{tm_num} | {name} | {obtained}")
    return "\n".join(lines) + "\n"


def make_events_section(events_list):
    if not events_list:
        return "", []
    lines = ["## Pokémon Events", "", "Pokémon | Level | Type | Notes", "--- | --- | --- | ---"]
    new_defs = []

    for num, name, level, event_type, note in events_list:
        if num and (PKMN_IMGS / f"{num}.png").exists():
            pkmn_cell = f"![][{num}]<br>[{name}]"
            new_defs.append((num, f"../img/pokemon/{num}.png"))
            new_defs.append((name, f"../../pokemons/{int(num):03d}/"))
        else:
            pkmn_cell = name
        note_cell = note if note else "&nbsp;"
        lines.append(f"{pkmn_cell} | {level} | {event_type} | {note_cell}")

    return "\n".join(lines) + "\n", new_defs


# ============================================================
# FILE INJECTION
# ============================================================

LINK_DEF_RE = re.compile(r'^\[([^\]]+)\]:\s+\S')


def get_existing_defs(content):
    """Return set of already-defined link labels."""
    return {m.group(1) for line in content.splitlines()
            if (m := LINK_DEF_RE.match(line))}


def find_link_defs_start(lines):
    """Return index of the first link definition line."""
    for i, line in enumerate(lines):
        if LINK_DEF_RE.match(line):
            return i
    return len(lines)


def already_has_sections(content):
    return '## Items' in content or '## TMs & HMs' in content or '## Pokémon Events' in content


def inject_into_file(filepath, sections_md, new_link_defs):
    """Inject sections_md before link defs and append new link defs."""
    content = filepath.read_text()

    if already_has_sections(content):
        return False  # Already processed

    if not sections_md.strip():
        return False

    lines = content.splitlines(keepends=True)
    insert_at = find_link_defs_start([l.rstrip('\n') for l in lines])

    existing_defs = get_existing_defs(content)
    unique_defs = []
    seen = set()
    for label, url in new_link_defs:
        if label not in existing_defs and label not in seen:
            unique_defs.append(f"[{label}]: {url}")
            seen.add(label)

    # Build the inserted block
    insert_lines = ["\n"] + [s + "\n" for s in sections_md.rstrip().splitlines()] + ["\n"]

    new_lines = lines[:insert_at] + insert_lines + lines[insert_at:]

    if unique_defs:
        if new_lines and not new_lines[-1].endswith('\n'):
            new_lines[-1] += '\n'
        for d in unique_defs:
            new_lines.append(d + '\n')

    filepath.write_text("".join(new_lines))
    return True


# ============================================================
# MAIN
# ============================================================

def main():
    item_changes = DOCS / "item_changes.md"
    special_events = DOCS / "special_events.md"

    print("Parsing item_changes.md...")
    items_by_area = parse_items(item_changes)
    tms_by_area = parse_tms(item_changes)
    plates_by_area = parse_plates(item_changes)
    key_items_by_area = parse_key_items(item_changes)

    print("Parsing special_events.md...")
    events_by_area = parse_events(special_events)

    skip = {"general_changes"}
    area_files = sorted(AREA_DIR.glob("*.md"))

    updated = 0
    skipped = 0
    for path in area_files:
        stem = path.stem
        if stem in skip:
            continue

        items = items_by_area.get(stem, [])
        key_items = key_items_by_area.get(stem, [])
        plates = plates_by_area.get(stem, [])
        tms = tms_by_area.get(stem, [])
        events = events_by_area.get(stem, [])

        if not (items or key_items or plates or tms or events):
            skipped += 1
            continue

        items_md, items_defs = make_items_section(items, key_items, plates)
        tms_md = make_tms_section(tms)
        events_md, events_defs = make_events_section(events)

        all_sections = "\n\n".join(filter(None, [items_md.rstrip(), tms_md.rstrip(), events_md.rstrip()]))
        all_defs = items_defs + events_defs

        if inject_into_file(path, all_sections, all_defs):
            print(f"  Updated: {stem}")
            updated += 1
        else:
            skipped += 1

    print(f"\nDone. Updated {updated} files, skipped {skipped}.")


if __name__ == "__main__":
    main()
