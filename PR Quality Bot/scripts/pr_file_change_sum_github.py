#!/usr/bin/env python3
import argparse, os, requests, sys
from utils import gh_headers

p = argparse.ArgumentParser()
p.add_argument("--owner", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--pr", required=True)
p.add_argument("--threshold", type=int, default=300)
args = p.parse_args()

per_page=100
page=1
total=0
while True:
    url = f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}/files?page={page}&per_page={per_page}"
    r = requests.get(url, headers=gh_headers())
    if r.status_code != 200:
        print("::error::Failed to fetch PR files")
        sys.exit(1)
    batch = r.json()
    if not batch:
        break
    for f in batch:
        total += (f.get("additions",0) + f.get("deletions",0))
    if len(batch) < per_page:
        break
    page += 1

print(f"Total changes (add+del): {total}")
if total > args.threshold:
    print(f"::warning::PR too large ({total} lines changed). Threshold: {args.threshold}")
    sys.exit(1)
print("PR size OK")
sys.exit(0)
