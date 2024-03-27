import { Box, SkeletonCircle } from "@chakra-ui/react";
import { useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";

interface ChatWindowProps {
  messages: { sender: "user" | "bot"; message: string }[];
  isBotThinking: boolean;
}

function ChatWindow({ messages, isBotThinking }: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Box
      overflowY="auto"
      flex="1"
      p="3"
      css={{
        "::-webkit-scrollbar": {
          width: "5px",
        },

        "::-webkit-scrollbar-track": {
          background: "#f1f1f1",
        },

        "::-webkit-scrollbar-thumb": {
          background: "#888",
        },

        "::-webkit-scrollbar-thumb:hover": {
          background: "#555",
        },
      }}
    >
      {messages.map((item) => (
        <ChatMessage sender={item.sender}>{item.message}</ChatMessage>
      ))}
      {isBotThinking && (
        <ChatMessage sender="bot">
          <SkeletonCircle size="6" />
        </ChatMessage>
      )}
      <div ref={messagesEndRef} />
    </Box>
  );
}

export default ChatWindow;
