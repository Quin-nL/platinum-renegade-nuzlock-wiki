import json
import re
from os.path import isfile

_name_cache = {}


def _get_id_from_url(url):
    return int(re.search(r"/(\d+)/$", url).group(1))


def _prettify(name):
    return " ".join(w.capitalize() for w in name.split("-"))


def _get_name(species_id):
    if species_id not in _name_cache:
        path = f"temp/species/{species_id}.json"
        if isfile(path):
            with open(path) as f:
                data = json.load(f)
            for entry in data.get("names", []):
                if entry["language"]["name"] == "en":
                    _name_cache[species_id] = entry["name"]
                    break
            else:
                _name_cache[species_id] = _prettify(data["name"])
    return _name_cache.get(species_id, f"#{species_id:03}")


def _describe_evolution(details):
    trigger = details["trigger"]["name"]

    if trigger == "shed":
        return "Lv. 20 (empty party slot + Poké Ball)"

    parts = []

    if trigger == "trade":
        if details["held_item"]:
            parts.append(f"Trade holding {_prettify(details['held_item']['name'])}")
        elif details["trade_species"]:
            parts.append(f"Trade for {_prettify(details['trade_species']['name'])}")
        else:
            parts.append("Trade")

    elif trigger == "use-item":
        parts.append(f"Use {_prettify(details['item']['name'])}")

    elif trigger == "level-up":
        if details["min_level"]:
            parts.append(f"Lv. {details['min_level']}")
        elif details["min_happiness"]:
            parts.append("Level up (high happiness)")
        else:
            parts.append("Level up")

        if details["held_item"]:
            parts.append(f"holding {_prettify(details['held_item']['name'])}")
        if details["known_move"]:
            parts.append(f"knowing {_prettify(details['known_move']['name'])}")
        if details["known_move_type"]:
            parts.append(f"knowing a {_prettify(details['known_move_type']['name'])}-type move")
        if details["location"]:
            parts.append(f"at {_prettify(details['location']['name'])}")
        if details["time_of_day"] in ("day", "night"):
            parts.append(f"({details['time_of_day']})")
        if details["gender"] == 1:
            parts.append("(female only)")
        elif details["gender"] == 2:
            parts.append("(male only)")
        if details["relative_physical_stats"] == 1:
            parts.append("(Atk > Def)")
        elif details["relative_physical_stats"] == -1:
            parts.append("(Atk < Def)")
        elif details["relative_physical_stats"] == 0:
            parts.append("(Atk = Def)")

    elif trigger == "other":
        parts.append("Special")

    return " ".join(parts)


def _flatten_chain(node):
    from_id = _get_id_from_url(node["species"]["url"])
    from_name = _get_name(from_id)

    for child in node["evolves_to"]:
        to_id = _get_id_from_url(child["species"]["url"])
        to_name = _get_name(to_id)
        for details in child["evolution_details"]:
            yield (from_name, to_name, _describe_evolution(details))
        yield from _flatten_chain(child)


def get_evolution_table(id):
    species_path = f"temp/species/{id}.json"
    if not isfile(species_path):
        return None

    with open(species_path) as f:
        species = json.load(f)

    chain_id = _get_id_from_url(species["evolution_chain"]["url"])
    chain_path = f"temp/evolution/{chain_id}.json"
    if not isfile(chain_path):
        return None

    with open(chain_path) as f:
        chain_data = json.load(f)

    rows = list(_flatten_chain(chain_data["chain"]))
    if not rows:
        return None

    lines = [
        "Evolves from | Method                                | Evolves to\n",
        "---          | ---                                   | ---\n",
    ]
    for from_name, to_name, condition in rows:
        lines.append(f"[{from_name}] | {condition} | [{to_name}]\n")

    return "".join(lines)


if __name__ == "__main__":
    import re
    import tqdm

    for id in tqdm.tqdm(range(1, 494)):
        md_path = f"docs/pokemons/{id:03}.md"
        if not isfile(md_path):
            continue

        with open(md_path) as f:
            content = f.read()

        # Match existing evolution section content (between ## Evolution and next ##)
        m = re.search(r'\n## Evolution\n(.*?)(?=\n## )', content, re.DOTALL)

        if m:
            section_content = m.group(1).strip()

            # Skip if already formatted with admonition
            if '!!! note' in section_content:
                continue

            if 'Evolves from' in section_content:
                # Already a vanilla table — no RP note, nothing to change
                continue

            # Bare RP note: wrap in admonition and append vanilla table
            indented = '\n'.join('    ' + line for line in section_content.split('\n'))
            admonition = f'!!! note "Renegade Platinum Changes"\n{indented}'
            table = get_evolution_table(id)
            new_content = f'{admonition}\n\n{table}' if table else admonition
            updated = content[:m.start(1)] + new_content + '\n' + content[m.end(1):]
        else:
            # No evolution section yet — insert vanilla table before ## Ability
            table = get_evolution_table(id)
            if table is None:
                continue
            section = f"## Evolution\n\n{table}"
            updated = content.replace("\n\n## Ability\n", f"\n\n{section}\n## Ability\n", 1)

        if updated == content:
            print(f"WARNING: could not find insertion point in {md_path}")
            continue

        with open(md_path, "w") as f:
            f.write(updated)
