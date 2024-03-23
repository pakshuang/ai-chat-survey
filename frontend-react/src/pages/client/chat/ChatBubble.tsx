import React from 'react';
import { Box } from '@chakra-ui/react';

interface ChatBubbleProps {
  text: string;
  sender: 'user' | 'bot';
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ text, sender }) => {
  return (
    <Box
      mb="2"
      p="2"
      borderRadius="lg"
      alignSelf={sender === 'user' ? 'flex-end' : 'flex-start'}
      bg={sender === 'user' ? 'blue.500' : 'gray.200'}
      color={sender === 'user' ? 'white' : 'black'}
    >
      {text}
    </Box>
  );
};

export default ChatBubble;
