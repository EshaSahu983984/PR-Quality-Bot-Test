#!/usr/bin/env python3
import argparse, os, requests, sys, re
from utils import gh_headers

p = argparse.ArgumentParser()
p.add_argument("--owner", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--pr", required=True)
args = p.parse_args()

# -------------------------------------------------------------------
# Load forbidden patterns from config/forbidden_files.txt
# -------------------------------------------------------------------
config_path = os.path.join(os.path.dirname(__file__), "..", "config", "forbidden_files.txt")

if not os.path.exists(config_path):
    print(f"::error::Missing config file: {config_path}")
    sys.exit(1)

with open(config_path, "r") as f:
    forbidden_patterns = [
        line.strip() for line in f.readlines()
        if line.strip() and not line.startswith("#")
    ]

if not forbidden_patterns:
    print("::warning::forbidden_files.txt is empty. No forbidden file checks applied.")

# -------------------------------------------------------------------
# Fetch PR files from GitHub API
# -------------------------------------------------------------------
url = f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}/files"
r = requests.get(url, headers=gh_headers())

if r.status_code != 200:
    print("::error::Failed to fetch PR files")
    sys.exit(1)

files = [f.get("filename", "") for f in r.json()]

# -------------------------------------------------------------------
# Validate forbidden file patterns
# -------------------------------------------------------------------
violations = []

for f in files:
    for pattern in forbidden_patterns:
        try:
            if re.search(pattern, f):
                violations.append(f)
                break
        except re.error:
            print(f"::error::Invalid regex in forbidden_files.txt → {pattern}")
            sys.exit(1)

if violations:
    print("::error::Forbidden files detected:")
    for v in violations:
        print(" -", v)
    sys.exit(1)

print("No forbidden files detected")

# -------------------------------------------------------------------
# Check .gitignore existence rule
#
# Rule:
# ✔ If .gitignore exists in target branch → PR does NOT need it
# ✔ If .gitignore missing in target branch → PR MUST include it
# -------------------------------------------------------------------

# PR branch /head ref
pr_head_ref = f"pull/{args.pr}/head"

# Get base branch name
pr_details_url = f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}"
pr_details_resp = requests.get(pr_details_url, headers=gh_headers())

if pr_details_resp.status_code != 200:
    print("::error::Failed to fetch PR details to determine base branch.")
    sys.exit(1)

base_branch = pr_details_resp.json().get("base", {}).get("ref")

if not base_branch:
    print("::error::Unable to determine PR target branch.")
    sys.exit(1)

# Check .gitignore in target branch
target_gitignore_url = (
    f"https://api.github.com/repos/{args.owner}/{args.repo}/contents/.gitignore?ref={base_branch}"
)
target_resp = requests.get(target_gitignore_url, headers=gh_headers())
target_exists = (target_resp.status_code == 200)

# Check .gitignore in PR branch
pr_gitignore_url = (
    f"https://api.github.com/repos/{args.owner}/{args.repo}/contents/.gitignore?ref={pr_head_ref}"
)
pr_resp = requests.get(pr_gitignore_url, headers=gh_headers())
pr_exists = (pr_resp.status_code == 200)

# ---------------------- Decision Logic ----------------------
if target_exists:
    print("✔ .gitignore exists in target branch → PR not required to contain it.")
else:
    # target missing
    if not pr_exists:
        print("::error::.gitignore does NOT exist in target branch and is also missing in PR.")
        print("PR MUST include a .gitignore file.")
        sys.exit(1)

    print("✔ Target branch missing .gitignore, but PR includes it → OK.")

# -------------------------------------------------------------------
# Success message
# -------------------------------------------------------------------
print("✔ PR Forbidden Files + .gitignore Validation Passed!")
sys.exit(0)
