# molecule-dev

Molecule AI codebase conventions, quality standards, past bugs, and coordination workflows. Agents operating in Molecule AI workspaces load these rules automatically.

## What it provides

### Codebase conventions (`rules/codebase-conventions.md`)

Patterns, idioms, and anti-patterns specific to the Molecule AI codebase. Covers:
- Python style (type hints, docstrings, error handling)
- Go conventions (context usage, error wrapping)
- Directory structure and naming
- Deprecation policy

### Review loop skill (`review-loop`)

Guides the agent through a structured review before each commit:
1. Scope check — does the diff match the ticket?
2. Style check — conventions followed?
3. Test check — coverage sufficient?
4. Security check — secrets or injection risks?
5. Sign-off — agent declares the change ready

## Install

### In org template (org.yaml)

```yaml
plugins:
  - molecule-dev
```

### From URL (community install)

```
github://Molecule-AI/molecule-ai-plugin-molecule-dev
```

## Runtimes

- `claude_code` — primary
- `deepagents` — supported
- `hermes` — supported

## Architecture

```
rules/
  codebase-conventions.md   # Prose rules loaded into agent memory
adapters/
  claude_code.py            # Registers rules + review-loop skill
skills/
  review-loop/              # SKILL.md + scripts/
runbooks/
  local-dev-setup.md        # Setup guide for contributors
```

## Known issues

See [known-issues.md](known-issues.md).

## License

Business Source License 1.1 — © Molecule AI.
