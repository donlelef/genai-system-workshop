# AGENTS.md

Project rules and context for AI coding agents.

## Runtime and Package manager

- Use Python 3.14
- Use **uv** for dependency and environment management (install, add deps, run scripts).
- Use `uv sync` to install dependencies and `uv run <script>` to run commands in the project environment.

## Linting & Formatting

- Pre-commit hooks run automatically on commit.
- Pre-commit also enforces [Commitizen](https://commitizen-tools.github.io/commitizen/) conventional commit messages (
  e.g. `feat:`, `fix:`, `chore:`).

## Type hints

- Use type hints on all public functions, methods, and variables where they improve clarity.
- Treat types as mandatory for new and modified code; do not defer adding them.

## Radical simplicity

- Prefer the smallest change that works: fewer abstractions, no speculative features, minimal dependencies.
- Remove or simplify before adding.

## Clear names

- Use self-explanatory names for variables, functions, modules, and types.
- Avoid abbreviations unless they are standard in the codebase.

## DRY (Don't Repeat Yourself)

- Extract repeated logic into shared functions or modules.
- Implement each behavior in one place; call or reuse instead of copying.
