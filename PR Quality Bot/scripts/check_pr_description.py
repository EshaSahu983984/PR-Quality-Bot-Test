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

body = r.json().get("body","") or ""
if len(body.strip()) < 20:
    print("::error::PR description missing or too short (min 20 chars).")
    sys.exit(1)

# require either Jira-like ticket or ADO AB# reference
if not (re.search(r"[A-Z]{2,}-\d+", body) or re.search(r"AB#\d+", body)):
    print("::error::No Jira or ADO work item reference found in PR description.")
    sys.exit(1)

print("✅ PR description OK")
sys.exit(0)
