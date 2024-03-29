from openai import OpenAI
from unittest import TestCase
from unittest.mock import patch, MagicMock
from ..src.llm_classes import LLM, GPT, ChatLog, construct_chatlog


class TestMockAPI(TestCase):
    @patch("llm_classes.llm_level.OpenAI")
    def test_gpt_exception_handling(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception(
            "API limit reached or network error"
        )

        gpt = GPT(model="gpt-3.5-turbo")
        with self.assertRaises(Exception) as context:
            gpt.run([{"role": "system", "content": "Some prompt"}])
        self.assertTrue("API limit reached or network error" in str(context.exception))

    @patch("llm_classes.llm_level.OpenAI")
    def test_gpt_run(self, mock_openai):
        # Mock the OpenAI client's behavior
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Mocked response"))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        gpt = GPT()
        response = gpt.run([{"role": "system", "content": "Some prompt"}])
        self.assertEqual(response, "Mocked response")
        mock_client.chat.completions.create.assert_called_once()
