import { Flex, Card, Image } from "@chakra-ui/react";
import { ChatMessageProps } from "./constants";
import bot from "../../assets/bot.svg";
import user from "../../assets/user.svg";

function ChatMessage({ children, sender }: ChatMessageProps) {
  const isUser = sender === "user";
  return (
    <Card bg={isUser ? "gray.400" : "gray.200"} p="1.5rem">
      <Flex alignItems="start" gap="1rem">
        {isUser ? (
          <Image
            boxSize="45px"
            src={user}
            ignoreFallback={true}
            borderRadius={0}
            loading="eager"
            // Icon by <a href="https://freeicons.io/profile/722">Fasil</a> on <a href="https://freeicons.io">freeicons.io</a>
          />
        ) : (
          <Image
            boxSize="45px"
            src={bot}
            ignoreFallback={true}
            borderRadius={0}
            loading="eager"
            // Icon by <a href="https://freeicons.io/profile/433683">Pexelpy</a> on <a href="https://freeicons.io">freeicons.io</a>
          />
        )}
        {children}
      </Flex>
    </Card>
  );
}

export default ChatMessage;
