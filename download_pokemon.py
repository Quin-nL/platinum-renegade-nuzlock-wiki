
from concurrent.futures import ThreadPoolExecutor, as_completed
from genericpath import isfile
from os import makedirs
import json
import re
import time
import requests
import tqdm

MAX_WORKERS = 10

makedirs("temp/pokemon/", exist_ok=True)
makedirs("temp/ability/", exist_ok=True)
makedirs("temp/move/", exist_ok=True)
makedirs("temp/item/", exist_ok=True)
makedirs("temp/species/", exist_ok=True)
makedirs("temp/evolution/", exist_ok=True)

session = requests.Session()

def download(url, path):
    if isfile(path):
        return
    for attempt in range(5):
        response = session.get(url)
        if response.status_code == 200:
            with open(path, "wb") as fh:
                fh.write(response.content)
            return
        if response.status_code == 429:
            time.sleep(2 ** attempt)
        else:
            return

def download_range(desc, url_template, path_template, ids):
    tasks = [(url_template.format(i), path_template.format(i)) for i in ids]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download, url, path) for url, path in tasks}
        for _ in tqdm.tqdm(as_completed(futures), total=len(futures), desc=desc):
            pass

download_range("pokemon",  "https://pokeapi.co/api/v2/pokemon/{}",         "temp/pokemon/{}.json",  range(1, 494))
download_range("ability",  "https://pokeapi.co/api/v2/ability/{}",         "temp/ability/{}.json",  range(1, 234))
download_range("move",     "https://pokeapi.co/api/v2/move/{}",            "temp/move/{}.json",     range(1, 826))
download_range("item",     "https://pokeapi.co/api/v2/item/{}",            "temp/item/{}.json",     range(1, 1607))
download_range("species",  "https://pokeapi.co/api/v2/pokemon-species/{}", "temp/species/{}.json",  range(1, 494))

# Collect unique evolution chain IDs from downloaded species files
seen_chains = set()
chain_ids = []
for id in range(1, 494):
    path = f"temp/species/{id}.json"
    if not isfile(path):
        continue
    with open(path) as fh:
        chain_id = int(re.search(r"/(\d+)/$", json.load(fh)["evolution_chain"]["url"]).group(1))
    if chain_id not in seen_chains:
        seen_chains.add(chain_id)
        chain_ids.append(chain_id)

download_range("evolution", "https://pokeapi.co/api/v2/evolution-chain/{}", "temp/evolution/{}.json", chain_ids)
