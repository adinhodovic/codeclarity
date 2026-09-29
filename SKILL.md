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
  version: "0.1.1"
---

# Code Clarity

Make code easier to understand without changing what it does. Improve the words around
the code and, when explicitly asked, rename identifiers so their intent is apparent.

Apply these rules in any language. Worked examples use Python and prose in
`references/before.py` and `references/after.py`, under matching section and rule headings.
Load the relevant pair when you need a demonstration. Treat context stated in a before
example as part of the input, not something to invent.

## Generic guidelines and gotchas

### What to change

Fix first whatever misleads or slows down a reader:

- Comments, docstrings, JSDoc, and API documentation
- Function, method, variable, parameter, and test names
- Commit messages and pull-request titles and descriptions
- Code-review feedback

### Stay within scope

Edit only the requested surfaces. Do not rewrite executable logic, formatting, test
behavior, or configuration unless asked. Rename identifiers only when asked; a request
to clarify local names does not authorize changing a public API. In a comments-only edit,
suggest extractions or structural refactors; do not perform them. Report significant
misleading documentation outside the scope; do not silently fix it.

### Working method

Treat the implementation, tests, and supplied context as evidence. Describe current
behavior only. Do not invent business rules, historical reasons, performance guarantees,
TODO owners, measurements, or verification results.

1. Read the relevant implementation, call sites, tests, and existing terminology. For
   commits and PRs, inspect the relevant diff and supplied motivation and verification.
2. Identify what the reader needs: purpose, constraint, side effect, failure mode,
   ownership, or reason for a non-obvious choice.
3. Remove wording that only narrates syntax or repeats an identifier.
4. State supported behavior concretely, preserving necessary qualifications.
5. Review the resulting diff against the requested scope and the final check below.

When the evidence does not reveal intent, ask a focused question. Do not guess. When
deleting a vague TODO would lose an unresolved concern, keep it and ask what it tracks.
Put planned behavior in an issue or actionable TODO, clearly separate from the current
contract.

### Apply editorial defaults

Apply this skill's editorial defaults to the requested surfaces. Read nearby text for
context and terminology, not as permission to repeat its weaknesses. Do not preserve a
style just because existing wording or recurring habit uses it.

Honor explicit project requirements for docstrings, naming, commit formats, and PR
templates. Within those requirements, remove redundant prose and state concrete meaning.
Otherwise, use this skill's defaults even when surrounding text follows a weaker pattern.
Do not ask permission for routine editorial choices within scope. No style requirement
justifies a false claim.

### When not to act

Leave clear text alone: text that already states a supported contract, reason, or
constraint without redundant narration. Do not rewrite it to swap in synonyms. Remove
redundancy even when it occurs only once or matches the surrounding style.

Preserve defined domain terms even when they sound generic. Preserve long docstrings that
document a genuinely large surface. Do not silently rewrite text inside quotations, log
messages, or test fixture literals; it may be data, not documentation.

### Preserve functional comments

Some comments drive tools or carry required notices. Preserve lint and type-checker
suppressions, formatter and coverage controls, build and generation directives, license
headers, and structured documentation tags unless explicitly asked to change them.
Edit surrounding prose without breaking their syntax, placement, or scope.

### Patterns to remove

Delete syntax narration, empty praise, and decorative warnings. Replace vague verbs and
inflated claims with supported behavior; delete them when they add no information.
Delete recent-refactor narration from permanent comments. State the local constraint, not
an unsupported comparison with related code. Keep any real warning, qualification, or
domain term carried by the wording you remove.

### Code review comments

Comment on the code, never the person. Follow the project's feedback labels; absent a
convention, use `Nit:` for minor non-blocking details and `Optional:` or `Consider:` for
suggestions. State required changes and their reasons explicitly. When a review explanation
contains information future maintainers need, ask for it in the code or its
documentation, not only in the review tool. Edit only within scope.

### What to return

For pasted code or prose, return the revision and a brief note of meaningful changes.
For a named file, edit within scope and report what changed. For a review, lead with
actionable findings, give file/line references when available, and separate misleading
documentation from stylistic preferences. When no change is warranted, say so briefly.

### Final check

- Every factual claim is supported, including verification and reasons for changes.
- Comments add intent or a non-obvious constraint rather than narrating syntax.
- Cross-references support a locally stated constraint; claims about related code
  have been verified.
- Names are specific without being verbose and preserve domain vocabulary.
- The diff stays in scope and preserves behavior, contracts, and functional comments.
- Renames update references and documentation without leaving stale names.
- The result sounds like a developer explaining this code to another developer.

## Code comments and docstrings

### Comments

#### Explain intent

Write comments that preserve information the code does not make obvious. State the
constraint or consequence directly. Do not repeat a visible operation; the second copy
drifts out of sync.

#### What a useful comment contains

Keep a non-required comment only when it supplies information beyond the visible code,
answering a question such as:

- Why is this branch, order, workaround, or limit required?
- What side effect or invariant must a future change preserve?
- What does a caller need to know before using this function?
- What does a non-obvious error or fallback mean?
- What unit, range, or coded value is not already explained by the name and type?

#### What to remove

Remove empty praise, commented-out obsolete code, person/date attributions that belong
in version control, and end-of-block markers already clear from syntax or indentation.
Do not restructure the code just to eliminate a comment.

Make every new TODO name an actionable next step or link to tracked work. Include a real
owner or condition when it is known and useful, following the project's convention. Do
not invent missing details to make a TODO look complete.

#### Do not explain obvious configuration

Framework declarations, class names, option values, and straightforward assignments
explain themselves. Remove comments that only paraphrase visible configuration. Keep a
comment that records a non-obvious constraint or explains why a default or alternative
would be unsafe.

#### Document inherited behavior at the parent

Put shared contracts and ownership rules on the parent abstraction. On a child,
document only what it adds, overrides, or does differently.

#### Generalize repeated rationale

When a workaround repeats, explain its shared reason once, at the common abstraction or
enclosing scope where readers will find it. Keep local comments only for differences.

#### Don't cite a named sibling as unverified evidence

State the local constraint first. Keep a cross-reference only when it supplies supporting
evidence, explains a necessary relationship, or identifies code that must change together.
Verify claims about related code; a reference alone does not keep them accurate. When the
rationale comes from a shared rule, document, or tracked migration, cite that source.

#### Shared conventions

Do not repeat framework, library, or project conventions in every comment or docstring.
Explain the local exception or constraint a reader would miss.

#### Describe the contract, not the mechanism

Lead with what the code guarantees or requires. Omit routine helper sequences and
query-by-query narration. When precedence, failure modes, or supported cost or freshness
guarantees matter to the reader, explain them.

Keep implementation rationale a maintainer needs: an upstream bug, library limitation,
protocol requirement, or lock a caller must hold. Summarize the constraint locally and
link supporting evidence when it adds something. Explain why ordering matters even when
the call site is easy to find.

#### Do not defend against hypothetical code

Do not explain an expression by describing helpers or refactors that might be added
later. When a defensive option protects a real invariant, state the invariant. Otherwise
let the expression speak for itself.

#### Replace a comment with a name

When a comment only labels an expression and a named variable or function would make
the expression easier to understand, extract one if refactoring is authorized; otherwise
suggest it. Preserve short-circuiting, evaluation order, and side effects. Check that the
name describes the expression; names go stale too.

### Docstrings

#### Keep docstrings standalone

Explain the core contract where the reader uses it. Link specifications, design
decisions, or upstream issues as support, but never make readers follow a link to learn
required inputs, outputs, or failure behavior.

#### Do not restate the entry point

Lead with behavior the name cannot express: ambiguity handling, idempotency, side effects,
or failure behavior. Remove opening sentences that merely expand the function name. When
no non-obvious contract remains, remove the docstring unless it is explicitly required.

#### Summarize complex behavior as a list

For several distinct rules, write a short list of inputs, precedence, fallbacks, side
effects, or edge cases, not a dense paragraph. Number the list when precedence matters;
use bullets for independent constraints. Do not list every implementation step.

#### Keep documentation proportional

Use the smallest form that communicates the contract: no comment for obvious code, one
line for a simple purpose, a longer block for inputs, outputs, errors, and constraints.
Remove empty sections and boilerplate. When a docstring is explicitly required but the
name already communicates the behavior, write the shortest accurate summary that satisfies
the requirement. Do not delete useful details for length alone.

#### Examples when clearer than prose

Add an example when it clarifies an input/output shape, unfamiliar API, or misuse risk
better than prose. Do not add one just to make a docstring look complete. Keep it small
and self-contained.

### Tests

#### Let test names carry the scenario

Name each test for its behavior and important conditions. Remove comments that repeat
fixture setup or assertions; keep those explaining a non-obvious regression or constraint.
Remove non-required module and class docstrings that add nothing beyond the test names.

## Method and function names

### Name the behavior

Name the action, result, unit or boundary, or boolean question.

### Avoid generic names

Within an authorized naming edit, replace vague names with the specific behavior or
role the evidence supports. Keep domain terms; do not replace them with supposedly
clearer synonyms. Do not add redundant type words to names that already have strong
context, and do not infer a business meaning from arithmetic. When the domain itself is
unclear, ask.

### Rename safely

Check scope and references before renaming. Preserve public names, serialized keys,
protocol fields, reflection-based lookups, and framework conventions unless the user
explicitly includes them. Use symbol-aware rename tooling when available, then inspect
the diff for references it missed. Verify changed call sites and relevant behavior.

## Commit descriptions

### Write the summary for a reader scanning history

Write a short, standalone imperative summary naming the concrete change. Keep it to
about 50 characters, capitalize it, and omit a trailing period. Separate the body with a
blank line. Follow explicitly required formats such as Conventional Commits, and depart
from these defaults only where the requirement conflicts. Do not copy vague subjects or
inconsistent tense from recent history.

### Explain the rationale

Explain the motivating problem, reasoning, constraints, and known shortcomings. When the
rationale depends on what changed, summarize it without narrating the diff. Keep essential
context in the message and use links only as a supplement; links rot. Omit the body when
the summary is sufficient.

### Avoid vague or inflated wording

Name the actual change, not its supposed importance or quality. Apply "Patterns to
remove" here and to PR titles.

### Do not leave review artifacts in the message

Describe the change that belongs in permanent history. Drop reviewer names, feedback
chronology, and references to fixes of earlier drafts. When the supplied review summary
lacks substance, inspect the diff or ask; do not invent a different change.

### Call out breaking changes and follow-up work

State public-contract changes, migrations, and known follow-up work in the body. Follow
the project's breaking-change format so readers and release tools can identify it.

## PR descriptions

### Describe the change

Lead with the problem and explain the approach in concrete nouns and observable
behavior. Do not assume readers know the history. Use a paragraph for a single change
and bullets for distinct outcomes. Remove file-by-file changelogs and unsupported claims
of performance, security, compatibility, or quality.

For a draft or exploratory PR, state its readiness and, when known, the feedback wanted;
do not imply it is ready to merge. Before finalizing, recheck the description against
the current diff, including changes made during review.

### Show verification

Report meaningful evidence and verification gaps. Do not imply that added coverage ran,
or that a planned check passed. When the evidence is unavailable, say so or ask.

Include manual or unusual checks, limitations, and results a reader needs to interpret
the change. When routine CI results are already visible and the template does not require
them, summarize or omit them. When a meaningful check needs exact commands to reproduce,
include them.

### Keep PR descriptions narrow

Keep relevant scope, supported counts, exceptions, and outcomes. Remove review history,
implementation chronology, and detailed test logs from the description. Organize the
remaining material around the problem, approach, and verification. Retain the author's
structure when it already serves that order, and honor required template sections.

### Call out breaking changes and follow-ups

Make migrations, deprecations, and required follow-up work visible; do not bury them in
a summary paragraph.

### Omit sections that do not apply

Preserve required template sections and checklists, including required non-applicability
answers. Remove optional empty sections instead of filling them with boilerplate. Add
sections when the change needs a migration note, rollback plan, or screenshot.
