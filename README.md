# Codeclarity

Codeclarity improves the words around code without changing what the code does. It
focuses on comments, docstrings, function and method names, and pull-request
descriptions.

## Installation

Install with the Skills CLI:

```bash
npx skills add . --global
```

For a project-local installation, omit `--global`. The skill can also be loaded by
installing this repository as a Claude Code plugin.

## Usage

Call the skill directly:

```text
/codeclarity
```

Or ask in plain language:

```text
Improve the comments and names in this file without changing behavior.
```

Codeclarity can also review a pull-request description or rewrite a pasted docstring.

## Scope

- Explain intent, constraints, side effects, and non-obvious behavior.
- Remove comments that narrate syntax or repeat the code.
- Prefer precise names over generic names such as `process` or `data`.
- Keep docstrings short and add examples only for meaningful gotchas.
- Preserve behavior, public contracts, and project terminology unless a rename is
  explicitly requested.

## Version history

- **0.1.0** - Initial code communication skill.

## License

MIT
