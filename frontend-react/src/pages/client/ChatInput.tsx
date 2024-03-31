import { Button, Input, Flex } from "@chakra-ui/react";
import { FormEvent, useState, useRef, useEffect } from "react";

interface ChatInputProps {
  onSubmitMessage: (message: string) => void;
  isSubmitting: boolean;
}

function ChatInput({ onSubmitMessage, isSubmitting }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    onSubmitMessage(message)
    setMessage("");
  }

  useEffect(() => {
    inputRef.current?.focus();
  }, [message]);

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
          ref={inputRef}
        />
        <Button
          type="submit"
          colorScheme="gray"
          variant="outline"
          borderColor="gray.500"
          _hover={{ bg: "gray.300" }}
          isDisabled={message.length===0}
          isLoading={isSubmitting}
        >
          Send
        </Button>
      </Flex>
    </form>
  );
}

export default ChatInput;
