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
# Ensure .gitignore exists in PR branch (NOT default branch)
# -------------------------------------------------------------------
gitignore_url = (
    f"https://api.github.com/repos/{args.owner}/{args.repo}/contents/.gitignore"
    f"?ref=pull/{args.pr}/head"
)

response = requests.get(gitignore_url, headers=gh_headers())

if response.status_code == 404:
    print("::error::.gitignore file is missing in the PR branch.")
    sys.exit(1)

if response.status_code != 200:
    print("::error::Failed to verify .gitignore due to GitHub API error.")
    sys.exit(1)

print(".gitignore file found in PR branch.")

# -------------------------------------------------------------------
# Success message
# -------------------------------------------------------------------
print("✔ PR Forbidden Files Validation Passed!")
sys.exit(0)
