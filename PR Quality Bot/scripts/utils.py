# minimal helpers used by other scripts
import os, requests, sys

def gh_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Missing GITHUB_TOKEN")
        sys.exit(1)
    return {"Authorization": f"token {token}", "Accept":"application/vnd.github+json"}

def gh_api(url):
    return requests.get(url, headers=gh_headers())
