#!/bin/sh

# Place this script in a directory containing subdirectories, where each subdirectory is a GitHub repo.

for dir in *; do
    if [[ -d $dir ]]; then
        cd $dir
        username="${dir:13}"
        zip_source="{PATH_TO_DIRECTORY_CONTAINING_GITHUB_REPOS_HERE}"
        extension=".zip"
        source_file="${zip_source}${username}${extension}"
        if [[ -f ${source_file} ]]; then
            echo ${source_file}
            #cp ${source_file} .
            #git add .
            #git commit -m "docs: Add peer reviews"
            #git push
        fi
        cd ..
    fi
done
