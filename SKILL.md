---
name: codeclarity
description: |
  Improve the words around code. Use when writing or reviewing comments and docstrings,
  clarifying identifier names, drafting commit messages or pull-request descriptions,
  or wording code-review feedback. Preserve behavior and project terminology while
  removing redundant narration and unsupported claims.
license: MIT
metadata:
  audience: software developers
  scope: code communication
  version: "0.1.0"
---

# Code Clarity

Make code easier to understand without changing what it does. Improve the words around
the code and, when explicitly requested, rename identifiers to make their intent apparent.

These principles apply regardless of language. Worked examples use Python and prose in
`references/before.py` and `references/after.py`, under matching section and rule headings.
Load the relevant pair when you need a demonstration. Context stated in a before example
is part of the input, not something to invent.

## Generic guidelines and gotchas

### What to change

Prioritize communication that misleads or slows down a reader:

- Comments, docstrings, JSDoc, and API documentation
- Function, method, variable, parameter, and test names
- Commit messages and pull-request titles and descriptions
- Code-review feedback

### Stay within scope

Edit only the requested surfaces. Do not rewrite executable logic, formatting, test
behavior, or configuration unless asked. Rename identifiers only when requested; a
request to clarify local names does not authorize changing a public API. Suggest
extractions or structural refactors rather than performing them in a comments-only edit.
Report significant misleading documentation outside the scope instead of silently fixing it.

### Working method

Treat the implementation, tests, and supplied context as evidence. Claims must describe
current behavior. Do not invent business rules, historical reasons, performance guarantees,
TODO owners, measurements, or verification results.

1. Read the relevant implementation, call sites, tests, and existing terminology. For
   commits and PRs, inspect the relevant diff and supplied motivation and verification.
2. Identify what the reader needs: purpose, constraint, side effect, failure mode,
   ownership, or reason for a non-obvious choice.
3. Remove wording that only narrates syntax or repeats an identifier.
4. State supported behavior concretely, preserving necessary qualifications.
5. Review the resulting diff against the requested scope and the final check below.

When the evidence does not reveal intent, ask a focused question rather than guessing.
Retain a vague TODO and ask what it tracks when deleting it would lose an unresolved
concern. Put planned behavior in an issue or actionable TODO, clearly distinguished from
the current contract.

### Match existing style

Read nearby comments, docstrings, or names before rewriting. Follow established project
conventions, including required docstrings, test naming, commit formats, and PR templates.
Override them only when requested. Style conventions do not justify false claims.

### When not to act

A flagged pattern is a candidate, not a verdict. Rewrite when it improves accuracy or
readability in the requested context; one occurrence can be enough. Leave already-clear
text alone rather than changing it to demonstrate activity.

Preserve defined domain terms even if they sound generic, and long docstrings that
document a genuinely large surface. Text inside quotations, log messages, and test fixture
literals may be data rather than documentation; do not silently rewrite it.

### Preserve functional comments

Some comments affect tools or carry required notices. Preserve lint and type-checker
suppressions, formatter and coverage controls, build and generation directives, license
headers, and structured documentation tags unless changing them is explicitly requested.
Edit surrounding prose without breaking their syntax, placement, or scope.

### Patterns to remove

Watch for syntax narration, vague verbs, decorative warnings, inflated wording, and
claims about quality without observable meaning. Recent-refactor narration belongs in
history, not permanent comments. These are signals, not banned words: retain wording
when it is the clearest expression of the domain or required by project conventions.

### Code review comments

Comment on the code, never the person. Follow the project's feedback labels; absent a
convention, use `Nit:` for minor non-blocking details and `Optional:` or `Consider:` for
suggestions. Make required changes and their reasons explicit. When a review explanation
contains information future maintainers need, suggest putting it in the code or its
documentation instead of leaving it only in the review tool. Edit only within scope.

### What to return

For pasted code or prose, return the revision and a brief note of meaningful changes.
For a named file, edit within scope and report what changed. For a review, lead with
actionable findings and file/line references where available, distinguishing misleading
documentation from stylistic preferences. If no change is warranted, say so briefly.

### Final check

- Every factual claim is supported, including verification and reasons for changes.
- Comments add intent or a non-obvious constraint rather than narrating syntax.
- Names are specific without being verbose and preserve domain vocabulary.
- The diff stays in scope and preserves behavior, contracts, and functional comments.
- Renames update references and documentation without leaving stale names.
- The result sounds like a developer explaining this code to another developer.

## Code comments and docstrings

### Comments

#### Explain intent

Comments earn their place by preserving information that is not obvious from the code.
State the constraint or consequence directly. Repeating a visible operation creates a
second copy of knowledge that can drift out of sync.

#### What a useful comment contains

Prefer comments that answer one of these questions:

- Why is this branch, order, workaround, or limit required?
- What side effect or invariant must a future change preserve?
- What does a caller need to know before using this function?
- What does a non-obvious error or fallback mean?
- What unit, range, or coded value is not already explained by the name and type?

#### What to remove

Remove empty praise, commented-out obsolete code, person/date attributions better left
to version control, and end-of-block markers already clear from syntax or indentation.
Do not restructure the code just to eliminate a comment.

A new TODO should name an actionable next step or link to tracked work. Include a real
owner or condition when useful and known, following the project's convention. Do not
invent missing details to make a TODO look complete.

#### Do not explain obvious configuration

Framework declarations, class names, option values, and straightforward assignments
already explain themselves. Do not add a comment that paraphrases visible configuration.
Keep a comment when it records a non-obvious constraint or explains why a default or
alternative would be unsafe.

#### Document inherited behavior at the parent

Put shared contracts and ownership rules on the parent abstraction. Children should
document only what they add, override, or do differently.

#### Generalize repeated rationale

When a workaround repeats, explain its shared reason once at the common abstraction or
enclosing scope where readers will find it. Keep local comments only for differences.

#### Shared conventions

Do not repeat framework, library, or project conventions in every comment or docstring.
Explain the local exception or constraint that a reader could miss.

#### Describe the contract, not the mechanism

Lead with what the code guarantees or requires. Omit routine helper sequences and
query-by-query narration. Explain meaningful precedence, failure modes, and supported
cost or freshness guarantees where needed.

Keep implementation rationale a maintainer needs: an upstream bug, library limitation,
protocol requirement, or lock a caller must hold. Summarize the constraint locally and
link to supporting evidence when useful. A discoverable call site does not replace an
explanation of why its ordering matters.

#### Do not defend against hypothetical code

Do not explain an expression by describing helpers or refactors that may be added later.
If a defensive option protects a real invariant, state it. Otherwise let the expression
speak for itself.

#### Replace a comment with a name

When a comment only labels an expression, consider a named variable or function if it
makes the expression easier to understand. Perform the extraction only when refactoring
is authorized; otherwise suggest it. Preserve short-circuiting, evaluation order, and
side effects. Names can also become stale: check that the name describes the expression.

### Docstrings

#### Keep docstrings standalone

Explain the core contract where the reader uses it. Supporting links to specifications,
design decisions, or upstream issues are welcome; readers should not have to follow them
to learn required inputs, outputs, or failure behavior.

#### Do not restate the entry point

Use the docstring for behavior the name cannot express: ambiguity handling, idempotency,
side effects, or failure behavior. An obvious summary is not a substitute for a contract.

#### Summarize complex behavior as a list

For several distinct rules, prefer a short list of inputs, precedence, fallbacks, side
effects, or edge cases over a dense paragraph. Order the list when precedence matters;
use bullets for independent constraints. Do not list every implementation step.

#### Keep documentation proportional

Use the smallest form that communicates the contract: no comment for obvious code, one
line for a simple purpose, or a longer block for inputs, outputs, errors, and constraints.
Omit empty sections and boilerplate. A mandatory docstring with nothing to say invites
stale documentation; still follow an established project requirement unless asked to
change it. Length alone is not a reason to delete useful details.

#### Examples when clearer than prose

Add an example when it clarifies an input/output shape, unfamiliar API, or misuse risk
better than prose. Do not add one just to make a docstring look complete. Prefer a small
self-contained snippet.

### Tests

#### Let test names carry the scenario

Test names should state behavior and important conditions. Comments should explain a
non-obvious regression or constraint, not repeat fixture setup and assertions. Module
and class docstrings are useful only when they add context the names and tests do not
already provide, subject to project conventions.

## Method and function names

### Name the behavior

Choose names that convey the action, result, unit or boundary, or boolean question.

### Avoid generic names

Use a more specific name when the evidence supports it. Preserve domain terms rather
than replacing them with supposedly clearer synonyms. Do not add redundant type words
to names that already have strong context, or infer a business meaning from arithmetic.
If the domain itself is unclear, ask.

### Rename safely

Check scope and references before renaming. Preserve public names, serialized keys,
protocol fields, reflection-based lookups, and framework conventions unless the user
explicitly includes them. Use symbol-aware rename tooling when available, then inspect
the diff for references it may miss. Verify changed call sites and relevant behavior.

## Commit descriptions

### Write the summary for a reader scanning history

Write a short, standalone imperative summary naming the change. Check whether it
completes "If applied, this commit will ___." Without a project convention, aim for
about 50 characters, capitalize, and omit a trailing period. Separate a body with a
blank line. Follow existing tense, mood, and formats such as Conventional Commits.

### Explain the rationale

Explain the motivating problem, reasoning, constraints, and known shortcomings. Summarize
what changed when needed to understand the rationale, without narrating the diff. Keep
essential context in the message; links supplement it, since they may become inaccessible.
Omit a body when the summary is sufficient.

### Avoid vague or inflated wording

Name the actual change instead of its supposed importance or quality. See "Patterns to
remove"; the same principle applies to PR titles.

### Do not leave review artifacts in the message

Describe the change that belongs in permanent history. Drop reviewer names, feedback
chronology, and references to fixes of earlier drafts. Do not invent a different change
when the supplied review summary lacks substance; inspect the diff or ask.

### Call out breaking changes and follow-up work

State public-contract changes, migrations, and known follow-up work in the body. Follow
the project's breaking-change format so readers and release tools can identify it.

## PR descriptions

### Describe the change

Make the purpose clear and explain the problem and approach using concrete nouns and
observable behavior. Do not assume readers know the history. Use a paragraph or list
according to the material; avoid file-by-file changelogs and unsupported claims of
performance, security, compatibility, or quality.

For draft or exploratory PRs, state readiness and the kind of feedback wanted when known;
do not imply the change is ready to merge. Before finalizing, recheck the description
against the current diff, including changes made during review.

### Show verification

Report meaningful evidence and verification gaps. Do not imply that adding coverage means
it ran, or that a planned check passed. If the evidence is unavailable, say so or ask.

Include manual or unusual checks, limitations, and results important to interpreting the
change. Routine CI may be summarized or omitted when results are already visible and
the template does not require them. Include exact commands when needed to reproduce a
meaningful check.

### Keep PR descriptions narrow

Keep relevant scope, supported counts, exceptions, and outcomes. Leave review history,
implementation chronology, and detailed test logs in the diff or issue. Preserve the
author's structure unless an optional section is empty or important information needs a
section.

### Call out breaking changes and follow-ups

Make migrations, deprecations, and required follow-up work visible rather than burying
them in a summary paragraph.

### Omit sections that do not apply

Preserve required template sections and checklists, including required non-applicability
answers. Remove optional empty sections instead of filling them with boilerplate. Add
sections when the change needs a migration note, rollback plan, or screenshot.
