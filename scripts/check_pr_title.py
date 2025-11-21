import sys
import re

def check_title(title):
    pattern = r"^(feat|fix|chore|refactor):\s+.+$"
    if not re.match(pattern, title):
        print("::error::Invalid PR title format. Use 'feat: ...' or 'fix: ...'")
        sys.exit(1)
    print("✅ PR title check passed")

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else ""
    check_title(title)
