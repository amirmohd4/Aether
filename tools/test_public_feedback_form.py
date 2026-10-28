from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FORM = ROOT / "public" / "feedback.html"
THANKS = ROOT / "public" / "feedback-thanks.html"
PREVIEW = ROOT / "public" / "research-preview.html"
NETLIFY = ROOT / "netlify.toml"
SERVICES = ROOT / "src" / "servicesConfig.ts"


class PublicFeedbackFormTests(unittest.TestCase):

    def test_canonical_catalog_has_32_unique_nonjudicial_templates(self):
        import re

        source = SERVICES.read_text(encoding="utf-8")
        ids = re.findall(r"\{ id: '([^']+)'", source)
        self.assertEqual(len(ids), 32)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn("court-case", source.lower())
        self.assertNotIn("e-court", source.lower())

    def test_netlify_form_is_discoverable_and_posted(self):
        html = FORM.read_text(encoding="utf-8")
        self.assertIn('name="aether-feedback"', html)
        self.assertIn('data-netlify="true"', html)
        self.assertIn('name="form-name" value="aether-feedback"', html)
        self.assertIn('method="POST"', html)
        self.assertIn('action="/feedback-thanks.html"', html)
        self.assertIn('name="demo_feedback"', html)
        self.assertIn("sessionStorage", html)
        self.assertIn('name="demo_feedback"', html)
        self.assertIn("demoFeedbackField.setCustomValidity", html)
        self.assertNotIn('name="observed_example" maxlength="3000" required', html)
        self.assertNotIn('name="friction" maxlength="2000" required', html)
        self.assertTrue(THANKS.is_file())
        self.assertIn('netlify-honeypot="bot-field"', html)

    def test_form_does_not_accept_file_uploads(self):
        html = FORM.read_text(encoding="utf-8").lower()
        self.assertNotIn('type="file"', html)
        self.assertIn("do not submit real applications", html)
        self.assertIn("aadhaar/pan numbers", html)
        self.assertIn("confidential records", html)

    def test_contact_is_optional_and_consent_is_explicit(self):
        html = FORM.read_text(encoding="utf-8")
        self.assertIn('id="contact" name="contact_email" type="email"', html)
        self.assertIn('name="follow_up_consent"', html)
        self.assertIn("follow-up if you opt in", html)

    def test_confirmation_page_exists(self):
        self.assertTrue(THANKS.is_file())
        html = THANKS.read_text(encoding="utf-8")
        self.assertIn("Thank you for the critical feedback", html)
        self.assertIn('href="/feedback.html"', html)

    def test_research_preview_has_truthful_scope_and_feedback_links(self):
        self.assertTrue(PREVIEW.is_file())
        html = PREVIEW.read_text(encoding="utf-8")
        self.assertIn("Research preview", html)
        self.assertIn("simulated department systems", html)
        self.assertIn("does not access protected government records", html)
        self.assertIn("does not prove real-world time or cost savings", html)
        self.assertIn('href="/feedback.html"', html)
        self.assertIn("No government endorsement claimed", html)


    def test_preview_links_to_safe_interactive_demo(self):
        preview = PREVIEW.read_text(encoding="utf-8").lower()
        netlify = NETLIFY.read_text(encoding="utf-8")
        self.assertIn('href="/"', preview)
        self.assertIn("try the interactive synthetic sandbox", preview)
        self.assertIn("[context.deploy-preview.environment]", netlify)
        self.assertIn('VITE_API_URL = "https://aether-public-demo.onrender.com"', netlify)
        self.assertIn('VITE_REQUIRE_AUTH = "false"', netlify)
        self.assertIn('VITE_PUBLIC_DEMO = "true"', netlify)


if __name__ == "__main__":
    unittest.main()
