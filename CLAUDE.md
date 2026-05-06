# molecule-dev — Molecule AI Codebase Conventions Plugin

`molecule-dev` is a **platform conventions plugin** that captures hard-won lessons from Molecule AI's production codebase. Rather than repeating mistakes, every agent working on the platform benefits from rules derived from real bugs and production failures.

**Version:** 1.0.0
**Runtime:** `claude_code`, `deepagents`, `hermes`

---

## Repository Layout

```
molecule-dev/
├── plugin.yaml                    — Plugin manifest (runtimes, rules, skills)
├── rules/
│   └── codebase-conventions.md   — Platform-wide conventions (Canvas/Go/Python)
├── skills/
│   └── review-loop/SKILL.md      — Multi-round review orchestration workflow
└── adapters/                     — Harness adaptors (thin wrappers)
```

---

## Conventions Summary

See `rules/codebase-conventions.md` for the full ruleset. Key highlights:

### Canvas (Next.js 15 App Router)

- **`'use client'` is non-negotiable** — every `.tsx` file using React hooks or event handlers must declare it as the very first line.
- **Zustand selectors**: never call a function returning a new object inside a selector — use `useMemo` instead.
- **Dark zinc theme** — backgrounds `zinc-900`/`zinc-950`, text `zinc-300`/`zinc-400`. Never use `#ffffff` or light colors.
- **Verify API response shapes** with `curl` or Go handler inspection — don't assume.

### Platform (Go)

- **SQL safety**: always parameterized queries (`$1`, `$2`), always `ExecContext`/`QueryContext`.
- **Access control**: every workspace endpoint must verify ownership; new A2A proxy paths must pass `CanCommunicate()`.
- **Container lifecycle**: use `ContainerRemove(Force: true)` — never `ContainerStop` + `ContainerRemove` separately.

### Workspace Runtime (Python)

- **Error sanitization**: use `sanitize_agent_error()` — never emit raw exception messages or subprocess stderr to the user.
- **System prompt hot-reload**: always use `encoding="utf-8", errors="replace"` when reading prompt files.

---

## Development

### Prerequisites

- Node.js >= 18 (for markdownlint)
- Python 3.11+ (for `adapters/`)
- `gh` CLI authenticated
- Write access to `Molecule-AI/molecule-ai-plugin-molecule-dev`

### Setup

```bash
git clone https://github.com/Molecule-AI/molecule-ai-plugin-molecule-dev.git
cd molecule-ai-plugin-molecule-dev

# Install markdownlint CLI for pre-commit linting
npm install -g markdownlint-cli

# Validate the plugin structure
gh workflow run validate-plugin.yml --ref main
```

### Adapter Dev

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install plugins_registry

python -c "from adapters.claude_code import Adaptor; print('OK')"
```

### Pre-Commit Checklist

```bash
# Markdown lint
npx markdownlint '**/*.md' --ignore node_modules

# YAML validation
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"

# No pycache committed
find . -name '__pycache__' -o -name '*.pyc' | grep -v .gitignore && exit 1
```

---

## Test Commands

There are no unit tests in this plugin — it is a configuration-only package. Validation is done by the shared `validate-plugin.yml` workflow (see CI).

To run validation locally:
```bash
gh workflow run validate-plugin.yml --ref main
```

To validate `plugin.yaml` structure:
```bash
python3 -c "
import yaml, os
with open('plugin.yaml') as f:
    data = yaml.safe_load(f)
for key in ['rules', 'skills']:
    for ref in data.get(key, []):
        path = ref if ref.endswith('.md') else ref + '.md'
        print(f'[OK] {path}' if os.path.exists(path) else f'[MISSING] {path}')
"
```

---

## Release Process

1. **Review changes** — `git log origin/main..HEAD --oneline`
2. **Validate** — run `npx markdownlint` on all `.md` files
3. **Bump version** in `plugin.yaml`
4. **Commit** — `chore: bump version to X.Y.Z`
5. **Tag** — `git tag -a vX.Y.Z -m "Release vX.Y.Z"` and push
6. **Create GitHub Release** with a changelog section
7. **Verify CI green** on the release commit

---

## Key Contacts

| Role | Owner |
|------|-------|
| Platform architecture (Go/Canvas) | Molecule AI Engineering |
| Workspace runtime (Python) | Molecule AI Engineering |
| Plugin maintenance | Molecule AI Engineering |

For questions, bugs, or suggestions, open an issue in this repo or reach out via the Molecule AI internal channels.

---

## Adding a New Convention

1. Create `rules/<rule-name>.md` describing the convention.
2. Add it to `rules:` in `plugin.yaml` (and add `rules/` section if not present).
3. If it affects canvas work, include a concrete code example (BAD / GOOD pattern).
4. Run markdownlint validation before committing.

---

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`).
2. Add it to `skills:` in `plugin.yaml`.
3. Skills are the canonical workflow surface — prefer skills over commands.
