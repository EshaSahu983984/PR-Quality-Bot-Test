import argparse
import requests
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--owner")
parser.add_argument("--repo")
parser.add_argument("--pr")
parser.add_argument("--threshold", type=int, default=300)
args = parser.parse_args()

token = os.getenv("GITHUB_TOKEN")
url = f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}/files"
headers = {"Authorization": f"token {token}"}

response = requests.get(url, headers=headers)
files = response.json()

total_changes = sum(f["additions"] + f["deletions"] for f in files)

if total_changes > args.threshold:
    print(f"::warning::PR too large ({total_changes} lines changed). Threshold: {args.threshold}")
else:
    print(f"✅ File change analysis passed ({total_changes} lines changed).")
