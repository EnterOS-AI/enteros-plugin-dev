# Known Issues

Active and recently resolved issues for `molecule-dev`.

---

## Active Issues

*(None currently open. This section is updated when issues are filed.)*

---

## Recently Resolved

### [RESOLVED] plugin.yaml Merge Conflict Residue

**Severity:** P2
**Resolved in:** v1.0.0

**Symptoms:** `plugin.yaml` contained residual merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) that caused YAML parsing to fail. The `runtimes:` section listed `claude_code`, `deepagents` in the main branch while the working copy attempted to add `hermes`.

**Cause:** A `git stash` operation was used to temporarily discard local changes; on `git stash pop`, the conflicted state was re-applied and committed without conflict resolution.

**Fix:** Resolved by overwriting `plugin.yaml` with clean, conflict-free content. The file now has 3 runtimes declared and the `rules:` section populated.

**Prevention:** Never `git add` a file containing conflict markers. Use `git add <file>` only after `<<<<<<<` markers are fully removed, or use `git mergetool`.

---

## Known Gotchas

These are not bugs but behaviors that may surprise contributors:

### `rules/` section missing from plugin.yaml

**Symptoms:** Adding a new rule file and referencing it in `plugin.yaml` may silently fail if the `rules:` key is absent.

**Workaround:** Verify `plugin.yaml` contains the top-level `rules:` key before adding rule references. If absent, add it:

```yaml
rules:
  - rules/codebase-conventions.md
  - rules/<new-rule>.md
```

### `hermes` runtime requires adapter

**Symptoms:** Installing the plugin for a `hermes` workspace runtime works, but at runtime the adapter import may fail if `plugins_registry` is not installed in the harness environment.

**Workaround:** This is expected in isolated dev environments. The harness handles adapter resolution at runtime. See `runbooks/local-dev-setup.md` in the repo for local adapter testing.

### No local test runner

**Symptoms:** `npm test` / `python -m pytest` return no results — there are no unit tests in this plugin.

**Workaround:** This is by design — the plugin is a configuration package. Validation is done by the shared `validate-plugin.yml` workflow in CI. Run it locally via `gh workflow run validate-plugin.yml --ref main`.

---

## How to Update This File

When a new issue is discovered:

1. Add it under **Active Issues** using the template below.
2. Include: symptom, cause (if known), workaround, and fix (if resolved).
3. When fixed, move it to **Recently Resolved** and note the fix version.

### Issue Template

```markdown
## [TICKET-NUMBER] <Short Title>

**Severity:** P0 / P1 / P2 / P3
**Status:** Workaround / Fix in progress / Fix available / Resolved in vX.Y.Z

**Symptoms:**
**Cause:**
**Workaround:**
**Fix (if available):**
```

---

## Severity Definitions

| Level | Description |
|-------|-------------|
| P0 | Plugin fails to load entirely; no workaround |
| P1 | Core convention violated; can cause production failures |
| P2 | Non-core issue; minor impact or workaround available |
| P3 | Cosmetic; edge case; informational |

---

## Reporting

Use the Molecule-AI/internal issue tracker. Tag issues with `plugin-molecule-dev`.
