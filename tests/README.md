# Test Coverage Rationale — molecule-dev

## Why This Plugin Has Limited Unit-Test Coverage

`molecule-dev` is a **skill+rules plugin** — it provides codebase conventions
(rules/codebase-conventions.md) and a review-loop coordination skill
(review-loop/SKILL.md) via prose documentation.

## What We Test (and Why)

| What | Why |
|------|-----|
| `plugin.yaml` schema | Verifies all 1 rule, 1 skill, 2 adapters registered |
| `rules/` directory + file | Declared rule file exists and is non-empty |
| `skills/review-loop` SKILL.md | Frontmatter parses, body has `#` heading |
| Adapters (2) | claude_code + deepagents adapters are wired |
| `known-issues.md` | Active Issues + Severity Definitions + Reporting sections present |
| `README.md` | H1 heading, Install section, Architecture section |

## What We Cannot Unit-Test Here

- **SKILL.md prose content** — review-loop guidance is prose; its quality is
  a documentation review concern, not a unit-test concern.

- **Codebase conventions** — the rules in `rules/codebase-conventions.md` are
  prose; their correctness is a team convention concern.

## Integration Tests

If you want to test that agents use the review-loop skill correctly:
1. Install `molecule-dev` on a test workspace
2. Ask the agent to coordinate a multi-stakeholder feature
3. Verify the agent follows the Round 1 → Round 2 → Round 3 structure
4. Verify QA findings are routed back and re-verified
