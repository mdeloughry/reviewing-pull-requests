---
name: reviewing-pull-requests
description: Use when asked to review someone else's pull request, check whether a PR matches its Jira ticket, say whether a PR can be approved, or draft review comments for a Bitbucket PR. Not for checking your own branch before raising a PR (that is pre-pr-review).
---

# Reviewing pull requests

**The review goes out in Matt's name, in Matt's voice, and he answers the replies.** So every sentence must be true, must sound like him, and must be something he understands. Verify everything, decide everything, explain it to him, then leave it as drafts for him to submit.

## 1. Pin down what is being reviewed

1. **Fetch the PR**: title, author, source and **destination** branch, tip commit, reviewers, existing comments, build status.
2. **Diff source against destination**, not against `main`. A PR can target a feature branch, and the parent branch's work is not this PR's.
3. **Read the ticket's acceptance criteria.** Map each one to done, partial or not started, for this PR and for the whole branch.
4. **Read every linked ticket.** They can contradict the PR, or cite its files.

## 2. Verify every claim before it goes in

| Check | Why |
|---|---|
| **Counts** come from a script, not from reading | Hand counts were wrong twice ("all nine" was eight) |
| **Quotes are exact**, including symbols like `§` | Tidying a quote changes evidence |
| **Who did what**: never "I added" | The reviewer didn't write the PR |
| **The project's own rule** is cited, not taste | "The contributing guide says…" ends the debate. "I prefer…" starts one |
| **The fix actually works** | "Repoint the links" pointed at an empty file |
| **Praise is specific and true** | "The approach held up" was false |
| **Symptoms of one cause are one point** | Three points for one problem reads as three failures |

Re-check every sentence against its source before drafting. Drop any claim that doesn't survive.

## 3. Write it in Matt's voice

**It should read like Matt typed it to a colleague**, not like a report about their work.

| Not this | This |
|---|---|
| "I can't approve it as it stands. Seven things to fix." | "Really good work on this. There are a few tidy-ups before I approve." |
| "Every cell I added links…" | "Every cell this PR adds links…" |
| "The ticket says a result without versions is just a guess." | "Could you fill this in? It needs the version of each tool you used." |
| "We need to pick one: keep the copies or redo the work." | "I'm happy with the new version, so let's swap it in for the old one." |

- **First person only for Matt's own view or decision**: "I'm happy to", "before I approve". Never for the author's work.
- **Ask, don't order**: "Could you…", "Please add…".
- **Contractions, plain words, varied sentence length.** No em-dashes, no "it's not just X", no closing summary. His `CLAUDE.md` ticket-writing rules apply.
- **Each point says what, where, and exactly what to do.** File, line, count.
- **No open choices.** Decide, or ask Matt in chat first. A question in the review comes back as a question he has to answer.
- **Leave out anything that invites debate**: scale numbers, pointed quotes, side observations.
- **Dyslexia-friendly**: headline first, short sentences, bold anchors, numbered steps. Matt asked for this on PR reviews, which overrides the no-dyslexia-style-on-tickets rule.
- **Things only for Matt** (doubts, follow-ups) go in chat, never in the review.

## 4. Split into inline and general comments

- **Inline**: one per issue, on a line **this PR changes**. Bitbucket refuses anything else.
- **General**: a short checklist pointing at the inline comments, plus what can't go inline (untouched files, Jira tickets, work for later).

## 5. Make sure Matt understands it

**Matt answers the replies, so he has to understand every point before it posts.** A point he can't explain back is a point the author won't understand either.

1. **Explain each point plainly in chat**: what's wrong, why it matters, what the fix is. Dyslexia-friendly, one point at a time if there are several.
2. **Give Matt links** to see each issue himself: `https://bitbucket.org/<ws>/<repo>/src/<tip>/<path>#lines-N`.
3. **Ask him to confirm he understands and agrees** with every point. Don't take "looks fine" on the whole draft as that.
4. **If he's unsure about a point, the point is the problem.** Rewrite it until it's clear, or drop it. Never post a point he's asked about but not confirmed.

## 6. Post as drafts

1. **Save** the general comment and `comments.json` in the scratchpad. Open them in `fresh` in a herdr split to the right.
2. **Wait for his OK** on that exact draft, then post as pending drafts:

```bash
~/.claude/skills/reviewing-pull-requests/post_pending_comments.py <PR-ID> comments.json
```

`comments.json` is `[{"path": "docs/x.md", "line": 12, "body": "…"}, {"path": null, "line": null, "body": "general"}]`.

The script refuses lines outside the diff. It posts one draft and reads it back before the rest, and it ends by confirming 0 live.

## Never

- **Submit, approve or decline.** Matt does that in Bitbucket.
- **Load credentials without asking.** Ask before `bw-ensure`, every time.
- **Post without Matt's OK** on that exact draft.
- **Post a point Matt hasn't confirmed he understands.**
