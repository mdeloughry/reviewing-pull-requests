# reviewing-pull-requests

**A Claude Code skill for reviewing someone else's pull request, and leaving the comments as drafts for you to send.**

I built this after a review went through five drafts before it was right. The first version was harsh, had a couple of wrong numbers in it, and suggested a fix that wouldn't have worked. This skill is the checklist that would have got it right first time.

## What it does

1. **Pins down the PR.** It diffs against the branch the PR actually targets and reads the ticket and any linked tickets.
2. **Verifies every claim.** Counts come from a script, quotes stay exact, and every fix it suggests has to actually work.
3. **Writes in your voice.** Warm, specific, and every point says what to do. No open questions for the author to bounce back.
4. **Splits inline from general.** One inline comment per issue, on a changed line, and a short general comment that points at them.
5. **Checks you understand it.** It explains each point before posting, because you're the one who answers the replies.
6. **Posts as drafts.** Nothing is submitted. You review and send it yourself.

## Posting drafts safely

`post_pending_comments.py` posts to Bitbucket Cloud with `pending: true`, so the comments stay drafts until you submit the review.

- It refuses any inline comment on a line that isn't in the diff.
- It posts one comment and reads it back. If Bitbucket stored it as live, it deletes it and stops.
- It finishes by re-reading every comment it made and confirming none are live.

```bash
export BITBUCKET_USERNAME=... BITBUCKET_APP_PASSWORD=...
./post_pending_comments.py 57 comments.json
```

`comments.json`:

```json
[
  {"path": "docs/guide.md", "line": 12, "body": "Could you fill this in?"},
  {"path": null, "line": null, "body": "General comment"}
]
```

## Install

```bash
cp -r skills/reviewing-pull-requests ~/.claude/skills/
```

## It's opinionated

This is set up for how I work: Bitbucket Cloud, Jira, a dyslexia-friendly writing style, and my own tools for secrets and terminal panes. Fork it and change the voice section and the tooling to fit yours.

## Licence

MIT
