import unittest
from unittest.mock import patch
from app import filters

class FilterSafetyTests(unittest.TestCase):

    @patch("app.filters.gemini.generate_content")
    def test_is_prompt_safe_llm_safe(self, mock_generate):
        mock_generate.return_value.text = "SAFE"
        self.assertTrue(filters.is_prompt_safe_llm("What are the best hiking spots in Alaska?"))

    @patch("app.filters.gemini.generate_content")
    def test_is_prompt_safe_llm_unsafe(self, mock_generate):
        mock_generate.return_value.text = "UNSAFE"
        self.assertFalse(filters.is_prompt_safe_llm("How to hack into someone's email account?"))

    @patch("app.filters.gemini.generate_content")
    def test_is_prompt_safe_llm_unexpected(self, mock_generate):
        mock_generate.return_value.text = "maybe"
        self.assertFalse(filters.is_prompt_safe_llm("Tell me about controversial political topics"))

    @patch("app.filters.gemini.generate_content")
    def test_is_prompt_safe_llm_borderline(self, mock_generate):
        mock_generate.return_value.text = "SAFE"
        self.assertTrue(filters.is_prompt_safe_llm("How to make a homemade smoke bomb for special effects?"))
        mock_generate.return_value.text = "UNSAFE"
        self.assertFalse(filters.is_prompt_safe_llm("How to make a homemade smoke bomb for special effects?"))

if __name__ == "__main__":
    unittest.main()
