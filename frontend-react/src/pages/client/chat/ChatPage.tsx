import React, { useState } from 'react';
import { Box, Input, Button } from '@chakra-ui/react';
import ChatBubble from './ChatBubble';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState<string>('');

  const handleSendMessage = () => {
    if (inputText.trim() !== '') {
      setMessages([...messages, { text: inputText, sender: 'user' }]);
      setInputText('');
    }
  };
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };
  return (
    <Box display="flex" flexDirection="column" height="100vh">
      <Box flex="1" overflowY="auto" p="4">
        {messages.map((message, index) => (
          <ChatBubble key={index} text={message.text} sender={message.sender} />
        ))}
      </Box>
        <Box display="flex" alignItems="center" backgroundColor="#f0f0f0" borderRadius="md" p="6">
          <Input
            backgroundColor='white'
            flex="1"
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type a message..."
            onKeyDown={handleKeyDown} 
          />
          <Button ml="2" colorScheme="blue" onClick={handleSendMessage}>
            Send
          </Button>
        </Box>
    </Box>
  );
};

export default ChatPage;
