## FEATURES, SPECS, AND DOCS

A feature is a `roadmap` row, alive from `brainstorm` onward. Specs
(`documents`, kind `spec`) hang off the feature, ordered by `seq`; a feature
may hold several unfrozen specs at once, and freezing one never gates the
others. A spec is **shipped** when frozen, **active** when unfrozen with rows
in `spec_tasks`, otherwise **backlog**. The **doc** (kind `doc`) is the
feature's readable face, written when its first spec ships. Bodies live in
the DB; never author a loose `.md` as the canonical copy.

Every feature belongs to a work-stream (`projects`). On every feature create,
spec author, or spec update, assess it in the same act: `sc mem get projects`;
a new feature -> `sc mem roadmap add "<title>" --project <shortname>`;
ungrouped -> `sc mem roadmap project <feature_id> <shortname>`; no fit ->
`sc mem project add <shortname> "<title>" --purpose "…"` then assign. Ask the
FnB only when several streams fit. Quick fixes need no feature.

## POSTURE, THEN CHALLENGE

Before writing: `sc mem get documents`, `sc mem get decisions`, and the repo's
own docs (`sc map-sql "SELECT path FROM dr_filepath WHERE role='doc'"`). A
spec that touches a recorded decision honors it or supersedes it explicitly
with `sc mem decision "…" --parent <id>`; never silently re-decide.
Documentation is the preferred account of intended posture; when it is absent,
ambiguous, or plausibly stale, verify the narrow code path and name that
fallback in the spec. Documentation and code disagree -> surface both to the
FnB; do not pick one as truth.

Walk the proposed workflow end to end. Challenge contradictions, missing
boundaries, hidden assumptions, audience mismatches, partial failure,
concurrent use, permissions, and the unhappy path. Ask the FnB to resolve
anything that could change implementation or acceptance; a deferral belongs in
Out of Scope with the boundary it leaves behind. The conversation is input;
the spec is the resolved contract: settled FnB decisions sit beside the clause
they govern, and an unconfirmed suggestion is never promoted to a requirement.

## THE SPEC CONTRACT

Every new spec and every substantive revision of an unfrozen spec carries:

| section | holds |
|---|---|
| `## Current Posture` | related systems and behavior before the change; documents and decisions consulted; code paths read because documentation was missing, ambiguous, or stale |
| `## Scope` → `### In Scope` / `### Out of Scope` | what this delivery adds, changes, or removes; what it deliberately excludes and the boundary retained ("not in this delivery", never "never") |
| design sections | synthesized FnB decisions and rationale beside the requirement they constrain |
| `## Anticipated User Activity` | `### Vocabulary`, `### Expected Activity`, `### Reach`, `### Audience and Assurance`, `### Data Tenancy`, `### Beyond Intention`; about 60 lines at most |

Vocabulary roster: Valid Privileged User, Valid User, Visitor, Future
Potential User, System, Shell, Unexpected Participant. Audience postures:
Unknown, Authenticated, Operational, Technical, Administrator. Separate process
curation (how much explanation a surface needs) from safety hardening
(correctness, validation, authorization, tenancy, safe failure — never waived
by expertise). Soft vocabulary, hard invariants: write anticipated activity,
Unexpected Participant, Beyond Intention, Reach, and tenancy; never threat
model, attack, adversary, exploit, abuse case, vulnerability, breach,
privilege escalation, exfiltration, or malicious. Internal-only features still
carry the section.

Author with
`sc mem doc add "<title>" --kind spec --feature <id> --body-file ./draft.md --render-path specs_sc/<slug>.md`;
`--seq` auto-advances. Body format: the `themed_markdown` skill.

## REVISE, FREEZE, DOCUMENT

Unfrozen -> edit in place: `sc mem doc edit <document_id> --body-file ./draft.md`
(also `--title`, `--render-path`); no new row, no seq bump. Frozen -> title
and body are refused; open a new spec under the same feature; only
`--render-path` still moves. When a new era makes a feature's history
misleading: create the fresh feature with its work-stream, run
`sc mem doc move <document_id> --feature <target>` (atomic across the spec,
its tasks, and document-linked decisions; refuses frozen, doc-kind, terminal,
or Sprint-bound), re-read under the target, then retitle the old feature and
set its truthful terminal status.

On the dev's docs-pending flag: `sc mem doc freeze <document_id>`; read the
shipped code, not the spec, and write
`sc mem doc add "<feature> — how it works" --kind doc --feature <id> --body-file ./draft.md --render-path docs_sc/<slug>.md`;
then `sc mem flag close <flag_id> --notes "Spec frozen; doc <id> written → docs_sc/<slug>.md"`.
Until that close, shipped + open flag is the truthful interim state.
