# Repository Guidelines

## Project Structure & Module Organization
- Keep source in `src/`; tests in `tests/`; docs in `docs/`; helper scripts in `scripts/`; static assets in `assets/`.
- Example layout:
  - `src/` — implementation modules
  - `tests/` — mirrors `src/` (e.g., `tests/<module>/test_<file>.py` or `<file>.spec.ts`)
  - `docs/` — architecture notes, ADRs, how‑tos
  - `scripts/` — repeatable tasks (format, lint, release)

## Build, Test, and Development Commands
Prefer `make` targets when available; otherwise use the ecosystem defaults.
- `make dev` — run local dev server or watcher
- `make build` — produce a release build
- `make test` — run unit tests with coverage
- JavaScript: `npm run dev|build|test`
- Python: `python -m pytest -q`; coverage with `pytest --cov src`

## Coding Style & Naming Conventions
- Indentation: 2 spaces; max line length 100.
- Files: kebab-case for JS/TS; snake_case for Python; PascalCase for class files when idiomatic.
- Identifiers: `snake_case` (Python), `camelCase` (JS/TS), `PascalCase` for classes/types.
- Formatting: Prettier (JS/TS) and Black (Python). Run `scripts/format` or `make fmt`.
- Linting: ESLint (JS/TS) and Ruff/Flake8 (Python). Run `scripts/lint` or `make lint`.

## Testing Guidelines
- Frameworks: Jest/Vitest (JS/TS) or Pytest (Python).
- Naming: `tests/<package>/test_*.py`, `*.spec.ts`, or `*.test.ts` mirroring `src/` paths.
- Coverage target: 85%+ lines. Add focused unit tests for new code; include regression tests for bug fixes.
- Run locally before pushing: `make test` (or `npm test` / `pytest`).

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`, `refactor: ...`, `test: ...`.
- Keep commits small and scoped; include rationale in the body when non-obvious.
- PRs must include: clear description, linked issue (e.g., `Closes #123`), screenshots for UI, and test evidence (output or coverage).
- Ensure CI is green and all linters/formatters have been run.

## Security & Configuration Tips
- Never commit secrets. Use `.env.local` for developer overrides and provide `.env.example` with safe defaults.
- Validate inputs and avoid shelling out without sanitization in scripts.
- Review third-party licenses before adding dependencies and pin versions where possible.

