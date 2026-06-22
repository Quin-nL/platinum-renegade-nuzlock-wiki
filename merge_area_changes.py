#!/usr/bin/env python3
"""
Merge trainer_changes/ and wild_pokemon/ into a unified area_changes/ section.

Creates docs/area_changes/ with combined pages, updates pokemon page links,
and rewrites the nav in mkdocs.yml.
"""

import re
from pathlib import Path

REPO = Path(".")
DOCS = REPO / "docs"
T = DOCS / "trainer_changes"
W = DOCS / "wild_pokemon"
AREA = DOCS / "area_changes"

AREA.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_file(filepath):
    """Return (title, body_lines, include_lines, link_def_lines)."""
    text = filepath.read_text()
    lines = text.splitlines()

    title = None
    body_lines = []
    include_lines = []
    link_def_lines = []

    i = 0
    if i < len(lines) and lines[i].startswith("# "):
        title = lines[i][2:]
        i += 1

    # Skip blank lines after title
    while i < len(lines) and lines[i] == "":
        i += 1

    # Skip cross-reference !!! note block
    if i < len(lines) and lines[i].startswith("!!! note"):
        i += 1
        while i < len(lines) and (lines[i].startswith("    ") or lines[i] == ""):
            i += 1
        while i < len(lines) and lines[i] == "":
            i += 1

    for line in lines[i:]:
        if line.startswith("--8<--"):
            include_lines.append(line)
        elif re.match(r"^\[([^\]]*)\]:", line):
            link_def_lines.append(line)
        else:
            body_lines.append(line)

    while body_lines and body_lines[-1] == "":
        body_lines.pop()

    return title, body_lines, include_lines, link_def_lines


def demote_h2(body_lines):
    """Promote ## headings to ### so they nest under a new ## section."""
    return [("#" + line if re.match(r"^## ", line) else line) for line in body_lines]


def merge_link_defs(trainer_defs, wild_defs):
    """Merge and deduplicate link defs; trainer defs win on conflict."""
    seen = {}
    for line in trainer_defs + wild_defs:
        if not line.strip():
            continue
        m = re.match(r"^\[([^\]]*)\]:", line)
        if m:
            key = m.group(1)
            if key not in seen:
                seen[key] = line
    return sorted(seen.values())


def _rstrip(parts):
    while parts and parts[-1] == "":
        parts.pop()


# ---------------------------------------------------------------------------
# File writer
# ---------------------------------------------------------------------------

def assemble(title, sections, includes, link_defs):
    """
    sections: list of (heading_or_None, body_lines)
    If heading is given, wraps content with ## heading.
    """
    parts = [f"# {title}", ""]

    for heading, body in sections:
        if heading:
            parts.append(f"## {heading}")
            parts.append("")
        parts.extend(body)
        _rstrip(parts)
        parts.append("")

    _rstrip(parts)
    parts.append("")

    seen_incs = []
    for inc in includes:
        if inc not in seen_incs:
            seen_incs.append(inc)
            parts.append(inc)
            parts.append("")

    for link in link_defs:
        parts.append(link)

    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Page creation
# ---------------------------------------------------------------------------

def create_page(output_name, trainer_file, wild_entries):
    """
    wild_entries: list of (sub_title_or_None, wild_path)
      sub_title=None → single wild area, no sub-heading inside Wild Pokémon
      sub_title=str  → multiple wild sub-areas, each gets a ### sub-heading
    """
    output_path = AREA / output_name

    has_trainer = trainer_file is not None and trainer_file.exists()
    trainer_title, trainer_body, trainer_incs, trainer_links = (None, [], [], [])
    if has_trainer:
        trainer_title, trainer_body, trainer_incs, trainer_links = parse_file(trainer_file)

    wild_data = []  # (sub_title, wt, body, incs, links)
    for sub_title, wild_file in wild_entries:
        if wild_file.exists():
            wt, wb, wi, wl = parse_file(wild_file)
            wild_data.append((sub_title, wt, wb, wi, wl))

    has_wild = bool(wild_data)

    # Determine page title from sources
    if trainer_title:
        page_title = trainer_title
    elif wild_data:
        page_title = wild_data[0][1]  # first wild file's title
    else:
        page_title = output_name.removesuffix(".md").replace("_", " ")

    # Collect all link defs and includes
    all_wild_links = [l for _, _, _, _, links in wild_data for l in links]
    all_wild_incs = [inc for _, _, _, incs, _ in wild_data for inc in incs]
    all_link_defs = merge_link_defs(trainer_links, all_wild_links)
    all_incs = trainer_incs.copy()
    for inc in all_wild_incs:
        if inc not in all_incs:
            all_incs.append(inc)

    if has_trainer and has_wild:
        # Merged: ## Trainers + ## Wild Pokémon
        trainer_body_demoted = demote_h2(trainer_body)

        if len(wild_data) == 1 and wild_data[0][0] is None:
            # Single wild area, content goes straight under ## Wild Pokémon
            wild_body = wild_data[0][2]
        else:
            # Multiple wild sub-areas → ### sub-headings
            wild_body = []
            for sub_title, _, wb, _, _ in wild_data:
                wild_body.append(f"### {sub_title}")
                wild_body.append("")
                wild_body.extend(wb)
                _rstrip(wild_body)
                wild_body.append("")

        sections = [
            ("Trainers", trainer_body_demoted),
            ("Wild Pokémon", wild_body),
        ]

    elif has_trainer:
        sections = [(None, trainer_body)]

    elif has_wild:
        if len(wild_data) == 1:
            sections = [(None, wild_data[0][2])]
        else:
            combined = []
            for sub_title, _, wb, _, _ in wild_data:
                combined.append(f"## {sub_title}")
                combined.append("")
                combined.extend(wb)
                _rstrip(combined)
                combined.append("")
            sections = [(None, combined)]

    else:
        print(f"WARNING: no sources found for {output_name}")
        return

    output_path.write_text(assemble(page_title, sections, all_incs, all_link_defs))
    print(f"  {output_path.relative_to(REPO)}")


def create_general_changes():
    """Merge trainer_changes/general_changes.md + wild_pokemon/general_changes.md."""
    t_text = (T / "general_changes.md").read_text()
    w_text = (W / "general_changes.md").read_text()

    # Trainer file starts with ## General Changes (h2), not h1
    t_body = re.sub(r"^##\s+General Changes\s*\n", "", t_text).strip()
    # Wild file starts with # General Changes (h1)
    w_body = re.sub(r"^#\s+General Changes\s*\n", "", w_text).strip()

    content = (
        "# General Changes\n\n"
        "## Trainer Changes\n\n"
        f"{t_body}\n\n"
        "## Wild Pokémon Changes\n\n"
        f"{w_body}\n"
    )
    (AREA / "general_changes.md").write_text(content)
    print(f"  {(AREA / 'general_changes.md').relative_to(REPO)}")


# ---------------------------------------------------------------------------
# Pokemon page link updates
# ---------------------------------------------------------------------------

# Maps wild_pokemon filename stems to area_changes stems when they differ
WILD_REMAP = {
    "oreburgh_gate__1f": "oreburgh_gate",
    "oreburgh_gate__b1f": "oreburgh_gate",
    "oreburgh_mine__1f": "oreburgh_mine",
    "oreburgh_mine__b1f": "oreburgh_mine",
    "iron_island__outside": "iron_island",
    "iron_island__inside__1f,_b1f": "iron_island",
    "iron_island__inside__b2f,_b3f": "iron_island",
    "wayward_cave_(both)": "wayward_cave",
    "stark_mountain_(outside)": "stark_mountain__outside",
    "stark_mountain_(entrance)": "stark_mountain__entrance",
    "stark_mountain_(interior)": "stark_mountain__interior",
}


def update_pokemon_links():
    def replace(m):
        stem = m.group(1)
        new_stem = WILD_REMAP.get(stem, stem)
        return f"../../area_changes/{new_stem}/"

    updated = 0
    for md_file in sorted((DOCS / "pokemons").glob("*.md")):
        text = md_file.read_text()
        new_text = re.sub(r"\.\./\.\./wild_pokemon/([^/]+)/", replace, text)
        if new_text != text:
            md_file.write_text(new_text)
            updated += 1
    print(f"  Updated {updated} pokemon pages")


# ---------------------------------------------------------------------------
# mkdocs.yml nav update
# ---------------------------------------------------------------------------

# (nav_label, filename_in_area_changes/)
NAV_ENTRIES = [
    ("General Changes", "general_changes.md"),
    ("Twinleaf Town", "twinleaf_town.md"),
    ("Route 201", "route_201.md"),
    ("Lake Verity", "lake_verity.md"),
    ("Route 202", "route_202.md"),
    ("Jubilife City Trainer School", "jubilife_city_trainer_school.md"),
    ("Route 204 ~ South", "route_204__south.md"),
    ("Ravaged Path", "ravaged_path.md"),
    ("Route 203", "route_203.md"),
    ("Oreburgh Gate", "oreburgh_gate.md"),
    ("Oreburgh City", "oreburgh_city.md"),
    ("Oreburgh Mine", "oreburgh_mine.md"),
    ("💪Oreburgh Gym", "oreburgh_gym.md"),
    ("Jubilife City", "jubilife_city.md"),
    ("Route 204 ~ North", "route_204__north.md"),
    ("Floaroma Town", "floaroma_town.md"),
    ("Floaroma Meadow", "floaroma_meadow.md"),
    ("Valley Windworks", "valley_windworks.md"),
    ("Route 205 ~ South", "route_205__south.md"),
    ("Eterna Forest", "eterna_forest.md"),
    ("Eterna Forest (Outside)", "eterna_forest_(outside).md"),
    ("Old Chateau (All Rooms)", "old_chateau_(all_rooms).md"),
    ("Route 205 ~ North", "route_205__north.md"),
    ("Eterna City", "eterna_city.md"),
    ("Route 211 ~ West", "route_211__west.md"),
    ("Mt. Coronet ~ Route 211 Entrance", "mt_coronet__route_211_entrance.md"),
    ("Mt. Coronet ~ Tunnel to Route 211 Entrance", "mt_coronet__tunnel_to_route_211_entrance.md"),
    ("Mt. Coronet ~ B1F", "mt_coronet__b1f.md"),
    ("Mt. Coronet ~ Route 216 Entrance", "mt_coronet__route_216_entrance.md"),
    ("Route 216", "route_216.md"),
    ("Route 211 ~ East", "route_211__east.md"),
    ("Route 206", "route_206.md"),
    ("Wayward Cave", "wayward_cave.md"),
    ("Mt. Coronet ~ Route 207 Entrance", "mt_coronet__route_207_entrance.md"),
    ("Route 207", "route_207.md"),
    ("💪Eterna Gym", "eterna_gym.md"),
    ("Team Galactic Eterna Building", "team_galactic_eterna_building.md"),
    ("Route 208", "route_208.md"),
    ("💪Hearthome Gym", "hearthome_gym.md"),
    ("Route 212 ~ North", "route_212__north.md"),
    ("Trophy Garden", "trophy_garden.md"),
    ("Route 209", "route_209.md"),
    ("Lost Tower", "lost_tower.md"),
    ("Solaceon Ruins", "solaceon_ruins.md"),
    ("Route 210 ~ South", "route_210__south.md"),
    ("Route 215", "route_215.md"),
    ("💪Veilstone Gym", "veilstone_gym.md"),
    ("Veilstone City", "veilstone_city.md"),
    ("Route 214", "route_214.md"),
    ("Maniac Tunnel", "maniac_tunnel.md"),
    ("Seven Stars Restaurant", "seven_stars_restaurant.md"),
    ("Valor Lakefront", "valor_lakefront.md"),
    ("Route 213", "route_213.md"),
    ("Route 212 ~ South", "route_212__south.md"),
    ("Pastoria City", "pastoria_city.md"),
    ("💪Pastoria Gym", "pastoria_gym.md"),
    ("Great Marsh ~ Area 1/2", "great_marsh__area_1_2.md"),
    ("Great Marsh ~ Area 3/4", "great_marsh__area_3_4.md"),
    ("Great Marsh ~ Area 5/6", "great_marsh__area_5_6.md"),
    ("Route 210 ~ North", "route_210__north.md"),
    ("Celestic Town", "celestic_town.md"),
    ("Route 218", "route_218.md"),
    ("Fuego Ironworks", "fuego_ironworks.md"),
    ("Route 219", "route_219.md"),
    ("Route 220", "route_220.md"),
    ("Route 221", "route_221.md"),
    ("Pal Park", "pal_park.md"),
    ("Canalave City", "canalave_city.md"),
    ("Iron Island", "iron_island.md"),
    ("💪Canalave Gym", "canalave_gym.md"),
    ("Lake Valor", "lake_valor.md"),
    ("Route 217", "route_217.md"),
    ("Acuity Lakefront", "acuity_lakefront.md"),
    ("Snowpoint City", "snowpoint_city.md"),
    ("Snowpoint Temple", "snowpoint_temple.md"),
    ("Lake Acuity", "lake_acuity.md"),
    ("💪Snowpoint Gym", "snowpoint_gym.md"),
    ("Galactic HQ", "galactic_hq.md"),
    ("Mt. Coronet ~ 2F", "mt_coronet__2f.md"),
    ("Mt. Coronet ~ 3F", "mt_coronet__3f.md"),
    ("Mt. Coronet ~ Snow Area", "mt_coronet__snow_area.md"),
    ("Mt. Coronet ~ 4F", "mt_coronet__4f.md"),
    ("Mt. Coronet ~ Summit", "mt_coronet__summit.md"),
    ("Mt. Coronet ~ 5F", "mt_coronet__5f.md"),
    ("Mt. Coronet ~ 6F", "mt_coronet__6f.md"),
    ("Mt. Coronet ~ 7F", "mt_coronet__7f.md"),
    ("Spear Pillar", "spear_pillar.md"),
    ("Distortion World", "distortion_world.md"),
    ("Sendoff Spring", "sendoff_spring.md"),
    ("Turnback Cave", "turnback_cave.md"),
    ("Route 222", "route_222.md"),
    ("Sunyshore City", "sunyshore_city.md"),
    ("💪Sunyshore Gym", "sunyshore_gym.md"),
    ("Route 223", "route_223.md"),
    ("Victory Road", "victory_road.md"),
    ("Victory Road ~ East", "victory_road__east.md"),
    ("Victory Road ~ 1F", "victory_road__1f.md"),
    ("Victory Road ~ 2F", "victory_road__2f.md"),
    ("Victory Road ~ B1F", "victory_road__b1f.md"),
    ("Victory Road ~ 1F Back 1", "victory_road__1f_back_1.md"),
    ("Victory Road ~ 1F Back 2", "victory_road__1f_back_2.md"),
    ("Victory Road ~ 1F Back 3", "victory_road__1f_back_3.md"),
    ("Route 224", "route_224.md"),
    ("🥇Pokémon League", "pokemon_league.md"),
    ("Fight Area", "fight_area.md"),
    ("Route 225", "route_225.md"),
    ("Route 226", "route_226.md"),
    ("Route 227", "route_227.md"),
    ("Route 228", "route_228.md"),
    ("Route 229", "route_229.md"),
    ("Resort Area", "resort_area.md"),
    ("Route 230", "route_230.md"),
    ("Stark Mountain ~ Outside", "stark_mountain__outside.md"),
    ("Stark Mountain ~ Entrance", "stark_mountain__entrance.md"),
    ("Stark Mountain ~ Interior", "stark_mountain__interior.md"),
    ("Battleground", "battleground.md"),
    ("Battle Marathon Only", "battle_marathon_only.md"),
    ("Pokémon Center", "pokemon_center.md"),
]


def update_mkdocs_nav():
    mkdocs_file = REPO / "mkdocs.yml"
    text = mkdocs_file.read_text()
    lines = text.splitlines()

    # Find "    - Trainer Changes:" line
    start_line = next(
        (i for i, l in enumerate(lines) if l == "    - Trainer Changes:"), None
    )
    if start_line is None:
        print("  ERROR: could not find '    - Trainer Changes:' in mkdocs.yml")
        return

    # Find the next sibling nav item (same 4-space indent) after start
    end_line = next(
        (
            i
            for i in range(start_line + 1, len(lines))
            if lines[i].startswith("    - ") and not lines[i].startswith("        ")
            and "Trainer Changes" not in lines[i]
            and "Wild Pokémon" not in lines[i]
        ),
        None,
    )
    if end_line is None:
        print("  ERROR: could not find end of sections in mkdocs.yml")
        return

    new_nav = ["    - Area Changes:"]
    for nav_label, filename in NAV_ENTRIES:
        new_nav.append(f"        - {nav_label}: area_changes/{filename}")

    new_lines = lines[:start_line] + new_nav + lines[end_line:]
    mkdocs_file.write_text("\n".join(new_lines) + "\n")
    print(f"  mkdocs.yml (replaced lines {start_line}–{end_line - 1})")


# ---------------------------------------------------------------------------
# Page definitions: (output_name, trainer_file_or_None, wild_entries)
# wild_entries: [(sub_title_or_None, wild_path), ...]
# ---------------------------------------------------------------------------

PAGES = [
    ("twinleaf_town.md",    None,               [(None,                    W/"twinleaf_town.md")]),
    ("route_201.md",        T/"route_201.md",   [(None,                    W/"route_201.md")]),
    ("lake_verity.md",      T/"lake_verity.md", [(None,                    W/"lake_verity.md")]),
    ("route_202.md",        T/"route_202.md",   [(None,                    W/"route_202.md")]),
    ("jubilife_city_trainer_school.md", T/"jubilife_city_trainer_school.md", []),
    ("route_204__south.md", T/"route_204__south.md", [(None,               W/"route_204__south.md")]),
    ("ravaged_path.md",     None,               [(None,                    W/"ravaged_path.md")]),
    ("route_203.md",        T/"route_203.md",   [(None,                    W/"route_203.md")]),
    ("oreburgh_gate.md",    T/"oreburgh_gate.md", [
        ("1F",  W/"oreburgh_gate__1f.md"),
        ("B1F", W/"oreburgh_gate__b1f.md"),
    ]),
    ("oreburgh_city.md",    T/"oreburgh_city.md", []),
    ("oreburgh_mine.md",    T/"oreburgh_mine.md", [
        ("1F",  W/"oreburgh_mine__1f.md"),
        ("B1F", W/"oreburgh_mine__b1f.md"),
    ]),
    ("oreburgh_gym.md",     T/"oreburgh_gym.md", []),
    ("jubilife_city.md",    T/"jubilife_city.md", []),
    ("route_204__north.md", T/"route_204__north.md", [(None,               W/"route_204__north.md")]),
    ("floaroma_town.md",    T/"floaroma_town.md", []),
    ("floaroma_meadow.md",  T/"floaroma_meadow.md", [(None,                W/"floaroma_meadow.md")]),
    ("valley_windworks.md", T/"valley_windworks.md", [(None,               W/"valley_windworks.md")]),
    ("route_205__south.md", T/"route_205__south.md", [(None,               W/"route_205__south.md")]),
    ("eterna_forest.md",    T/"eterna_forest.md", [(None,                  W/"eterna_forest.md")]),
    ("eterna_forest_(outside).md", None,        [(None,                    W/"eterna_forest_(outside).md")]),
    ("old_chateau_(all_rooms).md", None,        [(None,                    W/"old_chateau_(all_rooms).md")]),
    ("route_205__north.md", T/"route_205__north.md", [(None,               W/"route_205__north.md")]),
    ("eterna_city.md",      None,               [(None,                    W/"eterna_city.md")]),
    ("route_211__west.md",  T/"route_211__west.md", [(None,                W/"route_211__west.md")]),
    ("mt_coronet__route_211_entrance.md", None, [(None,                    W/"mt_coronet__route_211_entrance.md")]),
    ("mt_coronet__tunnel_to_route_211_entrance.md",
                            T/"mt_coronet__tunnel_to_route_211_entrance.md",
                                                [(None,                    W/"mt_coronet__tunnel_to_route_211_entrance.md")]),
    ("mt_coronet__b1f.md",  None,               [(None,                    W/"mt_coronet__b1f.md")]),
    ("mt_coronet__route_216_entrance.md", None, [(None,                    W/"mt_coronet__route_216_entrance.md")]),
    ("route_216.md",        T/"route_216.md",   [(None,                    W/"route_216.md")]),
    ("route_211__east.md",  T/"route_211__east.md", [(None,                W/"route_211__east.md")]),
    ("route_206.md",        T/"route_206.md",   [(None,                    W/"route_206.md")]),
    ("wayward_cave.md",     T/"wayward_cave.md", [(None,                   W/"wayward_cave_(both).md")]),
    ("mt_coronet__route_207_entrance.md", None, [(None,                    W/"mt_coronet__route_207_entrance.md")]),
    ("route_207.md",        T/"route_207.md",   [(None,                    W/"route_207.md")]),
    ("eterna_gym.md",       T/"eterna_gym.md",  []),
    ("team_galactic_eterna_building.md", T/"team_galactic_eterna_building.md", []),
    ("route_208.md",        T/"route_208.md",   [(None,                    W/"route_208.md")]),
    ("hearthome_gym.md",    T/"hearthome_gym.md", []),
    ("route_212__north.md", T/"route_212__north.md", [(None,               W/"route_212__north.md")]),
    ("trophy_garden.md",    None,               [(None,                    W/"trophy_garden.md")]),
    ("route_209.md",        T/"route_209.md",   [(None,                    W/"route_209.md")]),
    ("lost_tower.md",       T/"lost_tower.md",  [(None,                    W/"lost_tower.md")]),
    ("solaceon_ruins.md",   T/"solaceon_ruins.md", [(None,                 W/"solaceon_ruins.md")]),
    ("route_210__south.md", T/"route_210__south.md", [(None,               W/"route_210__south.md")]),
    ("route_215.md",        T/"route_215.md",   [(None,                    W/"route_215.md")]),
    ("veilstone_gym.md",    T/"veilstone_gym.md", []),
    ("veilstone_city.md",   T/"veilstone_city.md", []),
    ("route_214.md",        T/"route_214.md",   [(None,                    W/"route_214.md")]),
    ("maniac_tunnel.md",    None,               [(None,                    W/"maniac_tunnel.md")]),
    ("seven_stars_restaurant.md", T/"seven_stars_restaurant.md", []),
    ("valor_lakefront.md",  None,               [(None,                    W/"valor_lakefront.md")]),
    ("route_213.md",        T/"route_213.md",   [(None,                    W/"route_213.md")]),
    ("route_212__south.md", T/"route_212__south.md", [(None,               W/"route_212__south.md")]),
    ("pastoria_city.md",    T/"pastoria_city.md", [(None,                  W/"pastoria_city.md")]),
    ("pastoria_gym.md",     T/"pastoria_gym.md", []),
    ("great_marsh__area_1_2.md", None,          [(None,                    W/"great_marsh__area_1_2.md")]),
    ("great_marsh__area_3_4.md", None,          [(None,                    W/"great_marsh__area_3_4.md")]),
    ("great_marsh__area_5_6.md", None,          [(None,                    W/"great_marsh__area_5_6.md")]),
    ("route_210__north.md", T/"route_210__north.md", [(None,               W/"route_210__north.md")]),
    ("celestic_town.md",    T/"celestic_town.md", [(None,                  W/"celestic_town.md")]),
    ("route_218.md",        T/"route_218.md",   [(None,                    W/"route_218.md")]),
    ("fuego_ironworks.md",  T/"fuego_ironworks.md", [(None,                W/"fuego_ironworks.md")]),
    ("route_219.md",        T/"route_219.md",   [(None,                    W/"route_219.md")]),
    ("route_220.md",        T/"route_220.md",   [(None,                    W/"route_220.md")]),
    ("route_221.md",        T/"route_221.md",   [(None,                    W/"route_221.md")]),
    ("pal_park.md",         T/"pal_park.md",    []),
    ("canalave_city.md",    T/"canalave_city.md", [(None,                  W/"canalave_city.md")]),
    ("iron_island.md",      T/"iron_island.md", [
        ("Outside",           W/"iron_island__outside.md"),
        ("Inside ~ 1F, B1F",  W/"iron_island__inside__1f,_b1f.md"),
        ("Inside ~ B2F, B3F", W/"iron_island__inside__b2f,_b3f.md"),
    ]),
    ("canalave_gym.md",     T/"canalave_gym.md", []),
    ("lake_valor.md",       T/"lake_valor.md",  [(None,                    W/"lake_valor.md")]),
    ("route_217.md",        T/"route_217.md",   [(None,                    W/"route_217.md")]),
    ("acuity_lakefront.md", None,               [(None,                    W/"acuity_lakefront.md")]),
    ("snowpoint_city.md",   T/"snowpoint_city.md", []),
    ("snowpoint_temple.md", None,               [(None,                    W/"snowpoint_temple.md")]),
    ("lake_acuity.md",      None,               [(None,                    W/"lake_acuity.md")]),
    ("snowpoint_gym.md",    T/"snowpoint_gym.md", []),
    ("galactic_hq.md",      T/"galactic_hq.md", []),
    ("mt_coronet__2f.md",   None,               [(None,                    W/"mt_coronet__2f.md")]),
    ("mt_coronet__3f.md",   T/"mt_coronet__3f.md", [(None,                 W/"mt_coronet__3f.md")]),
    ("mt_coronet__snow_area.md", None,          [(None,                    W/"mt_coronet__snow_area.md")]),
    ("mt_coronet__4f.md",   T/"mt_coronet__4f.md", [(None,                 W/"mt_coronet__4f.md")]),
    ("mt_coronet__summit.md", None,             [(None,                    W/"mt_coronet__summit.md")]),
    ("mt_coronet__5f.md",   None,               [(None,                    W/"mt_coronet__5f.md")]),
    ("mt_coronet__6f.md",   T/"mt_coronet__6f.md", [(None,                 W/"mt_coronet__6f.md")]),
    ("mt_coronet__7f.md",   T/"mt_coronet__7f.md", [(None,                 W/"mt_coronet__7f.md")]),
    ("spear_pillar.md",     T/"spear_pillar.md", []),
    ("distortion_world.md", T/"distortion_world.md", []),
    ("sendoff_spring.md",   T/"sendoff_spring.md", [(None,                 W/"sendoff_spring.md")]),
    ("turnback_cave.md",    None,               [(None,                    W/"turnback_cave.md")]),
    ("route_222.md",        T/"route_222.md",   [(None,                    W/"route_222.md")]),
    ("sunyshore_city.md",   T/"sunyshore_city.md", [(None,                 W/"sunyshore_city.md")]),
    ("sunyshore_gym.md",    T/"sunyshore_gym.md", []),
    ("route_223.md",        T/"route_223.md",   [(None,                    W/"route_223.md")]),
    ("victory_road.md",     T/"victory_road.md", []),
    ("victory_road__east.md", T/"victory_road__east.md", []),
    ("victory_road__1f.md", None,               [(None,                    W/"victory_road__1f.md")]),
    ("victory_road__2f.md", None,               [(None,                    W/"victory_road__2f.md")]),
    ("victory_road__b1f.md", None,              [(None,                    W/"victory_road__b1f.md")]),
    ("victory_road__1f_back_1.md", None,        [(None,                    W/"victory_road__1f_back_1.md")]),
    ("victory_road__1f_back_2.md", None,        [(None,                    W/"victory_road__1f_back_2.md")]),
    ("victory_road__1f_back_3.md", None,        [(None,                    W/"victory_road__1f_back_3.md")]),
    ("route_224.md",        T/"route_224.md",   [(None,                    W/"route_224.md")]),
    ("pokemon_league.md",   T/"pokemon_league.md", [(None,                 W/"pokemon_league.md")]),
    ("fight_area.md",       T/"fight_area.md",  []),
    ("route_225.md",        T/"route_225.md",   [(None,                    W/"route_225.md")]),
    ("route_226.md",        T/"route_226.md",   [(None,                    W/"route_226.md")]),
    ("route_227.md",        T/"route_227.md",   [(None,                    W/"route_227.md")]),
    ("route_228.md",        T/"route_228.md",   [(None,                    W/"route_228.md")]),
    ("route_229.md",        T/"route_229.md",   [(None,                    W/"route_229.md")]),
    ("resort_area.md",      None,               [(None,                    W/"resort_area.md")]),
    ("route_230.md",        T/"route_230.md",   [(None,                    W/"route_230.md")]),
    ("stark_mountain__outside.md",  T/"stark_mountain__outside.md",  [(None, W/"stark_mountain_(outside).md")]),
    ("stark_mountain__entrance.md", T/"stark_mountain__entrance.md", [(None, W/"stark_mountain_(entrance).md")]),
    ("stark_mountain__interior.md", T/"stark_mountain__interior.md", [(None, W/"stark_mountain_(interior).md")]),
    ("battleground.md",     T/"battleground.md", []),
    ("battle_marathon_only.md", T/"battle_marathon_only.md", []),
    ("pokemon_center.md",   T/"pokemon_center.md", []),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Creating area_changes pages...")
    create_general_changes()
    for page_args in PAGES:
        create_page(*page_args)

    print("\nUpdating pokemon page links...")
    update_pokemon_links()

    print("\nUpdating mkdocs.yml nav...")
    update_mkdocs_nav()

    print("\nDone. Old trainer_changes/ and wild_pokemon/ directories are kept as-is.")
    print("Review the output, then remove them if satisfied.")
