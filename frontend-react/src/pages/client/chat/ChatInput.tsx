import { Button, Input, Flex } from "@chakra-ui/react";
import { FormEvent, useState } from "react";

interface ChatInputProps {
  sendMessage: (message: string) => void;
}

function ChatInput({ sendMessage }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setIsSubmitting(true);
    // test button loading
    setTimeout(() => {
      setIsSubmitting(false);
      sendMessage(message);
      setMessage("");
    }, 500);
  }

  return (
    <form onSubmit={(e) => handleSubmit(e)}>
      <Flex flexDirection="row" p="4">
        <Input
          type="text"
          placeholder="Enter message ..."
          background="white"
          borderColor="gray.500"
          _hover={{ borderColor: "gray.500" }}
          _focus={{
            borderColor: "gray.500",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
          }}
          onChange={(e) => setMessage(e.target.value)}
          value={message}
          isDisabled={isSubmitting}
        />
        <Button
          type="submit"
          colorScheme="gray"
          variant="outline"
          borderColor="gray.500"
          _hover={{ bg: "gray.300" }}
          isLoading={isSubmitting}
        >
          Send
        </Button>
      </Flex>
    </form>
  );
}

export default ChatInput;
