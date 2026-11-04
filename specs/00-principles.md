# Evaluation policy (DSPy practice judges)

This document is loaded by the hosted hackathon application for **evaluation only**. It governs the four permitted E12 DSPy practice judgments (criterion testability, requirement coverage, out-of-spec additions, review-comment substance). It does **not** define MCP collection behavior; see `AGENTS.md` for what tool calls store.

## Evidence-bound claims

- Every judgment must cite stored MCP events, repository snapshots, and other allowlisted evidence already persisted for the team and event window.
- Use typed missingness (`unobservable`, `not_applicable`, `discarded`) with required reason codes instead of guessing or inferring zero.
- Do not treat connection, initialize, or status instrumentation as proof of practice quality.

## Project conventions (for interpreting evidence)

- Specs use stable `REQ-` and `AC-` identifiers with human approval before `Status: approved`.
- Amendments must be explicit; do not assume silent scope change.
- Trace claims to artifact paths and ids present in evidence; do not invent repository paths or commits.

## Prohibited judgment content

Judges must not fabricate facts, uncited conclusions, or rankings. Do not claim product quality, DORA metrics, acceptance rate, suggestion volume, lines generated, or prohibited AI-usage narratives. Do not paste secrets, credentials, personal data, raw logs, or private evidence into prompts or outputs.

## Rubric boundary

DSPy modules may produce only the four cited judgments above. They must not compute participant markers, confidence, 0–5 scores, arm comparisons, Deploy facts, formulas, tiers, or report composition. Those remain deterministic services outside the model.

## Non-goals

This policy is not installed on a developer machine, does not instruct participants to download a starter kit, and does not replace MCP collection or workspace controls.
