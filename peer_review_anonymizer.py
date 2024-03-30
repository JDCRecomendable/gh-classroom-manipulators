#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

# Licensed under the GNU GPLv3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from typing import List
import os

from utils import list_assignment_submissions, move_file
import config_reader

# Run after preparing peer review files for destination, i.e. peer_review_sorter.py


CONFIG = config_reader.load_config()


def list_peer_review_submissions(path_to_peer_review_submissions) -> List[str]:
    response = []
    peer_review_submissions = os.listdir(path_to_peer_review_submissions)
    for peer_review_submission in peer_review_submissions:
        if os.path.isdir(f"{path_to_peer_review_submissions}/{peer_review_submission}"):
            response.append(peer_review_submission)
    return response


if __name__ == "__main__":
    print("Getting Submitted Peer Reviews... (this may take a while)")
    peer_review_submissions = list_peer_review_submissions(CONFIG["path_to_peer_review_dest"])
    print("Getting Submitted Peer Reviews done.")

    print("Anonymizing Peer Review files...")
    for peer_review_submission in peer_review_submissions:
        path_to_peer_review_submission = f"{CONFIG['path_to_peer_review_dest']}/{peer_review_submission}"
        all_files = os.listdir(path_to_peer_review_submission)
        count = 1
        for file in all_files:
            if file.endswith(".html"):
                move_file(f"{path_to_peer_review_submission}/{file}", f"{path_to_peer_review_submission}/{count}.html")
                count += 1
    print("Anonymizing Peer Review files done.")
