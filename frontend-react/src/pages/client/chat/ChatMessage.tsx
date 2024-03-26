import { Flex, Box, Avatar, Text } from "@chakra-ui/react";
import React from "react";

interface ChatMessageProps {
  children: React.ReactNode;
  sender: "user" | "bot";
}

function ChatMessage({ children, sender }: ChatMessageProps) {
  return sender === "user" ? (
    <Flex justifyContent="flex-end" alignItems="center">
      <Box bg="green.300" rounded="lg" p="2" maxW="xs" mx="1" my="2">
        <Text fontWeight="bold">
          {sender.charAt(0).toUpperCase() + sender.slice(1)}
        </Text>
        <Text>{children}</Text>
      </Box>
      <Avatar name="User" size="md" ml="1" />
    </Flex>
  ) : (
    <Flex justifyContent="flex-start" alignItems="start">
      <Avatar
        name={sender.charAt(0).toUpperCase() + sender.slice(1)}
        size="md"
        mr="1"
        mt="2"
      />
      <Box bg="blue.300" rounded="lg" p="2" maxW="sm" mx="1" my="2">
        <Text fontWeight="bold">
          {sender.charAt(0).toUpperCase() + sender.slice(1)}
        </Text>
        <Text>{children}</Text>
      </Box>
    </Flex>
  );
}

export default ChatMessage;
