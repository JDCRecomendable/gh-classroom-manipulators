#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

from typing import List
import os
import requests
import subprocess


def get_github_api_result_page(url, api_key=None, page=None, per_page=None) -> requests.Response:
    headers = {}
    if api_key:
        headers["Authorization"] = f"Token {api_key}"
    if type(page) == int and page > 1:
        url = f"{url}?page={page}"
    if type(per_page) == int and per_page > 1:
        symbol = "&" if "?page=" in url else "?"
        url = f"{url}{symbol}per_page={per_page}"
    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        return result
    else:
        raise Exception(f"Error: {result.status_code}")


def list_assignment_submissions(path_to_assignment_submissions: str, assignment_prefix: str) -> List[str]:
    response = []
    assignment_submissions = os.listdir(path_to_assignment_submissions)
    for assignment_submission in assignment_submissions:
        if str(assignment_submission).startswith(assignment_prefix):
            response.append(assignment_submission)
    return response


def move_file(src_path: str, dest_path: str) -> None:
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
