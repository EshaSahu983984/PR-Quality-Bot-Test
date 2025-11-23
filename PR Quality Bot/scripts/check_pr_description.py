#!/usr/bin/env python3
import argparse, os, sys, re, requests
from utils import gh_headers

p = argparse.ArgumentParser()
p.add_argument("--owner", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--pr", required=True)
args = p.parse_args()

url = f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}"
r = requests.get(url, headers=gh_headers())
if r.status_code != 200:
    print("::error::Failed to fetch PR details")
    sys.exit(1)

body = r.json().get("body", "") or ""
if len(body.strip()) < 20:
    print("::error::PR description missing or too short (min 20 chars).")
    sys.exit(1)

# -------------------------------------------------------------
# Work item reference patterns
# -------------------------------------------------------------
jira_pattern = r"[A-Z]{2,}-\d+"      # Jira: ELM-123
ado_with_prefix = r"AB#\d+"          # ADO: AB#12345
ado_standalone_num = r"\b\d{3,7}\b"  # ADO numeric: 12345 (standalone)

# Require at least one valid ticket reference
if not (
    re.search(jira_pattern, body)
    or re.search(ado_with_prefix, body)
    or re.search(ado_standalone_num, body)
):
    print("::error::No Jira or ADO work item reference found in PR description.")
    sys.exit(1)

# -------------------------------------------------------------
# Warning for missing 'checklist' or 'table'
# -------------------------------------------------------------
if not (re.search(r"\bchecklist\b", body, re.IGNORECASE) or
        re.search(r"\btable\b", body, re.IGNORECASE)):
    print("::warning::PR description does not contain 'checklist' or 'table'. Consider adding them for clarity.")

print("PR Description Validation Passed!")
print("Your PR description follows the required guidelines. Good job!")

sys.exit(0)
