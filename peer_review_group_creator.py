#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

# Licensed under the GNU GPLv3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from typing import List
import csv
import json

from utils import get_github_api_result_page
import config_reader


CONFIG = config_reader.load_config()


def list_gh_classroom_accepted_assignments(assignment_id, api_key=None) -> List[dict]:
    url = f"https://api.github.com/assignments/{assignment_id}/accepted_assignments"
    json_response = []
    page = 1
    per_page = 30
    has_next_page = True
    while has_next_page:
        result_page = get_github_api_result_page(url, api_key=api_key, page=page, per_page=per_page)
        raw_response = result_page.json()
        has_next_page = type(raw_response) == list and len(raw_response) == per_page
        page += 1
        json_response += raw_response
    return json_response


def map_gh_id_to_repo(accepted_assignments: List[dict], classroom_roster: dict) -> dict:
    student_to_assignment_mapping = {}
    for accepted_assignment in accepted_assignments:
        gh_id = accepted_assignment["students"][0]["login"]
        repo = accepted_assignment["repository"]
        repo["student_name"] = classroom_roster[gh_id]
        student_to_assignment_mapping[gh_id] = repo
    return student_to_assignment_mapping


if __name__ == "__main__":
    classroom_roster = {}

    print("Parsing Classroom Roster...")
    with open(CONFIG["path_to_github_classroom_roster"], "r") as classroom_roster_file:
        csv_reader = csv.reader(classroom_roster_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count and row[1] != "":
                classroom_roster[row[1]] = row[0]
            line_count += 1
        print(f"Parsing Classroom Roster done.  Processed {line_count} lines.")

    print("Getting GitHub Classroom Accepted Assignments... (this may take a while)")
    accepted_assignments = list_gh_classroom_accepted_assignments(CONFIG["github_classroom_assignment_id"], CONFIG["github_api_key"])
    print("Getting GitHub Classroom Accepted Assignments done.")

    print("Mapping GitHub IDs to repositories...")
    gh_id_to_repo_mappings = map_gh_id_to_repo(accepted_assignments, classroom_roster)
    with open(CONFIG["path_to_repo_mappings"], "w") as f:
        f.write(json.dumps(gh_id_to_repo_mappings, indent=2))
    print("Mapping GitHub IDs to repositories done.")

    print("Grouping students together for peer reviews...")
    peer_review_groups = {}
    valid_students = sorted(list(gh_id_to_repo_mappings.keys()))
    print(f"Got {len(valid_students)} students.")
    for i in range(len(valid_students)):
        reviewing_student_id = valid_students[i]
        interval = CONFIG["peer_assignment_interval"]
        peers = []
        for j in range(1, CONFIG["peer_count"] + 1):
            reviewed_student_id = valid_students[(i + j * interval) % len(valid_students)]
            if reviewing_student_id == reviewed_student_id:
                print("Got the same student!")
                exit(1)
            peers.append(reviewed_student_id)
        peer_review_groups[reviewing_student_id] = peers

    with open(CONFIG["path_to_peer_review_mappings"], "w") as f:
        f.write(json.dumps(peer_review_groups, indent=2, sort_keys=True))
    print("Grouping students together for peer reviews done.")
