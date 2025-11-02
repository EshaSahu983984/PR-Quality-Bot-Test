import sys
import re

def validate_commit_message(msg):
    pattern = r"^(feat|fix|chore|refactor):\s+.+$"
    if not re.match(pattern, msg):
        print("::error::Invalid commit message format.")
        sys.exit(1)
    print("✅ Commit message check passed!")

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else ""
    validate_commit_message(message)
