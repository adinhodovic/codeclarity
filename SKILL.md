---
name: codeclarity
description: |
  Improve code comments, docstrings, method names, function names, and pull-request
  descriptions so they communicate intent clearly and naturally. Use when writing,
  reviewing, or refactoring code for readability. Remove redundant narration, vague
  wording, unnecessary verbosity, generic generated-language patterns, and names that
  obscure what the code actually does.
license: MIT
compatibility: opencode
metadata:
  audience: software developers
  scope: code communication
  version: "0.1.0"
---

# Code Clarity

Make the code easier to understand without changing what it does. Improve the words
around the code and, when explicitly requested, rename local or public identifiers to
make their intent apparent.

## What to change

Prioritize the communication surfaces that mislead or slow down a reader:

- Comments and inline explanations
- Docstrings, JSDoc, and API documentation
- Function, method, variable, parameter, and test names
- Pull-request titles and descriptions
- Explanations in code review comments

Do not rewrite executable logic, formatting, tests, configuration, or public API names
unless the user asks for that change. A clearer name must still preserve the identifier's
scope, conventions, and domain meaning.

## Working method

Treat the code as evidence. Do not infer an invariant, performance property, business
rule, or historical reason that the code does not support.

1. Read the surrounding implementation, call sites, tests, and existing terminology.
2. Identify what a reader needs to know: purpose, constraint, side effect, failure mode,
   ownership, or reason for a non-obvious choice.
3. Remove wording that only narrates syntax or repeats the identifier.
4. Rewrite from the behavior outward. Prefer a short concrete statement over a general
   claim about quality, importance, or elegance.
5. Check that every factual claim remains supported and that the change did not alter
   behavior or the project's naming style.

When the implementation does not reveal the intended behavior, ask a focused question
instead of guessing. It is better to leave a comment imperfect than to document a false
contract.

## Comments and docstrings

### Explain intent

Comments earn their place when they preserve information that is not obvious from the
code. State the constraint or consequence directly.

```ts
// Good: records the reason the order matters.
// Process newest events first so a later event cannot be overwritten by an older one.
events.sort((a, b) => b.timestamp - a.timestamp);

// Bad: narrates the syntax.
// Sort the events by timestamp in descending order.
```

```python
def retry_after(response: Response) -> int:
    """Return the server's retry delay, falling back to one second."""
    return response.retry_after or 1
```

### What a useful comment contains

Prefer comments that answer one of these questions:

- Why is this branch, order, workaround, or limit required?
- What side effect or invariant must a future change preserve?
- What does the caller need to know before using this function?
- What does a non-obvious error or fallback mean?

### What to remove

Avoid comments that:

- Repeat the next line or the function name
- Describe routine control flow such as "loop through items"
- Use vague praise such as "efficiently handles" or "seamlessly integrates"
- Promise behavior the implementation does not guarantee
- Describe an old implementation outside a migration note or changelog
- Add a TODO without an owner, condition, or actionable next step

### Do not explain obvious configuration

Framework declarations, class names, option values, and straightforward assignments
already explain themselves. Do not add a comment that paraphrases visible configuration.
Keep a comment only when it records a non-obvious constraint or a reason the default
would be unsafe.

**Before:**

```python
# Read-only endpoint with no pagination. The collection is small, so this disables
# writes and returns every item.
class ItemViewSet(ReadOnlyModelViewSet):
    pagination_class = None
```

**After:**

```python
class ItemViewSet(ReadOnlyModelViewSet):
    pagination_class = None
```

### Document inherited behavior at the parent

Put shared contracts, ownership rules, and general behavior on the parent abstraction.
Child classes should document only what they add, override, or do differently. Do not
repeat inherited behavior in every child description.

**Before:**

```python
class SpecificRecord(ScopedRecord):
    """Uses the shared scope hierarchy and inherited precedence rules. It is owned by
    one of several actors, with the narrowest scope winning. The shared base handles
    the scope fields and resolution behavior."""
```

**After:**

```python
class SpecificRecord(ScopedRecord):
    """Select records by attribute criteria or explicit membership."""
```

### Generalize repeated rationale

When the same workaround appears in several places, describe the shared reason and
observable result once, using the shortest wording that remains clear. Do not repeat
framework option names, decorator mechanics, or the full implementation rationale at
each occurrence.

**Before:**

```python
# The field has choices, so the admin would show the choice label in the list. Use a
# method with a display decorator to return the stored value instead.
```

**After:**

```python
# Show the stored value rather than its display label.
```

### Shared conventions

If a framework, library, or project convention is documented elsewhere, do not repeat
it at every definition. State only the local distinction that a reader could miss.

**Before:**

```python
# Uses the shared catalog, not a record-specific value.
```

**After:**

```python
# This definition supports several related fields, mirrors a legacy collection,
# and must not be joined to other record-level fields.
```

### Keep docstrings standalone

Docstrings should explain the contract where the reader uses it. Do not make them
depend on external documents, section numbers, implementation history, workflow plans,
or long nested business examples.

**Before:**

```python
"""Apply a manual override to one scope, or to all scopes when it is empty."""
```

**After:**

```python
"""See docs/example.md section 9 for the workflow. This is used when one team
changes ownership of a matching item, except when a broad catalog entry matches
several different records and the administrator has to repair the result manually."""
```

### Let tooling provide navigation

Comments should explain behavior, not list consumers, call sites, related implementations,
or file references. Language servers and editors already provide symbol references and
navigation. Mention another component only when its interaction is part of the behavior
the reader must preserve.

**Before:**

```python
"""Return the shared value, falling back to the local value when it is absent."""
```

**After:**

```python
"""Used by the list view and export task; see helper.py and the related adapter
for the other implementation."""
```

### Describe constraints, not call paths

When a framework limitation explains an unusual declaration, document the limitation
and the required behavior. Do not list the model, form, admin, or save-hook names that
implement it; those references are discoverable through the language server.

**Before:**

```python
# Reverse fields must be declared here because ModelForm generation does not handle
# them automatically; the admin writes them through ItemAdmin.save_related.
```

**After:**

```python
# Declare reverse relations explicitly; automatic admin fields cover forward relations.
```

### Do not restate the entry point

The command, function, or method name already states its basic purpose. Use the
docstring for behavior that is surprising, easy to misuse, or important to preserve:
adoption rules, ambiguity handling, idempotency, side effects, or failure behavior.

**Before:**

```python
"""Seed records from the starter catalog. See data/catalog.yml and the design
document for details.

For each catalog entry, create a row when no match exists, update a matching row,
or skip the entry when several matches exist. This command is safe to run again.
"""
```

**After:**

```python
"""Seed records from the starter catalog.

- Create a row when no live match exists.
- Update exactly one matching row.
- Skip ambiguous matches for manual review.
- Run safely more than once.
"""
```

### Document current behavior

Comments must describe behavior that exists in the code today. Do not record planned
phases, future queries, unimplemented reuse, or intended schema decisions in a code
comment. Put future work in an issue, design document, or changelog instead.

**Before:**

```python
# Scope-specific mappings take precedence over tenant-wide mappings.
```

**After:**

```python
# The future resolver will use this ordering in Phase Seven.
```

### Do not narrate the diff

Code review already shows what was added, removed, or renamed. Do not use comments to
announce a new surface, compare the current code with its previous version, or preserve
commit-history context. Keep only the behavior or contract a future reader still needs.

**Before:**

```python
# New relation: it was not exposed by this serializer before, and it was not writable
# in the admin until now. It is a single-valued relation rather than a collection,
# unlike the other related fields, and uses a shorter wire name than the model field.
```

**After:**

```python
# Expose the single-valued relation under its unprefixed wire name.
```

### Do not defend against hypothetical code

Do not explain a current expression by describing joins, helpers, or refactors that may
be added later. If a defensive option protects a real invariant, state that invariant
briefly. Otherwise, let the expression speak for itself.

**Before:**

```python
# The prefetch does not join today, but this protects the count if a future relation
# is added to the query and causes row multiplication.
total=Count("items", distinct=True)
```

**After:**

```python
# Count unique related items.
total=Count("items", distinct=True)
```

### Let test names carry the scenario

Test names should state the behavior and important conditions clearly enough that a
reader can understand the case from the test declaration and assertions. Add a short
comment only for the non-obvious regression or constraint. Do not repeat the test name,
fixture setup, or every input variation in a docstring or comment.

Test modules usually do not need docstrings. A descriptive file name, test names, and
the test setup should provide the context. Add a module docstring only for a genuinely
non-obvious constraint that cannot be expressed more clearly in the code.

The same applies to test classes. Do not use a class docstring to repeat what the class
name, assertions, or implementation already show.

**Before:**

```python
"""Tests for the migration in the design document. The helper lives in another
module, uses historical models, and must be imported indirectly because of its name.
"""
```

**After:**

```python
def test_existing_behavior(...):
    assert result == expected
```

**Before:**

```python
class TestStoredValueDisplay:
    """The display method returns the raw value instead of the human-readable label."""
```

**After:**

```python
class TestStoredValueDisplay:
    def test_returns_the_stored_value(...):
        assert display_value(record) == record.value
```

**Before:**

```python
def test_list_renders_after_removed_field_is_not_selected(...):
    # Regression: the old relation caused rendering to fail for populated records.
```

**After:**

```python
def test_list_renders_after_removed_field_is_not_selected(...):
    # Regression test for the list page. It uses a real record, which may be scoped
    # narrowly or broadly, and verifies the page loads after the old field changed.
```

### Summarize complex behavior as a list

For a complex function, use a short list to state the meaningful behavior in order:
inputs, precedence, fallbacks, side effects, or important edge cases. Keep the list
focused on the contract. Do not turn it into a narrative of every query, helper, or
implementation detail.

Use an ordered list when order or precedence matters. Use an unordered list for
independent inputs, guarantees, or constraints. If a docstring has three or more
distinct rules, prefer a list over a dense paragraph.

**Before:**

```python
"""Select values for a record in this order:

1. Use the specific override.
2. Fall back to the shared default.
3. Keep the legacy value when no override exists.

Return an empty list when no value is available.
"""
```

**After:**

```python
"""Build the result with several subqueries, joins, annotations, and fallback
expressions. First the query checks one relation, then another helper reuses the
same expression, while a later condition handles null values and avoids row
multiplication in the generated SQL. See the implementation for details.
"""
```

### Explain complexity for humans

When a function is complex, document the decisions a reader must understand rather than
the mechanics a debugger can inspect. Cover the contract, meaningful precedence, why a
non-obvious strategy is used, and any important cost or freshness guarantee. Omit
internal helper names, query syntax, cache implementation details, and references to
the function's other methods unless they are part of the public contract.

**Before:**

```python
"""Use helper A, then helper B, which each query relation C. The prefetched values
are reused by one method but not another, so the sets are materialized before the
loop. The ranking is kept in Python instead of SQL because the queryset is small.
"""
```

**After:**

```python
"""Return the best matching candidate, or ``None`` when there is no match.

Candidates are ranked from most specific to least specific. The small candidate set
is ranked in Python, related values are loaded once per call, and results are rebuilt
on every call so changes are not hidden by stale state.
"""
```

### Keep documentation proportional

Use the smallest form that communicates the contract:

- No comment for obvious code
- One line for a simple purpose
- A short block for inputs, outputs, errors, side effects, or constraints
- A short, generic example only when it explains a non-obvious gotcha or misuse risk

### Examples only for gotchas

Do not add examples just to make a docstring look complete. If there is no important
gotcha, keep the docstring concise and omit the example. When an example is needed, use
one small self-contained snippet rather than involving multiple files, types, or related
functions.

**Keep:**

- Keep docstrings proportional to the contract.
- Add one short, generic example when it explains a non-obvious gotcha or misuse risk.
- Use a self-contained snippet rather than involving multiple files, types, or related
  functions.

**Avoid:**

- Turn every function into a mini-essay.
- Add examples just to make a docstring look complete.
- Add sections such as "Key Features", "Implementation Details", or "Important Notes"
  unless they carry distinct information.
- Add an example when the behavior is straightforward and there is no important gotcha.

### Document local exceptions

Do not repeat standard framework, library, or project conventions that are documented
elsewhere. Explain only the local exception, constraint, or reason this code differs.

**Before:**

```python
# The framework creates an implicit field from its configured field class.
# The type checker cannot infer the field type, so this annotation declares it.
record_id: int
```

**After:**

```python
# Type-only declaration for the type checker; the framework creates the field.
record_id: int
```

## Names

Choose names that say what the value or operation means at its use site.

### Name the behavior

```ts
// Before
function process(data: Item[]) {
  return data.filter((x) => x.active);
}

// After
function selectActiveItems(items: Item[]) {
  return items.filter((item) => item.active);
}
```

Use names that reveal:

- The action: `parseConfig`, `expireSession`, `sendInvoice`
- The result: `activeUsers`, `requestTimeoutMs`, `normalizedEmail`
- The unit or boundary: `timeoutMs`, `userId`, `bodyBytes`
- The boolean question: `isExpired`, `hasPermission`, `canRetry`

### Avoid generic names

Avoid generic names such as `process`, `handle`, `doThing`, `data`, `info`, `result`,
`value`, and `temp` when a more specific name is supported by the code. Do not replace a
domain term with a supposedly clearer synonym. Consistency with the surrounding code is
part of clarity.

### Rename safely

Before renaming an identifier, check its scope and references. Preserve public names,
serialized keys, protocol fields, reflection-based lookups, and framework conventions
unless the user explicitly includes them. If a name is technically accurate but the
domain itself is unclear, ask rather than inventing terminology.

Do not add noise to names that already have a strong type or context. `usersById` is
useful; `userDataCollectionMap` is not automatically better.

## Pull-request descriptions

### Describe the change

Write the description for a reviewer who needs to understand the change quickly. Cover
the problem, the approach, and verification. Use concrete nouns and observable behavior.

```md
## Summary

Reject expired session tokens before loading the user record. This prevents an expired
session from reaching handlers that assume authentication has already succeeded.

## Verification

- Added coverage for expired, valid, and missing tokens.
- Ran `pnpm test auth`.
```

Avoid:

- "This PR enhances", "improves", or "streamlines" without saying how
- A changelog of every file touched
- Claims about performance, security, or compatibility without evidence
- Generic sections that contain no information
- Describing the implementation as "robust", "seamless", "scalable", or "clean"
  instead of stating the behavior

### Show verification

State what was tested, checked, or intentionally left unverified. Do not claim confidence
that the available evidence does not support.

### Keep PR descriptions narrow

A concise PR description should cover the problem, the relevant data or scope, and the
solution. A short paragraph can provide context, but center concrete outcomes, counts,
exceptions, and changes in short lists. Preserve the repository's existing Markdown
structure; this skill improves the wording and focus, not the author's choice of headings
or layout. Leave review history, implementation chronology, and detailed test logs in the
diff or issue.

Do not restate routine CI, test, lint, format, or build commands that the repository
already runs by default. Mention verification only when it is unusual, manual, limited,
or important for interpreting the change.

**Before:**

```text
Ran the unit tests, integration tests, linter, formatter, type checker, and full CI
pipeline. All checks passed successfully.
```

**After:**

```text
Re-derived the expected data changes from the source spreadsheet and confirmed the
result matched the diff. The two unmatched source rows were left unchanged.
```

**Before:**

```text
This change follows a review of the starter catalog and several follow-up passes over
the generated spreadsheet. The review found that some items could legitimately use more
than one category, but the source suggestions were not uniformly reliable.

- Problem: Many entries had only one accepted category.
- Data: Some suggestions contradicted descriptions, and two source rows had no committed
  match.
- Verification: The catalog tests passed and the generated update set matched the diff.

This change comes from a review of the starter catalog and several follow-up passes over
the generated spreadsheet. During that review, we noticed that a number of entries had
only one category even though the same kind of item can legitimately be represented by
several categories depending on the site and the way the item is performed. The original
spreadsheet included suggested additions, so the first version of this change applied
those suggestions broadly and then went back through the results to look for cases where
the suggestion did not agree with the description.

There are a few exceptions worth calling out. Some suggestions were rejected because
the description explicitly ruled out the proposed category. One entry had a suggestion
that appeared to match a similar word rather than the actual item. Two other spreadsheet
rows could not be matched to the committed catalog because the source and repository had
drifted. Those cases are described here so the reviewer has the full history of the
investigation.

The change was checked with the catalog test suite. I also regenerated the expected
changes from the spreadsheet, compared that result with the diff, checked for unrelated
formatting changes, and verified the manually corrected entries one by one.
```

**After:**

```text
The catalog review found 447 records whose accepted categories needed checking.

- Problem: Some records accepted only one category even though the same item can use
  several.
- Data: 447 candidates were reviewed. 445 matched committed records; 8 suggestions were
  corrected because they contradicted the descriptions; 2 unmatched source rows were
  left unchanged.
- Solution: Merge valid additions into each existing category list, preserving order and
  removing duplicates. No new category values are introduced.
```

## Patterns to remove

These patterns often make generated code communication sound unnatural or unhelpful:

- `// This function is used to...` when the function can be described directly
- `// Here we...`, `// Now we...`, and `// First, we...` narration of syntax
- `// Important:` or `// Note:` used as decoration rather than a real warning
- `// Handle errors` or `// Process data` without naming the error or data
- `This ensures...` when the exact guarantee can be stated
- `In order to`, `utilize`, `functionality`, and other inflated wording
- Comments that restate a recent refactor: `// Changed from...`, `// Previously...`
- Names such as `doWork`, `processData`, `handleThing`, `getResult`, and `misc`
- PR phrases such as `minor improvements`, `various fixes`, and `updated code`

These are signals, not bans. Keep a phrase when it is the clearest wording for the
actual domain or when a project convention requires it.

## Output modes

For pasted code or prose, return:

1. The revised version.
2. A brief note of the meaningful changes.
3. A question for any missing fact needed to document behavior safely.

For a named file, edit only the requested comments, documentation, names, or PR prose.
Preserve code behavior, data, metadata, link targets, and formatting outside the target.
Then report what changed.

For a review, list only actionable findings first, with file and line references where
available. Distinguish misleading documentation from merely stylistic preferences.

## Final check

Before returning the result, verify:

- The words describe current behavior, not an imagined or previous implementation.
- Every claim is supported by the code, tests, or user-provided context.
- Comments explain intent or a non-obvious constraint rather than syntax.
- Names are specific without being verbose, and match local conventions.
- Public contracts and behavior are unchanged unless explicitly requested.
- The result sounds like a developer explaining this code to another developer.
