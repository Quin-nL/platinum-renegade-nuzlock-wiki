"""
Transpose trainer detail tables from vertical (each Pokémon = row) to horizontal
(each Pokémon = column).

Before:
    ![][roark]   | Item       | Nature | Ability | Moves
    ---          | ---        | ---    | ---     | ---
    ![][299]...  | Smooth Rock | Modest | Sturdy  | <ul>...</ul>
    ![][438]...  | Rindo Berry | Impish | Rock Head | <ul>...</ul>

After:
    ![][roark]   | ![][299]... | ![][438]... | ...
    ---          | ---         | ---         | ---
    **Item**     | Smooth Rock | Rindo Berry | ...
    **Nature**   | Modest      | Impish      | ...
    **Ability**  | Sturdy      | Rock Head   | ...
    **Moves**    | <ul>...</ul>| <ul>...</ul>| ...
"""

import re
from pathlib import Path


def split_row(line: str) -> list[str]:
    """Split a markdown table row into cells, stripping outer pipes and whitespace."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [c.strip() for c in stripped.split("|")]


def is_detail_header(cells: list[str]) -> bool:
    """Return True if this row is a detail table header (has Item/Nature/Ability/Moves)."""
    labels = {c.strip() for c in cells}
    return {"Item", "Nature", "Ability", "Moves"}.issubset(labels)


def is_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*-+\s*(\|\s*-+\s*)+\|?\s*$", line))


def is_table_row(line: str) -> bool:
    return "|" in line and not is_separator(line)


def get_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def transpose_block(indent: str, header_cells: list[str], data_rows: list[list[str]]) -> list[str]:
    """
    header_cells: [trainer_sprite, 'Item', 'Nature', 'Ability', 'Moves']
    data_rows: list of [pokemon, item, nature, ability, moves] per Pokémon
    Returns new table lines (without trailing newline).
    """
    trainer_sprite = header_cells[0]

    idx = {label: i for i, label in enumerate(header_cells)}
    pokemon_col = 0

    pokemons  = [row[pokemon_col]       for row in data_rows]
    items     = [row[idx["Item"]]       for row in data_rows]
    natures   = [row[idx["Nature"]]     for row in data_rows]
    abilities = [row[idx["Ability"]]    for row in data_rows]
    moves     = [row[idx["Moves"]]      for row in data_rows]

    n = len(data_rows)

    def make_row(label: str, values: list[str]) -> str:
        return indent + " | ".join([label] + values)

    lines = []
    lines.append(indent + " | ".join([trainer_sprite] + pokemons))
    lines.append(indent + " | ".join(["---"] * (n + 1)))
    lines.append(make_row("**Item**",    items))
    lines.append(make_row("**Nature**",  natures))
    lines.append(make_row("**Ability**", abilities))
    lines.append(make_row("**Moves**",   moves))

    return lines


def transform_file(path: Path) -> bool:
    """Transform a single file. Returns True if any changes were made."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    result = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip("\n")

        if "|" in stripped and not is_separator(stripped):
            cells = split_row(stripped)
            if is_detail_header(cells):
                indent = get_indent(stripped)

                if i + 1 < len(lines) and is_separator(lines[i + 1]):
                    data_rows = []
                    j = i + 2
                    while j < len(lines):
                        candidate = lines[j].rstrip("\n")
                        cand_indent = get_indent(candidate)
                        if (
                            is_table_row(candidate)
                            and cand_indent == indent
                            and "|" in candidate
                        ):
                            row_cells = split_row(candidate)
                            while len(row_cells) < len(cells):
                                row_cells.append("")
                            data_rows.append(row_cells)
                            j += 1
                        else:
                            break

                    if data_rows:
                        new_lines = transpose_block(indent, cells, data_rows)
                        for nl in new_lines:
                            result.append(nl + "\n")
                        i = j
                        changed = True
                        continue

        result.append(line)
        i += 1

    if changed:
        path.write_text("".join(result), encoding="utf-8")
    return changed


def main():
    base = Path(__file__).parent / "docs" / "trainer_changes"
    skip = {"pokemon_league.md"}

    files = sorted(base.glob("*.md"))
    total_changed = 0
    for f in files:
        if f.name in skip:
            print(f"  skip  {f.name}")
            continue
        changed = transform_file(f)
        status = "changed" if changed else "  same "
        print(f"  {status} {f.name}")
        if changed:
            total_changed += 1

    print(f"\n{total_changed} file(s) changed.")


if __name__ == "__main__":
    main()
