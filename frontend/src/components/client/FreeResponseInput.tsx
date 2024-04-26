import { Button, Textarea, Flex } from "@chakra-ui/react";
import { FreeResponseInputProps } from "../../pages/client/constants";
import { useState } from "react";

function FreeResponseInput({
  questionID,
  handleQuestionResponse,
}: FreeResponseInputProps) {
  const [answer, setAnswer] = useState<string>("");
  const isAnswered = answer !== "";

  function handleSubmit(
    e:
      | React.FormEvent<HTMLFormElement>
      | React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (!isAnswered) {
      return;
    }
    e.preventDefault();
    handleQuestionResponse(questionID, answer);
    setAnswer("");
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      handleSubmit(e);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
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
          onChange={(e) => setAnswer(e.target.value)}
          onKeyDown={handleKeyDown}
          value={answer}
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
          isDisabled={!isAnswered}
        >
          Send
        </Button>
      </Flex>
    </form>
  );
}

export default FreeResponseInput;
