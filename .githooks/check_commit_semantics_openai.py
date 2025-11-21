#!/usr/bin/env python3
import sys
import re

def is_vague_message(message: str) -> bool:
    vague_terms = [
        "test commit", "update", "changes", "fix issue", "minor fix",
        "temp", "trying", "stuff", "test", "check", "misc"
    ]
    msg_lower = message.lower()
    return any(term in msg_lower for term in vague_terms)

def validate_commit_message(commit_message: str) -> bool:
    """
    Validates the commit message format and ensures it’s descriptive.
    Format: feat|fix|chore|refactor: description
    """
    pattern = r"^(feat|fix|chore|refactor): .+"
    if not re.match(pattern, commit_message.strip()):
        print("❌ Commit message must follow 'feat|fix|chore|refactor: description'")
        return False

    if len(commit_message.split()) < 4:
        print("❌ Commit message too short — add more description.")
        return False

    if is_vague_message(commit_message):
        print("❌ Commit blocked due to vague message.")
        print("💡 Tip: Use a descriptive message like 'feat: add semantic commit validation logic'")
        return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: check_commit_semantics_openai.py <commit_message_file>")
        sys.exit(1)

    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, 'r', encoding='utf-8') as f:
        commit_message = f.read().strip()

    if not validate_commit_message(commit_message):
        sys.exit(1)

    print("✅ Commit message looks good!")
    sys.exit(0)


if __name__ == "__main__":
    main()
