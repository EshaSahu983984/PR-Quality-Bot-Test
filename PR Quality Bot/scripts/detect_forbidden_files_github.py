#!/usr/bin/env python3
import argparse, os, requests, sys, re
from utils import gh_headers

p = argparse.ArgumentParser()
p.add_argument("--owner", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--pr", required=True)
args = p.parse_args()

url = f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}/files"
r = requests.get(url, headers=gh_headers())
if r.status_code != 200:
    print("::error::Failed to fetch PR files")
    sys.exit(1)

files = [f.get("filename","") for f in r.json()]
forbidden = [
    r"\.env$", r"\.env\.", r"node_modules/", r"(^|/)\.vscode/", r"(^|/)\.idea/",
    r"\.log$", r"\.pyc$", r"\.dll$", r"\.exe$", r"(^|/)(__pycache__)/"
]
violations = []
for f in files:
    for pat in forbidden:
        if re.search(pat, f):
            violations.append(f)
            break
if violations:
    print("::error::Forbidden files detected:")
    for v in violations:
        print(" -", v)
    sys.exit(1)
print("No forbidden files detected")
sys.exit(0)
