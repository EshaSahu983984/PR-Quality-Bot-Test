import requests
import argparse
import os
import sys

FORBIDDEN_PATTERNS = ["*.log", "*.tmp", "*.exe", "__pycache__"]

parser = argparse.ArgumentParser()
parser.add_argument("--owner")
parser.add_argument("--repo")
parser.add_argument("--pr")
args = parser.parse_args()

token = os.getenv("GITHUB_TOKEN")
url = f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}/files"
headers = {"Authorization": f"token {token}"}

response = requests.get(url, headers=headers)
files = [f["filename"] for f in response.json()]

violations = [f for f in files if any(pat in f for pat in FORBIDDEN_PATTERNS)]

if violations:
    print("::error::Forbidden files detected in PR:")
    for f in violations:
        print(f" - {f}")
    sys.exit(1)
else:
    print("✅ No unwanted files detected.")
