import { Flex, Box, Avatar, Text, Divider } from "@chakra-ui/react";
import { ChatMessageProps } from "./constants";

function ChatMessage({ children, sender }: ChatMessageProps) {
  const isUser=sender === "user"
  return <Box bg={isUser ? "gray.400" : "gray.200"} >
    <Flex>
      {isUser ? <Avatar name="User" size="md" ml="1" mt="2" />
      :      <Avatar
      name={sender.charAt(0).toUpperCase() + sender.slice(1)}
      size="md"
      mr="1"
      mt="2"
    />}
    <Flex alignItems='center'>
        <Text fontSize="xl" >
          {children}
        </Text>
    </Flex>
    </Flex>
    <Divider borderColor="black" mt='4' ></Divider>
    </Box>
}

export default ChatMessage;
