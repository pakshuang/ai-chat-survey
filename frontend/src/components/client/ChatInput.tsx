import { Button, Textarea, Flex } from "@chakra-ui/react";
import React, { useState, useRef, useEffect } from "react";

interface ChatInputProps {
  onSubmitMessage: (message: string) => void;
  isSubmitting: boolean;
}

function ChatInput({ onSubmitMessage, isSubmitting }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const isEmpty = message.trim() === "";

  function handleSubmit(
    e:
      | React.MouseEvent<HTMLButtonElement>
      | React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (isEmpty) {
      return;
    }
    onSubmitMessage(message);
    e.preventDefault();
    e.stopPropagation();
    setMessage("");
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !isSubmitting) {
      handleSubmit(e);
    }
  };

  useEffect(() => {
    inputRef.current?.focus();
  }, [message]);

  return (
    <form>
      <Flex flexDirection="row" p="0.5rem" w="60rem" mx="auto">
        <Textarea
          size="lg"
          placeholder="Enter message..."
          background="white"
          borderColor="gray.500"
          borderRightRadius="0"
          _focus={{
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
          }}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          value={message}
          ref={inputRef}
          rows={1}
          resize="none"
          autoFocus
        />
        <Button
          size="lg"
          type="submit"
          onClick={handleSubmit}
          colorScheme="blue"
          borderColor="gray.500"
          borderLeftRadius="0"
          isLoading={isSubmitting}
          isDisabled={isEmpty}
        >
          Send
        </Button>
      </Flex>
    </form>
  );
}

export default ChatInput;
