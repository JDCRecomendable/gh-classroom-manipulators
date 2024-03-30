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

from pathos.multiprocessing import ProcessPool as Pool

from utils import list_assignment_submissions
import config_reader

# Requires `pandoc` to be installed on the underlying system.


CONFIG = config_reader.load_config()


def compile_markdown_to_pdf(path_to_submission_file: str, assignment_prefix: str) -> None:
    parent_path = "/".join(path_to_submission_file.split("/")[:-1])
    src_gh_username = parent_path.split("/")[-1][len(assignment_prefix):]
    basename = path_to_submission_file.split("/")[-1]
    command = f"cd {parent_path} && pwd && pandoc {basename} -t html --embed-resources=true --standalone -o {src_gh_username}__{basename.split(".")[0]}.html"
    subprocess.run(
        command,
        shell=True,
        check=True,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL
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

    print("Getting GitHub Classroom Accepted Assignments... (this may take a while)")
    assignment_submissions = list_assignment_submissions(CONFIG["path_to_peer_review_src"], CONFIG["assignment_prefix"])
    print("Getting GitHub Classroom Accepted Assignments done.")

    print("Preparing for compilation...")
    to_compile_to_pdf = []
    for assignment_submission in assignment_submissions:
        path_to_assignment_submission = f"{CONFIG['path_to_peer_review_src']}/{assignment_submission}"
        submission_files = os.listdir(path_to_assignment_submission)
        for submission_file in submission_files:
            if submission_file.endswith(".md") and not (submission_file.startswith("github") or submission_file.startswith("README")):
                path_to_submission_file = f"{path_to_assignment_submission}/{submission_file}"
                to_compile_to_pdf.append(path_to_submission_file)
    print("Preparing for compilation done.")

    print("Compiling Markdown files to PDF...")
    with Pool() as pool:
        pool.map(compile_markdown_to_pdf, to_compile_to_pdf)
    print("Compiling Markdown files to PDF done.")
