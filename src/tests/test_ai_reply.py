import unittest
from unittest.mock import patch, MagicMock
from src.services.ai_reply import generate_ai_response

class TestAIResponse(unittest.TestCase):
    @patch("src.services.ai_reply.genai.GenerativeModel")
    def test_response(self, mock_model_cls):
        # Mock out the Gemini call so this test runs offline, without
        # burning API quota or needing a real GEMINI_API_KEY.
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value = MagicMock(text="Thanks for reaching out! 😊")
        mock_model_cls.return_value = mock_instance

        comment = "What is the price of the product?"
        response = generate_ai_response(comment)

        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        mock_instance.generate_content.assert_called_once()

if __name__ == "__main__":
    unittest.main()