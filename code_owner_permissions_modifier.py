#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

# Licensed under the GNU GPLv3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from time import sleep
import json
import sys

import requests

import config_reader


CONFIG = config_reader.load_config()


def modify_repository_collaborator(collaborator_permission: str, peer_mappings: dict, github_org: str, assignment_prefix: str, api_key=None) -> None:
    request_body_params = {"permission": collaborator_permission}
    request_headers = {"Authorization": f"Token {api_key}"}
    counter = 0

    print()

    for user in peer_mappings:
        print(user)
        print(f"\tEnabling {user:<24} to write", end="")
        modify_collaborator_url = f"https://api.github.com/repos/{github_org}/{assignment_prefix}{user}/collaborators/{user}"
        result = requests.put(modify_collaborator_url, json=request_body_params, headers=request_headers)
        status_code = result.status_code
        print(f" - [{status_code}]", end=" ")
        if status_code == 204:
            print("OK")
        elif status_code == 403:
            print("Resource Forbidden")
        elif status_code == 422:
            print("Validation Failed, or Endpoint Spammed")
        else:
            print(result)
        sleep(1)
        counter += 1
        print(counter, file=sys.stderr)
        print()



if __name__ == "__main__":
    print("Assigning peer reviews... (this may take a while)")
    with open(CONFIG["path_to_repo_mappings"], "r") as f1:
        repo_mappings = json.load(f1)
        modify_repository_collaborator(CONFIG["collaborator_permission"], repo_mappings, CONFIG["github_org"], CONFIG["assignment_prefix"], CONFIG["github_api_key"])
    print("Assigning peer reviews done.")
