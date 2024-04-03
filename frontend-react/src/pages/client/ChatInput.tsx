import { Button, Textarea, Flex } from "@chakra-ui/react";
import { useState, useRef, useEffect } from "react";

interface ChatInputProps {
  onSubmitMessage: (message: string) => void;
  isSubmitting: boolean;
}

function ChatInput({ onSubmitMessage, isSubmitting }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  function handleSubmit() {
    onSubmitMessage(message);
    setMessage("");
  }

  const handleInputKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  useEffect(() => {
    inputRef.current?.focus();
  }, [message]);

  return (
    <form onSubmit={handleSubmit}>
      <Flex flexDirection="row" p="0.5rem" w="60rem" mx="auto">
        <Textarea
          size="lg"
          type="text"
          placeholder="Enter message..."
          background="white"
          borderColor="gray.500"
          borderRightRadius="0"
          _focus={{
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
          }}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleInputKeyPress}
          value={message}
          ref={inputRef}
          rows={1}
          resize="none"
          autoFocus
        />
        <Button
          size="lg"
          type="submit"
          colorScheme="blue"
          borderColor="gray.500"
          borderLeftRadius="0"
          isLoading={isSubmitting}
        >
          Send
        </Button>
      </Flex>
    </form>
  );
}

export default ChatInput;
