## THE ROOT CHECKOUT

You are the only shell on `main` at the repo root. Orient before writing:

```bash
git rev-parse --show-toplevel && git branch --show-current
git status --short --branch && git worktree list
```

Proceed only when the top level matches the boot document and the root is on
`main`. A dirty root, detached head, or diverged main is a decision boundary:
show the exact state to the FnB before changing it. Every other worktree
belongs to its shell. Never switch its branch, stash, reset, clean, move, or
remove it; repository-wide cleanup happens only on the FnB's request through
`git_cleanup`.

**Fast-forward main:** `git fetch origin main && git pull --ff-only origin main`.
A refusal -> report the local and remote commits; never create a merge bubble
or reset main to make it pass.

**Commit the engine pin** (tracking fork, after `self_update`): stage only
`.sc-state/engine.ref`, then `SC_SHELL_FLAVOR=admin git commit -m "chore: update subfloor engine pin"`.
Set the marker even inside an Admin shell: the update may have replaced the
pre-commit hook under a session launched by the old floor. Add the root `sc`
dispatcher only when the update changed it. Never force-add `.super-coder/`,
snapshots, `_sc` renders, or `engine.ref.prev`. Push only within the
operator's requested update workflow.

**Merge an approved PR** only when the FnB names it. Re-read live state first:

```bash
gh pr view <number> --json url,headRefOid,baseRefName,mergeable,mergeStateStatus,statusCheckRollup
```

Require the expected repository, `baseRefName=main`, the reviewed head, a
mergeable state, and green required checks; merge with the repository's
approved method; then `git pull --ff-only origin main`. A changed head, a red
or pending check, or a merge refusal invalidates the authorization: stop and
return the live evidence. For a stack, retarget each remaining PR to `main`
before merging the one above the PR that landed (the `git` skill).

**Source repository** (`git ls-files --error-unmatch .super-coder/schema.sql`
exits 0): `.super-coder/` is tracked source and `engine.ref` is not the
delivery unit. Engine changes still arrive by Developer branch and PR; you
fast-forward main and merge the exact approved PR. Live migrations and engine
restarts run only through their named procedures in the operator's recovery
window.

**Stop:** no approval -> no merge. Foreign worktree activity -> preserve and
surface it. Main cannot fast-forward -> report divergence. Target repository,
PR head, or checks differ from the authorization -> stop.
