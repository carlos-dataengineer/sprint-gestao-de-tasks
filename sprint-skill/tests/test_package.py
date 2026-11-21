from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "assets" / "sprint.html"


class SprintPackageTests(unittest.TestCase):
    def test_skill_has_required_frontmatter_and_instructions(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: sprint-task-management\n"))
        self.assertIn("assets/sprint.html", skill)
        self.assertIn("create_artifact.py", skill)
        self.assertIn("scripts/install.py", skill)

    def test_artifact_is_standalone_and_branded(self):
        html = HTML.read_text(encoding="utf-8")
        self.assertIn("<title>Sprint — Gestão de Tasks</title>", html)
        self.assertIn('textContent="Sprint — Gestão de Tasks"', html)
        self.assertIn("Squad Atlas — Plataforma de Dados", html)
        self.assertNotIn("window.claude", html)
        self.assertNotIn("claude:", html)
        self.assertIn("localStorage", html)

    def test_generator_creates_requested_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "Sprint.html"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "create_artifact.py"), "--output", str(target)],
                check=True, capture_output=True, text=True,
            )
            self.assertTrue(target.is_file())
            self.assertEqual(target.read_bytes(), HTML.read_bytes())
            self.assertEqual(Path(result.stdout.strip()), target)

    def test_installer_creates_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "Sprint.html"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "install.py"), "--output", str(target)],
                check=True, capture_output=True, text=True,
            )
            self.assertTrue(target.is_file())
            self.assertEqual(target.read_bytes(), HTML.read_bytes())
            self.assertIn("Sprint instalada", result.stdout)

    def test_demo_data_is_explicitly_fictional(self):
        html = HTML.read_text(encoding="utf-8")
        self.assertIn("DEMO", html)
        self.assertIn("Exemplo fictício", html)
        self.assertNotIn("MDP – Odonto", html)

    def test_license_and_docs_exist(self):
        for rel in ["LICENSE", "README.md", "CONTRIBUTING.md", "SECURITY.md",
                    "CODE_OF_CONDUCT.md", "docs/ARCHITECTURE.md", "docs/FEATURES.md",
                    "docs/DATA_MODEL.md", "scripts/install.py"]:
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
