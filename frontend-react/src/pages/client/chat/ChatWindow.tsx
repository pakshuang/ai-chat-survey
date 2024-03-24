import { Flex, Box } from "@chakra-ui/react";

interface ChatWindowProps {
  messages: { sender: "user" | "bot"; message: string }[];
}

function ChatWindow({ messages }: ChatWindowProps) {
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
      {messages.map((item, index) =>
        item.sender === "user" ? (
          <Flex key={index} justifyContent="flex-end" alignItems="center">
            <Box bg="green.300" rounded="lg" p="2" maxW="xs">
              {item.message}
            </Box>
          </Flex>
        ) : (
          <Flex key={index} justifyContent="flex-start" alignItems="center">
            <Box bg="blue.300" rounded="lg" p="2" maxW="xs">
              {item.message}
            </Box>
          </Flex>
        )
      )}
    </Box>
  );
}

export default ChatWindow;
