Goal: take the named issue-set through a governed delivery run that works on its own but pauses to escalate the operator's decisions, landing a PR flipped to ready for review, which the operator merges. The same standing orders run two ways — here in this session (local), or handed to a fresh cloud runner (cloud). The operator is the maintainer who invoked this skill; the canonical remote is the git remote that points at `spec-kitty/spec-kitty` (find it with `git remote -v`).

Input: the issue numbers or issue-set (parameter `issues`), the mode (parameter `mode`), optional guidance and a closeout profile. If no issue is named, ask which to run. If the mode is not given: ask whether to run here or dispatch when this session can create cloud sessions, otherwise run local.

The standing orders are identical in both modes and live in the `semi-auto-delivery` procedure — it carries the rules; this skill carries only the order and the mode fork. Load it with `spec-kitty charter context --include procedure:semi-auto-delivery`, and `--action implement` / `--action review` for the phase doctrine.

## Both modes: the order

Follow the `semi-auto-delivery` procedure end to end. Its steps, in order:

1. Orientation gate.
2. Research, grounding and discovery squads, before any spec.
3. Decide Mission vs Ops by blast radius.
4. Work autonomously, but pause and escalate on the operator's decisions.
5. Hold the brownfield standing orders.
6. Test to the calibrated blast radius, never the heavy suites.
7. Rebase on the fixed cadence.
8. Close out through the closeout step of `mission-wrap-up-sequence`. The operator merges.

## Local mode

You are the runner. Run the whole delivery in this session, following the standing orders above directly, and deliver the PR from here. Every escalation-class decision pauses THIS conversation and asks the operator before you proceed.

## Cloud mode

You are the dispatcher, not the runner. Follow the `cloud-session-dispatch` procedure to build a complete dispatch prompt (no placeholders) and spawn a fresh cloud runner against `spec-kitty/spec-kitty` at `main`, inheriting the model and environment. The prompt BINDS the semi-auto standing orders by reference — it tells the runner to load `spec-kitty charter context --include procedure:semi-auto-delivery` and follow it — instead of re-typing them, and fills in the issue-set, the per-kind doctrine for the work, the numbered slices, and the closeout profile. Report the session id, the branch and the instruction summary; never predict results; read real state back from the session before claiming any progress. Relay later operator guidance as a labelled addendum. The runner performs the escalation pauses in its own session — the prompt instructs it to surface escalation-class decisions there.

Apply the fleet controls of `cloud-session-dispatch` (capacity and collisions, settled conventions, the batched decision message, the setup fallback, the missing-skill fallback and the fleet record) and the integrity rules of `CLOUD_SESSION_ORCHESTRATION`, rather than dispatching independently.

## Stop and ask the operator when

- the mode is ambiguous and this session can create cloud sessions;
- the issue-set spans unrelated surfaces (split it into separate runs or dispatches and confirm the scope);
- any escalation-class decision arises (local: pause here; cloud: the runner pauses in its session);
- an issue is already resolved or superseded, or already claimed by someone active on it.

## Hand-off

Local: the closeout step of `mission-wrap-up-sequence` owns the flip to ready for review, which is the hand-off to the maintainers; report as its last step says and stop.

Cloud: the hand-off is the spawned session plus its dispatch summary; the runner delivers its own PR and performs its own hand-off. Do not archive or interrupt a session unless the operator asks.
