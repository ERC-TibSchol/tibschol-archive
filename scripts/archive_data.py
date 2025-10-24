"""
This file is used to fetch data from TibSchol via API and save it as JSON files.
"""

import json
import logging
import os
import sys
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.auth import HTTPBasicAuth
from tqdm import tqdm

API_USER = os.getenv("TIBSCHOL_API_USERNAME", "")
API_PASS = os.getenv("TIBSCHOL_API_PASSWORD", "")
API_BASE_URL = "https://tibschol.acdh-ch-dev.oeaw.ac.at/"

SELECTED_ENDPOINTS = {
    "apis/api/apis_ontology.place": f"{API_BASE_URL}apis/api/apis_ontology.place/",
    "apis/api/apis_ontology.zoteroentry": f"{API_BASE_URL}apis/api/apis_ontology.zoteroentry/",
    "apis/api/apis_ontology.person": f"{API_BASE_URL}apis/api/apis_ontology.person/",
    "apis/api/apis_ontology.work": f"{API_BASE_URL}apis/api/apis_ontology.work/",
    "apis/api/apis_ontology.instance": f"{API_BASE_URL}apis/api/apis_ontology.instance/",
    "apis/api/apis_ontology.excerpts": f"{API_BASE_URL}apis/api/apis_ontology.excerpts/",
    "apis/api/apis_ontology.subject": f"{API_BASE_URL}apis/api/apis_ontology.subject/",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def make_session():
    """Create a persistent session with retry strategy and timeouts."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.auth = HTTPBasicAuth(API_USER, API_PASS)
    session.headers.update({"Accept": "application/json"})
    return session


def fetch_data(session, endpoint, params=None):
    """Fetch data from a single API endpoint."""
    if not endpoint.startswith("http"):
        endpoint = f"{API_BASE_URL}{endpoint}"
    try:
        response = session.get(endpoint, params=params, timeout=(5, 60))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error("Error fetching %s: %s", endpoint, e)
        return None


def is_relevant_list_endpoint(endpoint):
    return "apis_ontology" in endpoint and "apis_ontology.version" not in endpoint


def fetch_list_data(session, endpoint):
    """Fetch paginated list data."""
    all_data = []
    while endpoint:
        data = fetch_data(session, endpoint)
        if not data or "results" not in data:
            break
        all_data.extend(data["results"])
        endpoint = data.get("next")
    return all_data


def save_json(item, folder_path=None):
    folder_path = Path("data") if folder_path is None else Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    filename = folder_path / f"{item['url'].rstrip('/').split('/')[-1]}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2)
    logging.debug("Saved %s", filename)


def main():
    for var in ("TIBSCHOL_API_USERNAME", "TIBSCHOL_API_PASSWORD"):
        if not os.getenv(var):
            logging.error("Please set %s in the environment.", var)
            sys.exit(1)

    logging.info("Fetching data from %s …", API_BASE_URL)

    session = make_session()

    relevant_endpoints = [
        e for e in SELECTED_ENDPOINTS.keys() if is_relevant_list_endpoint(e)
    ]

    for list_endpoint in tqdm(relevant_endpoints):
        list_data = fetch_list_data(session, SELECTED_ENDPOINTS[list_endpoint])
        folder = Path("data") / list_endpoint.replace("apis/api/", "").replace(
            "/", "_"
        ).replace(".", "_")
        for record in list_data:
            save_json(record, folder_path=folder)
        tqdm.write(f"Saved {len(list_data)} items from {list_endpoint}.")

    logging.info("All data from %s successfully fetched and stored.", API_BASE_URL)


if __name__ == "__main__":
    main()
