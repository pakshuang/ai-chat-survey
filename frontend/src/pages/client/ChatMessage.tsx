import { Flex, Card, Avatar, Text } from "@chakra-ui/react";
import { ChatMessageProps } from "./constants";

function ChatMessage({ children, sender }: ChatMessageProps) {
  const isUser = sender === "user";
  return (
    <Card bg={isUser ? "gray.400" : "gray.200"} p="1.5rem">
      <Flex alignItems="start" gap="1rem">
        {isUser ? (
          <Avatar
            name="User"
            size="md"
            src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Emoji_u263a.svg"
          />
        ) : (
          <Avatar
            name={sender.charAt(0).toUpperCase() + sender.slice(1)}
            size="md"
            src="https://emojiisland.com/cdn/shop/products/Emoji_Icon_-_Sunglasses_cool_emoji_large.png?v=1571606093"
          />
        )}
        <Text fontSize="xl" flexGrow="1">
          {children}
        </Text>
      </Flex>
    </Card>
  );
}

export default ChatMessage;
