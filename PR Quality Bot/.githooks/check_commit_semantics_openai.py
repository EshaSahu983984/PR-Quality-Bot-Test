#!/usr/bin/env python3
import sys, json, re, os

def is_vague_text(s: str) -> bool:
    vague_terms = ["test", "temp", "update", "changes", "misc", "stuff", "fix issue", "minor"]
    s = s.lower()
    return any(t in s for t in vague_terms) or len(s.split()) < 4

def run_openai_check(message: str) -> int:
    # optional: call OpenAI ChatCompletion if OPENAI_API_KEY is set
    # keep this optional: if no key, fallback to heuristic
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return 0 if not is_vague_text(message) else 1

    try:
        import openai
        openai.api_key = key
        prompt = (
            "You are a commit-message reviewer. Reply JSON {\"status\":\"VALID\"|\"INVALID\",\"suggestion\":\"...\"}.\n"
            "Commit message:\n'''%s'''\n\nIf the message is vague, suggest an improved Conventional Commit message." % message
        )
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=150
        )
        text = resp.choices[0].message.content.strip()
        try:
            j = json.loads(text)
            return 0 if j.get("status","")=="VALID" else 1
        except:
            return 0 if not is_vague_text(message) else 1
    except Exception:
        return 0 if not is_vague_text(message) else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_commit_semantics_openai.py <commit_msg_file>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        msg = f.read().strip()
    rc = run_openai_check(msg)
    if rc != 0:
        print("❌ Commit blocked due to vague message.")
        sys.exit(1)
    print("✅ Commit message looks good.")
    sys.exit(0)
