#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

# Licensed under the GNU GPLv3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from itertools import repeat
from typing import List
import subprocess

from pathos.multiprocessing import ProcessPool as Pool

from utils import get_github_api_result_page
import config_reader


CONFIG = config_reader.load_config()


def get_org_repo_metadata(org, api_key=None) -> List[dict]:
    url = f"https://api.github.com/orgs/{org}/repos"
    json_response = []
    page = 1
    per_page = 30
    while True:
        has_next_page = False
        result_page = get_github_api_result_page(url, api_key=api_key, page=page, per_page=per_page)
        links = result_page.headers["Link"].split(",")
        for link in links:
            if "rel=\"next\"" in link:
                page += 1
                has_next_page = True
                break
        json_response += result_page.json()
        if not has_next_page:
            break
    return json_response


def filter_data_by_key(data: List[dict], key_string: str, key_value: str) -> List[dict]:
    return [item for item in data if key_string in item and item[key_string].startswith(key_value)]


def extract_repo_urls(data: List[dict]) -> List[str]:
    return [item["clone_url"] for item in data]


def pre_clone(path_to_clone_assignment_repos: str):
    subprocess.run(f"rm -rf {path_to_clone_assignment_repos}", shell=True)
    subprocess.run(f"mkdir -p {path_to_clone_assignment_repos}", shell=True)


def clone_parallel(urls: List[str], path_to_clone_assignment_repos: str):
    # Run git clone in parallel
    paths = list(repeat(path_to_clone_assignment_repos, len(urls)))
    with Pool() as pool:
        pool.map(clone, urls, paths)


def clone(url: str, path_to_clone_assignment_repos: str):
    command = f"cd {path_to_clone_assignment_repos} && git clone {url}"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    print("Making GitHub API requests... (this may take a while)")
    org_repo_metadata = get_org_repo_metadata(CONFIG["github_org"], CONFIG["github_api_key"])
    print("Making GitHub requests done.")

    print("Filtering repos...")
    filtered_repos = org_repo_metadata.copy()
    search_filters = {
        "created_at": CONFIG["assignment_date_filter"],
        "name": CONFIG["assignment_prefix"]
    }
    for filter_key in search_filters:
        filtered_repos = filter_data_by_key(filtered_repos, filter_key, search_filters[filter_key])
    print("Filtering repos done.")

    print("Extracting repo URLs...")
    repo_urls = extract_repo_urls(filtered_repos)
    print("Repo URLs extraction done.")

    print("Configuring directory for cloning...")
    pre_clone(CONFIG["path_to_clone_assignment_repos"])
    print("Configuring done.")

    print("Beginning clone...")
    clone_parallel(repo_urls, CONFIG["path_to_clone_assignment_repos"])
    print("All done.")
