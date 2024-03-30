# GitHub Classroom Assignment Repo Manipulators

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


## Workflow

The following shows which script(s) to run and in what order (if applicable) depending on the context.

### Cloning Assignment Repos

* Run `assignment_repo_cloner.py`, modifying the following configuration values in `config.json`:
    * `github_api_key`
    * `github_org`
    * `assignment_prefix`
    * `assignment_date_filter`
    * `path_to_clone_assignment_repos`

### Granting or Restricting Access to Student Repos

* Run `code_owner_permissions_modifier.py`, modifying the following configuration values in `config.json`:
    * `github_api_key`
    * `github_org`
    * `assignment_prefix`
    * `path_to_repo_mappings`
    * `collaborator_permission`

### Making Bulk Changes to Student Repos

* Copy `git_actions_runner.sh` to the directory containing the student repos, then adapt the script accordingly.
* Remember to set execute permissions prior to running.

### Assigning Peer Reviews

Do this prior to the start of a peer review assignment.

1. Run `peer_review_group_creator.py`, modifying the following configuration values in `config.json`:
    * `github_api_key`
    * `github_classroom_assignment_id`
    * `path_to_github_classroom_roster`
    * `peer_count`
    * `peer_assignment_interval`
    * `path_to_repo_mappings`
    * `path_to_peer_review_mappings`
2. Next, run `peer_review_repo_access.py`, passing in `add` as the argument and modifying the following configuration values in `config.json`:
    * `github_api_key`
    * `path_to_repo_mappings`
    * `path_to_peer_review_mappings`

### Distributing Peer Reviews

Do this when a peer review assignment has concluded, and to pass on peer reviews to the target recipients.

1. Block out existing peer reviewers from accessing their peers' repos by running `peer_review_repo_access.py`, passing in `remove` as the argument and modifying the following configuration values in `config.json`:
    * `github_api_key`
    * `path_to_repo_mappings`
    * `path_to_peer_review_mappings`
2. Next, inspect directories for any improperly-formatted Markdown files, or Markdown files that do not follow the naming convention of `{target_recipient_gh_username}.md`, making corrections (and applying penalties) where necessary.
3. Next, run `peer_review_md_to_html_compiler.py`, modifying the following configuration values in `config.json`:
    * `assignment_prefix`
    * `path_to_peer_review_src`
    * `path_to_github_classroom_roster`
4. Next, run `peer_review_sorter.py`, modifying the following configuration values in `config.json`:
    * `assignment_prefix`
    * `path_to_github_classroom_roster`
    * `path_to_peer_review_src`
    * `path_to_peer_review_dest`
5. Next, inspect the directory bearing the Markdown files for distributions for anomalies.  E.g. students may have mispelt the name of a GitHub username while naming their Markdown files for peer reviews, leading to duplicate entries for the target recipient.  Make corrections where necessary, and apply penalties to the source of the peer review where needed.
6. Next, if the recipient should not know the source of their peer reviews, run `peer_review_anonymizer.py`, modifying the following configuration values in `config.json`:
    * `path_to_peer_review_dest`
7. Next, zip each directory containing the peer reviews for each recipient, adapting `git_actions_runner.sh` where needed.
8. Next, stage each recipient's ZIP file containing their peer reviews onto their Git repositories, adapting `git_actions_runner.sh` where needed.
9. Finally, commit the changes and push to the remote repo for each recipient, adapting `git_actions_runner.sh` where needed.


## Configuration

The Python scripts takes its configuration from `config.json`, which is included in `.gitignore`.

Below are descriptions of each key in `config.json`.

### `github_api_key`

The API key obtained from the GitHub Developer settings.  Required to make GitHub API requests to manipulate GitHub Orgnanization and GitHub Classroom repos.

### `github_classroom_assignment_id`

The assignment ID assigned by GitHub Classroom to an assignment.  Required to list accepted assignments in GitHub Classroom.

To obtain this, make a GET request to https://api.github.com/classrooms/{CLASSROOM_ID}/assignments with your GitHub API key.

Meanwhile, to obtain `CLASSROOM_ID`, make a GET request to https://api.github.com/classrooms with your GitHub API key.

### `github_org`

The name of the GitHub Organization that stores the GitHub assignment repos.

### `assignment-prefix`

A string that prefixes the assignment repo names.  Typically this is the name of the starter/template repo made for the GitHub Classroom assignment, plus a dash at the end.

### `assignment_date_filter`

A (partial) date string in ISO-8601 used to filter for assignment repos when cloning them from a GitHub Organization based on creation time.

Useful for GitHub Organizations that lump together submissions from different iterations of a course (e.g. over the years).

E.g. to obtain repos created in 2024, assign the value `2024-` to `assignment_date_filter`.  To further limit the search to April 2024, assign the value `2024-04-` instead.

### `path_to_clone_assignment_repos`

The path to the directory where the repos will be cloned to, i.e. will store the subdirectories where each subdirectory is a repo for an assignment submission.

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

### `collaborator_permission`

The permission to give collaborators of a repo.

Typically used to control student access to their repos, e.g. when the due date has lapsed.

Available values can be found by [reading the GitHub API docs](https://docs.github.com/en/rest/collaborators/collaborators?apiVersion=2022-11-28#add-a-repository-collaborator).

Requires `admin` permission on a repo to successfully update other collaborators' permissions.
