#!/usr/bin/env python3
import argparse, requests, sys, re, os

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--owner", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--pr", required=True)
    args=p.parse_args()

    token=os.getenv("GITHUB_TOKEN")
    if not token:
        print("Missing GITHUB_TOKEN"); sys.exit(1)

    url=f"https://api.github.com/repos/{args.owner}/{args.repo}/pulls/{args.pr}"
    r=requests.get(url, headers={"Authorization":f"token {token}"})
    data=r.json()
    body=data.get("body","") or ""
    if len(body.strip()) < 20:
        print("PR description missing or too short.")
        sys.exit(1)
    # Jira or ADO work item detection (example patterns)
    if not re.search(r"[A-Z]{2,}-\d+", body) and not re.search(r"AB#\d+", body):
        print("No Jira or ADO work-item reference found in PR description.")
        sys.exit(1)
    print("PR description OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
