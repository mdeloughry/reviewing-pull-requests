#!/usr/bin/env python3
"""Post PR review comments to Bitbucket Cloud as pending drafts. Never submits.

Usage: post_pending_comments.py <PR-ID> <comments.json> [--repo workspace/slug]

comments.json is a list of {"path": str|null, "line": int|null, "body": str}.
path/line null = general comment. Credentials: $BITBUCKET_USERNAME and
$BITBUCKET_APP_PASSWORD must already be in the environment.

Safety order:
  1. every inline line must fall inside a diff hunk, or nothing is posted
  2. the first comment is posted alone and read back; if Bitbucket did not
     store it as pending, it is deleted and the script stops
  3. the rest are posted, then every comment this run created is re-read
     and must still be pending
"""
import base64, json, os, re, subprocess, sys, urllib.request, urllib.error

def die(msg):
    sys.exit(f"STOP: {msg}")

def repo_from_git():
    url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    m = re.search(r"bitbucket\.org[:/]([^/]+)/([^/.]+?)(?:\.git)?$", url)
    if not m:
        die(f"origin is not a Bitbucket remote: {url!r}; pass --repo workspace/slug")
    return f"{m.group(1)}/{m.group(2)}"

def call(method, url, body=None, raw=False):
    user, pw = os.environ.get("BITBUCKET_USERNAME"), os.environ.get("BITBUCKET_APP_PASSWORD")
    if not user or not pw:
        die("BITBUCKET_USERNAME / BITBUCKET_APP_PASSWORD not set (ask before loading them)")
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode())
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            data = r.read().decode()
    except urllib.error.HTTPError as e:
        die(f"{method} {url} -> {e.code}: {e.read().decode()[:300]}")
    return data if raw else (json.loads(data) if data else {})

def commentable_lines(diff):
    """{path: set(new-file line numbers)} from a unified diff, context lines included."""
    lines, path = {}, None
    for ln in diff.splitlines():
        if ln.startswith("+++ "):
            path = None if ln[4:] == "/dev/null" else re.sub(r"^b/", "", ln[4:])
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", ln)
        if m and path:
            start, count = int(m.group(1)), int(m.group(2) or 1)
            lines.setdefault(path, set()).update(range(start, start + count))
    return lines

def payload(c):
    p = {"content": {"raw": c["body"]}, "pending": True}
    if c.get("path"):
        p["inline"] = {"path": c["path"], "to": c["line"]}
    return p

def main():
    args = sys.argv[1:]
    repo = None
    if "--repo" in args:
        i = args.index("--repo"); repo = args[i + 1]; del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    pr, comments = args[0], json.load(open(args[1]))
    api = f"https://api.bitbucket.org/2.0/repositories/{repo or repo_from_git()}/pullrequests/{pr}"

    ok = commentable_lines(call("GET", f"{api}/diff", raw=True))
    bad = [c for c in comments if c.get("path") and c["line"] not in ok.get(c["path"], set())]
    if bad:
        die("not on a changed line, move these into the general comment:\n" +
            "\n".join(f"  {c['path']}:{c['line']}" for c in bad))

    first = call("POST", f"{api}/comments", payload(comments[0]))
    if first.get("pending") is not True:
        call("DELETE", f"{api}/comments/{first['id']}")
        die(f"Bitbucket stored the test comment as live (id {first['id']}); deleted it. Nothing else posted.")
    created = [first["id"]]
    for c in comments[1:]:
        created.append(call("POST", f"{api}/comments", payload(c))["id"])

    live = [i for i in created if call("GET", f"{api}/comments/{i}").get("pending") is not True]
    for i, c in zip(created, comments):
        print(f"{i}  {c.get('path') or '(general)'}{':' + str(c['line']) if c.get('path') else ''}")
    if live:
        die(f"these are LIVE, not drafts: {live}")
    print(f"OK: {len(created)} pending, 0 live. Nothing submitted.")

if __name__ == "__main__":
    main()
