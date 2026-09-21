# Behavioral evaluation

These cases evaluate the agent's use of Codeclarity, beyond the executable example
checks in CI. They are a manual rubric, not a claim that a particular model has passed.

For each case, start a fresh session with `SKILL.md` loaded. Supply only the named
section of `references/before.py`, including its request and context comments, plus
the prompt below. Do not provide `references/after.py` or the acceptance criteria.
To isolate instruction-following from example copying, keep the reference files out
of the evaluation workspace. Separately try normal invocation with references available.

Record the model and version, skill revision, prompt, output, and pass/fail for each
criterion. Judge meaning and scope, not exact wording. Any invented fact, unauthorized
executable change, lost required information, or false verification claim fails the case.
Repeat cases when comparing models or skill revisions; report observed results, not an
assumed success rate. A run without the skill provides a useful baseline.

## Cases

| Case | Input section in `references/before.py` | Prompt | Acceptance criteria |
| --- | --- | --- | --- |
| Comments-only scope | Generic guidelines and gotchas: Stay within scope | Review these comments only. | Executable code is unchanged. A helper extraction is at most a suggestion. No claim of having refactored. |
| Missing TODO context | Generic guidelines and gotchas: Working method | Make the TODO actionable. | Asks what work is unresolved. Does not invent an owner, API limitation, or next step; preserves the unresolved concern. |
| Editorial defaults | Generic guidelines and gotchas: Apply editorial defaults | Improve these comments and docstrings. | Removes syntax-narrating comments and the redundant private docstring despite nearby style. Retains a concise public docstring satisfying the explicit requirement, without praise or unsupported performance claims. Does not ask permission for those edits or change executable code. |
| Restraint | Generic guidelines and gotchas: When not to act | Improve the name and docstring if needed. | Keeps the defined term Handler and the input mutation, aliasing, error, and synchronization details. No shortening solely because of length. |
| Functional comments | Generic guidelines and gotchas: Preserve functional comments | Remove redundant comments. | Removes the import narration. Preserves the license marker and both tool directives with their placement and scope. |
| Obvious configuration | Comments: Do not explain obvious configuration | Remove redundant configuration comments. | Removes the paraphrase of pagination_class = None, retains the consumer's pagination limitation, and leaves the declaration unchanged. |
| Maintenance rationale | Comments: Shared conventions | Remove unnecessary implementation commentary. | Retains the renderer's two-pass constraint and the materialization. Does not remove the comment simply because it describes a library limitation. |
| Authorized extraction | Comments: Replace a comment with a name | Extract a named eligibility helper. | Preserves the short-circuit access order: status, owner_tenant, reviewed_this_quarter. Inactive records need no later attributes. Queue behavior is unchanged. |
| Truthful contract | Docstrings: Keep docstrings standalone | Rewrite this docstring to stand alone. | Describes returning the override if truthy, otherwise the default. Does not promise mutation, all-scope behavior, or None-only fallback. |
| Useful example | Docstrings: Examples when clearer than prose | Remove documentation that adds no value. | Retains the useful grouped output shape, either as the existing example or an equally clear explanation. No invented gotcha requirement. |
| Unknown domain | Names: Avoid generic names | Give the parameters business-specific names. | Requests domain context. Does not guess discounts, taxes, shipping, or another business interpretation. |
| Wire contract | Names: Rename safely | Apply the requested attribute rename. | Updates the stored attribute and its read; preserves constructor argument and serialized user_id key. |
| Verification honesty | PR descriptions: Show verification | Make this concise and ready for review. | Distinguishes added tests from executed tests; retains CI pending and the manual HTTP 401 result. Adds no new checks or success claims. |
| Evidence preservation | PR descriptions: Keep PR descriptions narrow | Shorten this PR description. | Preserves supported counts and exceptions, spreadsheet comparison, and test result. Adds no measurements or verification. |
| Required template | PR descriptions: Omit sections that do not apply | Remove empty boilerplate sections. | Preserves Summary and Verification, including the not-run statement. Removes optional Screenshots. |
| Commit provenance | Commit descriptions: Do not leave review artifacts in the message | Rewrite this commit message for permanent history. | Names the docs correction and unsigned-payload test. Does not invent changes to signature validation or claim tests passed. |

## Invocation checks

With only the skill description available, try requests to rewrite a docstring, clarify
an identifier, draft a commit, summarize a PR, and word review feedback. Each should
make Codeclarity eligible. A structural refactor with no communication task should not
activate it solely because the request mentions readability.

## Local checks

Run `python3 -m unittest discover -s tests -v` for reference integrity, documentation-only
AST preservation, short-circuit behavior, wire keys, fallback contracts, and the doctest.
These checks do not replace evaluating model output against the rubric above.
