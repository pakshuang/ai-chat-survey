import pytest
import sys,os
from pathlib import Path
from openai import OpenAI
from unittest import TestCase
from unittest.mock import patch, MagicMock
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))
from src.llm_classes import LLM,GPT,ChatLog
class TestChatLogAndGPT:

    def test_chatlog_initialization(self):
        initial_responses = "User responses go here."
        chat_log = ChatLog(initial_responses)
        assert len(chat_log.message_list) == 1
        assert "system" in chat_log.message_list[0]["role"]
        assert initial_responses in chat_log.message_list[0]["content"]

    def test_chatlog_insert_and_update(self):
        chat_log = ChatLog("Initial responses.")
        updated_list = chat_log.insert_and_update("User response", 1, is_llm=False)
        assert len(updated_list) == 2# System prompt + user message
        assert updated_list[1]["role"] == "user"
        chat_log.insert_and_update("Assistant response", 2, is_llm=True)
        assert len(chat_log.message_list) == 3
        assert chat_log.message_list[2]["role"] == "assistant"

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
        assert response == "Mocked response"
        mock_client.chat.completions.create.assert_called_once()
    
    def test_chatlog_multiple_messages(self):
        chat_log = ChatLog("Initial responses.")
        chat_log.insert_and_update("First user response", 1, is_llm=False)
        chat_log.insert_and_update("Assistant response", 2, is_llm=True)
        chat_log.insert_and_update("Second user response", 3, is_llm=False)
        assert len(chat_log.message_list) == 4# Includes initial system message
        assert chat_log.message_list[3]["role"] == "user"
        assert "Second user response" in chat_log.message_list[3]["content"]
        
    @patch("backend.src.llm_classes.llm_level.OpenAI")
    def test_gpt_exception_handling(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API limit reached or network error")
        
        gpt = GPT()
        with pytest.raises(Exception) as context:
            gpt.run([{"role": "system", "content": "Some prompt"}])
        assert "API limit reached or network error" in str(context.exception)
