from openai import OpenAI
from unittest import TestCase
from unittest.mock import patch, MagicMock
from ..src.llm_classes import LLM,GPT,ChatLog
class TestChatLogAndGPT(TestCase):

    def test_chatlog_initialization(self):
        initial_responses = "User responses go here."
        chat_log = ChatLog(initial_responses)
        self.assertEqual(len(chat_log.message_list), 1)
        self.assertIn("system", chat_log.message_list[0]["role"])
        self.assertIn(initial_responses, chat_log.message_list[0]["content"])

    def test_chatlog_insert_and_update(self):
        chat_log = ChatLog("Initial responses.")
        updated_list = chat_log.insert_and_update("User response", 1, is_llm=False)
        self.assertEqual(len(updated_list), 2)  # System prompt + user message
        self.assertEqual(updated_list[1]["role"], "user")
        chat_log.insert_and_update("Assistant response", 2, is_llm=True)
        self.assertEqual(len(chat_log.message_list), 3)
        self.assertEqual(chat_log.message_list[2]["role"], "assistant")

    @patch("backend.src.llm_classes.llm_level.OpenAI")
    def test_gpt_run(self, mock_openai):
        # Mock the OpenAI client's behavior
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Mocked response"))]
        mock_client.chat.completions.create.return_value = mock_response

        gpt = GPT()
        response = gpt.run([{"role": "system", "content": "Some prompt"}])
        self.assertEqual(response, "Mocked response")
        mock_client.chat.completions.create.assert_called_once()
    
    def test_chatlog_multiple_messages(self):
        chat_log = ChatLog("Initial responses.")
        chat_log.insert_and_update("First user response", 1, is_llm=False)
        chat_log.insert_and_update("Assistant response", 2, is_llm=True)
        chat_log.insert_and_update("Second user response", 3, is_llm=False)
        self.assertEqual(len(chat_log.message_list), 4)  # Includes initial system message
        self.assertEqual(chat_log.message_list[3]["role"], "user")
        self.assertIn("Second user response", chat_log.message_list[3]["content"])
        
    @patch("backend.src.llm_classes.llm_level.OpenAI")
    def test_gpt_exception_handling(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API limit reached or network error")
        
        gpt = GPT()
        with self.assertRaises(Exception) as context:
            gpt.run([{"role": "system", "content": "Some prompt"}])
        self.assertTrue("API limit reached or network error" in str(context.exception))
        