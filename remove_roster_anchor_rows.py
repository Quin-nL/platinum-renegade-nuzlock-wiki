#!/usr/bin/env python3
"""
Remove roster table rows where the trainer has a dedicated card section.

These rows are identified by their first cell starting with a reference-style
text link: [Name]<br>![][sprite]. Regular trainers use plain text names.
The trainer with a card section appears in the roster without moves (redundant)
since the card section below covers their full detail.
"""

import re
from pathlib import Path

AREA_CHANGES_DIR = Path(__file__).parent / "docs" / "area_changes"


def is_separator(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*-+\s*(\|\s*-+\s*)+\|?\s*$", line))


def first_cell(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    return stripped.split("|")[0].strip()


def is_anchor_row(line: str) -> bool:
    """Return True if this roster row's trainer cell is a reference text link [Name]..."""
    stripped = line.strip()
    if not "|" in stripped or is_separator(stripped):
        return False
    cell = first_cell(stripped)
    # Starts with [ but NOT with ![ (which would be an image)
    return cell.startswith("[") and not cell.startswith("[!")


def reformat_file(path: Path) -> bool:
    text = path.read_text()
    lines = text.splitlines(keepends=True)

    output = []
    changed = False

    for line in lines:
        if is_anchor_row(line):
            changed = True
            continue
        output.append(line)

    if changed:
        path.write_text("".join(output))

    return changed


def main():
    files = sorted(AREA_CHANGES_DIR.glob("*.md"))
    total = 0
    for path in files:
        if reformat_file(path):
            print(f"changed {path.name}")
            total += 1
        else:
            print(f"  same  {path.name}")
    print(f"\n{total} file(s) changed.")


if __name__ == "__main__":
    main()
