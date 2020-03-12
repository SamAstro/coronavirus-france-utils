#!/bin/bash

# Merges the master branch into all other branches
#
# Process:
#
#   - Save the name of the current branch
#   - If the current branch is not master then checkout master.
#   - Pull the latest changes for master from its upstream branch.
#   - Loop over each local branch.
#     - If the branch is not master.
#       - Checkout the branch.
#       - Merge master into the branch.
#   - If the current branch is not the saved branch name checkout the saved
#     branch name
#
# Source : https://gist.github.com/tmiller/5222478

# Navigate to repo
cd ${1}

# Returns the names of all the local branches
local_branches() {
  git for-each-ref --format="%(refname:short)" refs/heads
}

# Returns the name of the current branch
current_branch() {
  git symbolic-ref --short HEAD
}

saved_branch=$(current_branch)

[[ "${saved_branch}" != "master" ]] && git checkout "master"
git fetch upstream
git merge upstream/master

for branch in $(local_branches); do
  if [[ "${branch}" != "master" ]]; then
    echo
    git checkout "${branch}"
    git merge "master"
    git push
  fi
done

echo
[[ "${saved_branch}" != "$(current_branch)" ]] && git checkout "${saved_branch}"
