#!/usr/bin/env python3
"""
Smoke tests for molecule-dev.

Rationale: This is a skill+rules plugin — it provides codebase conventions
(rules) and a review-loop coordination skill. Smoke tests verify all artifacts
exist and parse correctly. See tests/README.md.

Run: python tests/test_dev_smoke.py
"""
import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_manifest():
    import yaml
    with open(os.path.join(REPO_ROOT, 'plugin.yaml')) as f:
        return yaml.safe_load(f)


class TestPluginManifest(unittest.TestCase):
    """Verify plugin.yaml is well-formed."""

    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()

    def test_plugin_yaml_loads(self):
        self.assertIsInstance(self.manifest, dict)

    def test_name(self):
        self.assertEqual(self.manifest['name'], 'molecule-dev')

    def test_version_semver(self):
        v = self.manifest['version']
        self.assertRegex(v, r'^\d+\.\d+\.\d+$', f"Version {v!r} not semver")

    def test_description_present(self):
        self.assertGreater(len(self.manifest.get('description', '')), 10)

    def test_runtimes_include_claude_code(self):
        self.assertIn('claude_code', self.manifest.get('runtimes', []))

    def test_rules_declared(self):
        rules = self.manifest.get('rules', [])
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)

    def test_skills_declared(self):
        skills = self.manifest.get('skills', [])
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)


class TestRules(unittest.TestCase):
    """Verify declared rules files exist and are non-empty."""

    RULES_DIR = os.path.join(REPO_ROOT, 'rules')

    @classmethod
    def setUpClass(cls):
        cls.rules = load_manifest().get('rules', [])

    def test_rules_directory_exists(self):
        self.assertTrue(os.path.isdir(self.RULES_DIR))

    def test_each_declared_rule_file_exists(self):
        for rule in self.rules:
            filename = os.path.basename(rule)
            path = os.path.join(self.RULES_DIR, filename)
            self.assertTrue(
                os.path.isfile(path),
                f"Rule {rule!r} declared but file not found at {path}"
            )

    def test_each_rule_file_is_nonempty(self):
        for rule in self.rules:
            filename = os.path.basename(rule)
            path = os.path.join(self.RULES_DIR, filename)
            size = os.path.getsize(path)
            self.assertGreater(size, 100, f"Rule {rule!r} is suspiciously small ({size} bytes)")


class TestSkills(unittest.TestCase):
    """Verify declared skills have SKILL.md with valid frontmatter."""

    SKILLS_DIR = os.path.join(REPO_ROOT, 'skills')

    @classmethod
    def setUpClass(cls):
        cls.skills = load_manifest().get('skills', [])

    def test_skills_directory_exists(self):
        self.assertTrue(os.path.isdir(self.SKILLS_DIR))

    def test_each_declared_skill_directory_exists(self):
        for skill in self.skills:
            path = os.path.join(self.SKILLS_DIR, skill)
            self.assertTrue(
                os.path.isdir(path),
                f"Skill {skill!r} declared but directory not found at {path}"
            )

    def test_each_skill_has_skill_md(self):
        for skill in self.skills:
            path = os.path.join(self.SKILLS_DIR, skill, 'SKILL.md')
            self.assertTrue(os.path.isfile(path), f"Skill {skill!r} missing SKILL.md at {path}")

    def test_each_skill_md_has_frontmatter(self):
        import yaml
        for skill in self.skills:
            path = os.path.join(self.SKILLS_DIR, skill, 'SKILL.md')
            with open(path) as f:
                content = f.read()
            self.assertTrue(
                content.startswith('---'),
                f"{skill}: SKILL.md must have YAML frontmatter"
            )
            parts = content.split('---', 2)
            self.assertEqual(len(parts), 3, f"{skill}: SKILL.md must have opening and closing ---")
            _, frontmatter, _ = parts
            data = yaml.safe_load(frontmatter)
            self.assertIsInstance(data, dict)
            self.assertIn('name', data, f"{skill}: frontmatter must have 'name'")

    def test_each_skill_body_has_heading(self):
        for skill in self.skills:
            path = os.path.join(self.SKILLS_DIR, skill, 'SKILL.md')
            with open(path) as f:
                content = f.read()
            parts = content.split('---', 2)
            _, _, body = parts
            self.assertRegex(
                body.lstrip(), r'^# ',
                f"{skill}: SKILL.md body must start with # heading"
            )


class TestAdapters(unittest.TestCase):
    """Verify runtime adapters exist."""

    def test_claude_code_adapter_exists(self):
        path = os.path.join(REPO_ROOT, 'adapters', 'claude_code.py')
        self.assertTrue(os.path.isfile(path))

    def test_claude_code_adapter_imports_adaptor(self):
        path = os.path.join(REPO_ROOT, 'adapters', 'claude_code.py')
        with open(path) as f:
            content = f.read()
        self.assertIn('Adaptor', content)

    def test_deepagents_adapter_exists(self):
        path = os.path.join(REPO_ROOT, 'adapters', 'deepagents.py')
        self.assertTrue(os.path.isfile(path))


class TestKnownIssues(unittest.TestCase):
    """Verify known-issues.md structure."""

    KI_PATH = os.path.join(REPO_ROOT, 'known-issues.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.KI_PATH))

    def test_has_active_issues_section(self):
        with open(self.KI_PATH) as f:
            self.assertIn('Active Issues', f.read())

    def test_has_severity_definitions(self):
        with open(self.KI_PATH) as f:
            content = f.read()
        self.assertIn('Severity Definitions', content)

    def test_has_reporting_section(self):
        with open(self.KI_PATH) as f:
            content = f.read()
        self.assertIn('Reporting', content)


class TestReadme(unittest.TestCase):
    """Verify README.md has required sections."""

    README_PATH = os.path.join(REPO_ROOT, 'README.md')

    def test_readme_exists(self):
        self.assertTrue(os.path.isfile(self.README_PATH))

    def test_readme_has_h1(self):
        with open(self.README_PATH) as f:
            first_line = f.readline().strip()
        self.assertTrue(
            first_line.startswith('# '),
            f"README must start with # heading, got: {first_line!r}"
        )

    def test_readme_has_install_section(self):
        with open(self.README_PATH) as f:
            content = f.read()
        self.assertIn('Install', content)

    def test_readme_has_architecture_section(self):
        with open(self.README_PATH) as f:
            content = f.read()
        self.assertIn('Architecture', content)


if __name__ == '__main__':
    unittest.main(verbosity=2)
