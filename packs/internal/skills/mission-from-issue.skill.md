Goal: take the named issues on the canonical repository through a full governed Mission to a pull request that is green and flipped from draft to ready for review. The operator is the maintainer who invoked this skill; the canonical repository is the repository the work targets, and the canonical remote is the git remote that points at it (find it with `git remote -v`). In a fork clone, run `gh repo set-default` once so `gh` targets the canonical repository. Labels, test commands, the changelog mechanism and the PR template are the ones the repository's own charter or contributor docs define.

Input: the issue numbers the user names (parameter `issues`), optionally followed by guidance (parameter `guidance`). If no issue is named, ask which to run. Record the guidance in the Mission spec. Scale the review effort to the work: a small fix needs a couple of reviewers per round; a contract or API-surface change needs the full adversarial treatment.

## Steps

Follow the `issue-to-mission-delivery` procedure. It carries the rules and the commands; this list is the order:

1. Start from the current `main` of the canonical remote (fast-forward only, push nothing). Read the charter.
2. Ground the issues: confirm each still reproduces on current main and was not superseded, and set the Mission boundary.
3. Claim every issue (comment, assign the operator, add the repository's claim labels if it has them) and verify it before any planning artifact exists.
4. Specify, plan and tasks through the canonical commands; fill the issue matrix; keep the tracer files.
5. Survey the existing code, then implement red-first where the change carries a lasting regression risk (record real-run or gate evidence for configuration and glue work) with `spec-kitty next --agent <name> --mission <slug>`.
6. Run the `mission-wrap-up-sequence` procedure end to end: accept, issue verdicts, aggregate review, consolidate, compact, rebase, changelog and docs, pre-PR review and folds, PR body, then its closeout step. Add the repository's human-owned label to the PR when the closeout opens it, if it has one.
7. Add the repository's ready label to the PR after the closeout's flip, if it has one.

Every subagent you dispatch loads its profile as `adversarial-squad-deployment` describes. Use the cheaper model tier for implementation and the stronger tier for review.

## Stop and ask the operator when

- every issue is resolved or superseded (stop and report), or only some are (drop them and confirm the remaining scope);
- an issue is already assigned to someone active on it, or a claim fails;
- `main` cannot fast-forward or the working tree is not clean;
- a work package is rejected twice or blocked.

## Hand-off

The closeout step of `mission-wrap-up-sequence` owns the flip to ready for review, which is the hand-off to the maintainers. Report as its last step says, then stop: the operator merges.
