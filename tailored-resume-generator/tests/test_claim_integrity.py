import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "tailored-resume-generator"
sys.path.insert(0, str(SKILL / "scripts"))

from validate_claims import assemble_employer_text, classify  # noqa: E402


class ClaimIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = SKILL / "tests" / "fixtures" / "unsafe-example.synthetic.json"
        cls.records = json.loads(fixture.read_text())
        cls.result = classify(cls.records)
        cls.claim_text = " ".join(item["text"] for item in cls.result["eligible_claims"])
        cls.gap_text = " ".join(item["text"] for item in cls.result["gaps"])

    def test_requirements_and_unsupported_details_are_not_claims(self):
        for unsupported in ("SQL", "A/B testing", "HIPAA", "50+", "35%"):
            self.assertNotIn(unsupported, self.claim_text)
            self.assertIn(unsupported, self.gap_text)

    def test_job_keywords_remain_requirements(self):
        requirements = [r for r in self.result["gaps"] if r["status"] == "job_requirement"]
        self.assertEqual({r["text"] for r in requirements}, {"Expert SQL experience", "A/B testing experience"})

    def test_transferable_experience_is_labeled(self):
        item = next(r for r in self.result["eligible_claims"] if r["status"] == "transferable_experience")
        self.assertEqual(item["label"], "transferable experience")

    def test_unknown_remains_unknown(self):
        hipaa = next(r for r in self.result["gaps"] if "HIPAA" in r["text"])
        self.assertEqual(hipaa["status"], "unknown")

    def test_official_title_and_dates_are_preserved(self):
        self.assertIn("Data Analyst, Northstar Retail, 2019-2024", self.claim_text)

    def test_eligible_claim_without_evidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "requires evidence_id"):
            classify([{"text": "Python", "status": "candidate_confirmed_fact"}])

    def test_employer_output_cannot_cross_evidence_boundary(self):
        employer_output = assemble_employer_text(self.records)
        for unsupported in ("SQL", "A/B testing", "HIPAA", "50+", "35%"):
            self.assertNotIn(unsupported, employer_output)

        separately_supported = self.records + [
            {
                "text": "Used SQL to prepare monthly inventory reports",
                "status": "candidate_confirmed_fact",
                "evidence_id": "candidate-note-4",
            }
        ]
        self.assertIn("SQL", assemble_employer_text(separately_supported))

    def test_fixture_is_synthetic_and_contains_no_private_subject_name(self):
        fixture_text = json.dumps(self.records).lower()
        self.assertNotIn("roblmvp", fixture_text)
        self.assertNotRegex(fixture_text, r"\brob\b")


class RepositorySafetyTests(unittest.TestCase):
    def test_private_paths_are_ignored(self):
        paths = [
            ".env", ".firecrawl/session.json", ".private/resume.pdf",
            "private/contact.txt", "private-data/profile.json", "candidate-data/resume.md",
            "career-evidence/review.txt", "application-data/app.json", "outputs/private/result.md",
            "profile.local.json", "sample.secret.txt", "credentials.json", "secrets.txt",
        ]
        check = subprocess.run(
            ["git", "check-ignore", "--stdin"], input="\n".join(paths), text=True,
            cwd=ROOT, capture_output=True, check=False,
        )
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(set(check.stdout.splitlines()), set(paths))

    def test_governance_and_resume_files_have_no_secret_like_values(self):
        files = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
        reviewed = [
            ROOT / name for name in files
            if name in {"AGENTS.md", "docs/data-and-evidence-governance.md", ".codex/config.toml"}
            or name.startswith("tailored-resume-generator/")
        ]
        forbidden = ("AKIA" + "[0-9A-Z]{16}", "sk" + "-[A-Za-z0-9]{20,}", "Bearer " + "[A-Za-z0-9._-]{20,}")
        import re
        for path in reviewed:
            text = path.read_text(errors="ignore")
            for pattern in forbidden:
                self.assertIsNone(re.search(pattern, text), str(path))


if __name__ == "__main__":
    unittest.main()
