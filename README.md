# Assignment Manipulators

Copyright (c) 2023-2024 Jared Daniel Recomendable.


## What is this?

A collection of scripts for manipulating student submissions made to platforms such as GitHub Classroom.


## Requirements

* Unix System (macOS, most GNU/Linux distros, WSL under Windows)
* `pathos` for parallelism
* `requests` Library
* GitHub API Key

```sh
pip3 install pathos requests
```

See Developer setttings on GitHub to obtain your API key.  Be sure to include `administration:write` permissions.


## Configuration

The Python scripts takes its configuration from `config.json`, which is included in `.gitignore`.

### `github_api_key`

The API key obtained from the GitHub Developer settings.  Required to make GitHub API requests to manipulate GitHub Orgnanization and GitHub Classroom repos.

### `github_classroom_assignment_id`

The assignment ID assigned by GitHub Classroom to an assignment.  Required to list accepted assignments in GitHub Classroom.

To obtain this, make a GET request to https://api.github.com/classrooms/{CLASSROOM_ID}/assignments with your GitHub API key.

Meanwhile, to obtain `CLASSROOM_ID`, make a GET request to https://api.github.com/classrooms with your GitHub API key.

### `path_to_github_classroom_roster`

The path to the roster file generated from the GitHub Classroom web user interface.

### `peer_count`

The number of peer reviewers per peer in peer assignments.

### `peer_assignment_interval`

For peer reviews, each student reviews every nth peer from its ordinal rank, where n is defined as the `peer_assignment_interval`.  In the case that the nth peer from the student's ordinal rank occurs after the end of the list, a wraparound occurs to the start of the list.

### `path_to_peer_review_src`

Path to the directory containing subdirectories, where each subdirectory is a cloned repository from GitHub.

Each cloned repository contains peer reviews written by the student assigned to that repository.

Each peer review is written in a Markdown file.  The Markdown file may reference live media, such as GIFs and screencasts.  They need to be converted into self-contained HTML files for distribution to the target peers reviewed by the student.

### `path_to_peer_review_dest`

Path to the directory containing subdirectories, where each subdirectory contains HTML files.

Each subdirectory is named after a student who has received a peer review from peers.

### `path_to_repo_mappings`

Path to the file mapping GitHub usernames to assignment repository URLs.

### `path_to_peer_review_mappings`

Path to the file mapping a student to peers whom they will review.
