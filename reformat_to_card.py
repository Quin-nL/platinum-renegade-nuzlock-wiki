#!/usr/bin/env python3
"""
Reformat transposed trainer tables from multi-row format to card format.

Current format:
  trainer | pokemon1 | pokemon2 | ...
  --- | --- | --- | ...
  **Item** | item1 | item2 | ...
  **Nature** | nature1 | nature2 | ...
  **Ability** | ability1 | ability2 | ...
  **Moves** | moves1 | moves2 | ...

Target format:
  trainer | pokemon1<br>item1<br>nature1 / ability1<hr>moves1 | pokemon2<br>... | ...
  --- | --- | --- | ...
"""

import re
import sys
from pathlib import Path

TRAINER_CHANGES_DIR = Path(__file__).parent / "docs" / "trainer_changes"
SKIP_FILES = {"pokemon_league.md"}


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [c.strip() for c in stripped.split("|")]


def is_separator(line: str) -> bool:
    return bool(re.match(r"^\s*-+\s*(\|\s*-+\s*)+\|?\s*$", line))


def get_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def reformat_file(path: Path) -> bool:
    text = path.read_text()
    lines = text.splitlines(keepends=True)

    output = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        stripped_content = line.rstrip("\n").strip()
        indent = get_indent(line.rstrip("\n"))

        if "|" in stripped_content and i + 5 < len(lines):
            if is_separator(lines[i + 1]):
                item_cells = split_row(lines[i + 2].strip())
                nature_cells = split_row(lines[i + 3].strip())
                ability_cells = split_row(lines[i + 4].strip())
                moves_cells = split_row(lines[i + 5].strip())

                if (
                    item_cells and item_cells[0] == "**Item**"
                    and nature_cells and nature_cells[0] == "**Nature**"
                    and ability_cells and ability_cells[0] == "**Ability**"
                    and moves_cells and moves_cells[0] == "**Moves**"
                ):
                    header_cells = split_row(stripped_content)
                    n = len(header_cells)

                    new_cells = [header_cells[0]]
                    for j in range(1, n):
                        pokemon = header_cells[j]
                        item = item_cells[j] if j < len(item_cells) else "&nbsp;"
                        nature = nature_cells[j] if j < len(nature_cells) else "?"
                        ability = ability_cells[j] if j < len(ability_cells) else "?"
                        moves = moves_cells[j] if j < len(moves_cells) else ""

                        combined = f"{pokemon}<br>{item}<br>{nature} / {ability}<hr>{moves}"
                        new_cells.append(combined)

                    output.append(indent + " | ".join(new_cells) + "\n")
                    output.append(indent + " | ".join(["---"] * n) + "\n")
                    i += 6
                    changed = True
                    continue

        output.append(line)
        i += 1

    if changed:
        path.write_text("".join(output))

    return changed


def main():
    files = sorted(TRAINER_CHANGES_DIR.glob("*.md"))
    total = 0
    for path in files:
        if path.name in SKIP_FILES:
            print(f"  skip  {path.name}")
            continue
        if reformat_file(path):
            print(f"changed {path.name}")
            total += 1
        else:
            print(f"  same  {path.name}")
    print(f"\n{total} file(s) changed.")


if __name__ == "__main__":
    main()
