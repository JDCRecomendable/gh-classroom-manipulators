#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

# Licensed under the GNU GPLv3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from time import sleep
from typing import List
import json
import os
import sys

import requests

import config_reader


CONFIG = config_reader.load_config()


def manipulate_repo_access(peer_review_mappings: dict, repo_mappings: dict, api_key=None, is_adding: bool = False) -> None:
    request_body_params = {"permission": "pull"}
    request_headers = {"Authorization": f"Token {api_key}"}
    counter = 0

    print()

    for user in peer_review_mappings:
        reviewed_students = peer_review_mappings[user]
        print(user)
        for reviewed_student in reviewed_students:
            reviewed_repo = repo_mappings[reviewed_student]["full_name"]
            if user == reviewed_student: continue
            collaborator_endpoint = f"https://api.github.com/repos/{reviewed_repo}/collaborators/{user}"
            if is_adding:
                print(f"\tReviewing {reviewed_student:<24}", end="")
                result = requests.put(collaborator_endpoint, json=request_body_params, headers=request_headers)
            else:
                print(f"\tLosing access to {reviewed_student:<24}", end="")
                result = requests.delete(collaborator_endpoint, headers=request_headers)
            status_code = result.status_code
            print(f" - [{status_code}]", end=" ")
            if is_adding and status_code == 201:
                print("OK")
            elif is_adding and status_code == 204:
                print("Already Added")
            elif status_code == 204:
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
    if not (os.path.isfile(CONFIG["path_to_peer_review_mappings"]) and os.path.isfile(CONFIG["path_to_repo_mappings"])):
        print("Call peer_review_group_creator.py first to generate peer review mappings and repo mappings!", file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 2 and sys.argv[1].lower() in ("add", "adding"):
        is_adding = True
    elif len(sys.argv) == 2 and sys.argv[1].lower() in ("remove", "removing", "revoke", "revoking", "restrict", "restricting"):
        is_adding = False
    else:
        print("Requires second argument: `add` or `remove`", file=sys.stderr)
        sys.exit(1)
    activity_verb = "add" if is_adding else "remove"
    print(f"Contacting GitHub API to {activity_verb} access... (this may take a while)")
    with open(CONFIG["path_to_peer_review_mappings"], "r") as f1:
        with open(CONFIG["path_to_repo_mappings"], "r") as f2:
            peer_mappings = json.load(f1)
            repo_mappings = json.load(f2)
            manipulate_repo_access(peer_mappings, repo_mappings, CONFIG["github_api_key"])
    print(f"Contacting GitHub API to {activity_verb} access done.")
