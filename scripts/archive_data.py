"""
This file is used to fetch data from TibSchol via API and save it as JSON files.
"""

import json
import logging
import os
import sys

import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm

API_USER = os.getenv("TIBSCHOL_API_USERNAME", "")
API_PASS = os.getenv("TIBSCHOL_API_PASSWORD", "")

API_BASE_URL = "https://tibschol.acdh-ch-dev.oeaw.ac.at/"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def fetch_data(endpoint, params=None):
    """Fetch data from the given API endpoint."""
    logging.debug("Fetching data from %s", endpoint)
    if not endpoint.startswith("http"):
        endpoint = f"{API_BASE_URL}{endpoint}"
    response = requests.get(
        endpoint, params=params, auth=HTTPBasicAuth(API_USER, API_PASS)
    )

    if response.status_code == 200:
        return response.json()

    logging.error("Error fetching data: %s from %s", response.status_code, response.url)
    return None


def is_relavant_list_endpoint(endpoint):
    return "apis_ontology" in endpoint and "apis_ontology.version" not in endpoint


def fetch_list_data(endpoint):
    """Fetch paginated list data from the given API endpoint."""
    all_data = []
    while True:
        data = fetch_data(endpoint)
        if data is None or "results" not in data or not data["results"]:
            break
        all_data.extend(data["results"])
        if "next" not in data or not data["next"]:
            break
        endpoint = data["next"]
    return all_data


# Function to save JSON data to file
def save_json(item, folder="data"):
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{item['url'].rstrip('/').split('/')[-1]}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2)

    logging.debug("Saved %s.", filename)


if __name__ == "__main__":
    # Check if envionment variables are set
    REQUIRED_VARS = ["TIBSCHOL_API_USERNAME", "TIBSCHOL_API_PASSWORD"]
    for var in REQUIRED_VARS:
        if not os.getenv(var, "").strip():
            logging.error("Please set %s in the environment.", var)
            sys.exit(1)

    logging.info("Fetching data from %s …", API_BASE_URL)
    # Fetch collections
    API_ROOT = "apis/api/"
    endpoints = fetch_data(API_ROOT)
    if endpoints is None:
        logging.error("Failed to fetch API endpoints from %s", API_ROOT)
        exit(1)
    relavant_endpoints = [
        endpoint for endpoint in endpoints.keys() if is_relavant_list_endpoint(endpoint)
    ]
    for list_endpoint in tqdm(relavant_endpoints):
        list_data = fetch_list_data(list_endpoint)
        for record in list_data:
            folder = f"data/{list_endpoint.replace(API_ROOT,'').replace('/', '_').replace('.','_')}"
            save_json(record, folder=folder)

        tqdm.write(f"Saved {len(list_data)} items from {list_endpoint}.")
    logging.info("All data from %s successfully fetched and stored.", API_BASE_URL)
