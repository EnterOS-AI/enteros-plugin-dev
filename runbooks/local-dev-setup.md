# Local Development Setup

This runbook covers setting up a local development environment for
`molecule-dev`.

---

## Prerequisites

- Python 3.11+
- `gh` CLI authenticated
- Write access to `Molecule-AI/molecule-ai-plugin-molecule-dev`

---

## Clone & Bootstrap

```bash
git clone https://github.com/Molecule-AI/molecule-ai-plugin-molecule-dev.git
cd molecule-ai-plugin-molecule-dev
```

---

## Validating Plugin Structure

```bash
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"
echo "plugin.yaml OK"
```

---

## Testing the Dev Tools

Run the test suite to verify all dev tooling is functional:

```bash
python3 -m pytest tests/ -v
```

---

## Writing New Rules or Skills

1. Create `rules/<rule-name>/RULES.md` or `skills/<skill-name>/SKILL.md`
2. Follow the format of existing rules/skills in the repo
3. Validate the plugin structure (above)
4. Add tests in `tests/` if applicable

---

## Troubleshooting

### "No module named yaml"

Install PyYAML:
```bash
pip install pyyaml
```

### Plugin validation fails

- Ensure `plugin.yaml` has all required fields: `name`, `version`, `description`
- Ensure at least one of: `SKILL.md`, `hooks/`, `skills/`, `rules/`
- Check the schema with: `python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"`

---

## Related

- `skills/molecule-dev/SKILL.md` — dev tooling documentation
- `rules/` — existing rules