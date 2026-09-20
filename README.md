# Codeclarity

An agent skill for clearer code comments, docstrings, names, commit messages, and PR descriptions.

## Why

Comments, names, commit messages, and PR descriptions exist for a human reader. A
model can read raw code at a speed no comment needs to accommodate; a person reviewing
a diff cannot. Generated code communication has been getting this backwards: verbose
comments that narrate syntax, function names padded past what they mean, commit
messages that restate the diff, PR descriptions that repeat themselves across several
paragraphs. That verbosity makes the diff longer and the signal harder to find, which
defeats the reason these surfaces exist in the first place. Codeclarity's job is to cut
that padding: say only what a human reader could not get from the code itself, and let
everything else stay silent.

## Installation

Install with the Skills CLI:

```bash
npx skills add adinhodovic/codeclarity --global
```

For a project-local installation, omit `--global`. To install from a local checkout,
run `npx skills add . --global` from the repository root.

### Claude Code plugin

To load the plugin for a Claude Code session, clone it and pass its directory:

```bash
git clone https://github.com/adinhodovic/codeclarity.git
claude --plugin-dir ./codeclarity
```

In that session, invoke `/codeclarity:codeclarity`. Pass `--plugin-dir` on subsequent
launches as well. See Claude Code's [plugin documentation](https://code.claude.com/docs/en/plugins)
for plugin loading and distribution options.

## Usage

For a Skills CLI installation, call the skill directly:

```text
/codeclarity
```

Or ask in plain language:

```text
Improve the comments and names in this file.
```

Codeclarity can also review a pull-request description or rewrite a pasted docstring.

## Scope

- Explain intent, constraints, side effects, and non-obvious behavior.
- Remove comments that narrate syntax or repeat the code.
- Prefer precise names over generic names such as `process` or `data`.
- Keep documentation proportional and examples that clarify usage or return values.
- Preserve behavior, public contracts, and project terminology unless a rename is
  explicitly requested.

## Development

Run the local example checks:

```bash
python3 -m unittest discover -s tests -v
```

CI also checks skill discovery, the Claude plugin manifest, metadata, and skill size.
The [behavioral evaluation cases](evals/README.md) cover scope, evidence, restraint,
renaming, and verification honesty. Use them to assess model output when changing the
guidance; executable example checks alone cannot establish that an agent follows it.

## Credits

A few rules in `SKILL.md` are drawn from, or overlap with, established sources:

- Robert C. Martin, *Clean Code*, ch. 4 "Comments": a comment is an admission the code
  doesn't explain itself; fix the code first.
- Andrew Hunt & David Thomas, *The Pragmatic Programmer*: a comment that repeats the
  code duplicates knowledge, and the two can drift apart.
- Steve McConnell, *Code Complete*, ch. 32 "Self-Documenting Code": a mandated
  docstring with nothing to say is worse than none.
- Google, [CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)
  and [code review comments](https://google.github.io/eng-practices/review/reviewer/comments.html):
   describe what changed and why, and keep the description current through review;
   comment on the code, not the person.
- Chris Beams, [How to Write a Git Commit Message](https://cbea.ms/git-commit/): a
  subject line should complete "If applied, this commit will ___."
- GitHub, [How to Write the Perfect Pull Request](https://github.blog/developer-skills/github/how-to-write-the-perfect-pull-request/):
   state the PR's purpose, provide context rather than assuming shared history, and
   make readiness and requested feedback explicit.

## License

MIT
