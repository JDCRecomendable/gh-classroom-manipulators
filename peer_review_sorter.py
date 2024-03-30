#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

# Licensed under the GNU GPLv3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import csv
import os
import subprocess

from utils import list_assignment_submissions
import config_reader

# Run after compiling student peer review Markdown files into HTML, i.e. peer_review_md_to_html_compiler.py


CONFIG = config_reader.load_config()


def move_to_directory(src_path: str, dest_path: str) -> None:
    create_directory_command = f"mkdir -p {'/'.join(dest_path.split("/")[:-1])}"
    move_command = f"mv {src_path} {dest_path}"

    subprocess.run(
        create_directory_command,
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    subprocess.run(
        move_command,
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


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

    print("Getting Assignments Submissions... (this may take a while)")
    assignment_submissions = list_assignment_submissions(CONFIG["path_to_peer_review_src"], CONFIG["assignment_prefix"])
    print("Getting Assignments Submissions done.")

    print("Moving directories...")
    for assignment_submission in assignment_submissions:
        path_to_assignment_submission = f"{CONFIG['path_to_peer_review_src']}/{assignment_submission}"
        all_files = os.listdir(path_to_assignment_submission)
        for file in all_files:
            if file.endswith(".html"):
                path_to_src_file = f"{path_to_assignment_submission}/{file}"
                src_gh_username = file.split("__")[0].split(".")[0]
                dest_gh_username = file.split("__")[1].split(".")[0]
                path_to_dest_file = f"{CONFIG['path_to_peer_review_dest']}/{dest_gh_username}/{src_gh_username}.html"
                move_to_directory(path_to_src_file, path_to_dest_file)
    print("Moving directories done.")
