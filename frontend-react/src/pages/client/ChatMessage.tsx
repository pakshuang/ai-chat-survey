import { Flex, Box, Avatar, Text } from "@chakra-ui/react"
import { ChatMessageProps } from "./constants"

function ChatMessage({ children, sender }: ChatMessageProps) {
  const isUser = sender === "user"
  return (
    <Box bg={isUser ? "gray.400" : "gray.200"} px="0.5rem" py="1rem">
      <Flex>
        {isUser ? (
          <Avatar name="User" size="md" ml="1" mt="2" />
        ) : (
          <Avatar
            name={sender.charAt(0).toUpperCase() + sender.slice(1)}
            size="md"
            mr="1"
            mt="2"
          />
        )}
        <Flex alignItems="center" ml="0.5rem">
          <Text fontSize="xl">{children}</Text>
        </Flex>
      </Flex>
    </Box>
  )
}

export default ChatMessage
