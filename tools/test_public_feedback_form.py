from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FORM = ROOT / "public" / "feedback.html"
THANKS = ROOT / "public" / "feedback-thanks.html"
PREVIEW = ROOT / "public" / "research-preview.html"


class PublicFeedbackFormTests(unittest.TestCase):
    def test_netlify_form_is_discoverable_and_posted(self):
        html = FORM.read_text(encoding="utf-8")
        self.assertIn('name="aether-feedback"', html)
        self.assertIn('data-netlify="true"', html)
        self.assertIn('name="form-name" value="aether-feedback"', html)
        self.assertIn('method="POST"', html)
        self.assertIn('action="/feedback-thanks"', html)
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


if __name__ == "__main__":
    unittest.main()
