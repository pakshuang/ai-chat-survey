import { Flex, Box, Avatar, Text } from "@chakra-ui/react";
import { ChatMessageProps } from "./constants";

function ChatMessage({ children, sender }: ChatMessageProps) {
  const isUser = sender === "user";
  return (
    <Box bg={isUser ? "gray.400" : "gray.200"} p="1.5rem">
      <Flex alignItems="start" gap="1rem">
        {isUser ? (
          <Avatar name="User" size="md" />
        ) : (
          <Avatar
            name={sender.charAt(0).toUpperCase() + sender.slice(1)}
            size="md"
          />
        )}
        <Text fontSize="xl">{children}</Text>
      </Flex>
    </Box>
  );
}

export default ChatMessage;
