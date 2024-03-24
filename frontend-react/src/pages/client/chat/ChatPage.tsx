import { useState } from "react";
import { Flex } from "@chakra-ui/react";

import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";

interface Messages {
  sender: "user" | "bot";
  message: string;
}

function ChatPage() {
  const [messages, setMessages] = useState<Messages[]>([
    { sender: "user", message: "Hello" },
    { sender: "bot", message: "Hello, how are you?" },
  ]);

  function sendMessage(message: string) {
    setMessages(
      messages.concat(
        { sender: "user", message: message },
        { sender: "bot", message: "Hi, I'm a bot" }
      )
    );
  }
  return (
    <Flex flexDirection="column" bg="gray.100" h="100vh" p="1">
      <ChatWindow messages={messages} />
      <ChatInput sendMessage={sendMessage} />
    </Flex>
  );
}
export default ChatPage;
