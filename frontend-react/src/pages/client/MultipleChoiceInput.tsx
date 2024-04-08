import { Radio, RadioGroup, Button, Flex } from "@chakra-ui/react";
import { useState } from "react";
import { MultipleChoiceInputProps } from "./constants";

function MultipleChoiceInput({
  questionID,
  options,
  handleQuestionResponse,
}: MultipleChoiceInputProps) {
  const [answer, setAnswer] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isAnswered = answer !== "";

  function handleSubmit(e: React.MouseEvent<HTMLButtonElement>) {
    e.preventDefault();
    setIsSubmitting(true);
    handleQuestionResponse(questionID, answer);
  }

  return (
    <form>
      <Flex flexDirection="row" p="0.5rem" w="60rem" mx="auto">
        <RadioGroup
          size="lg"
          p="1rem"
          display="flex"
          backgroundColor="white"
          alignItems="left"
          flex="1"
          flexDirection="column"
          gap="1.5"
          justifyContent="space-evenly"
          borderRadius="md"
          borderRightRadius="0"
          border="1px"
          borderColor="gray.500"
          onChange={(e) => setAnswer(e)}
        >
          {options.map((option: string, index: number) => (
            <Radio
              borderColor="black"
              colorScheme="blue"
              key={index}
              value={option}
            >
              {option}
            </Radio>
          ))}
        </RadioGroup>
        <Button
          size="lg"
          type="submit"
          colorScheme="blue"
          borderColor="gray.500"
          borderLeftRadius="0"
          height="auto"
          onClick={handleSubmit}
          isDisabled={!isAnswered}
          isLoading={isSubmitting}
        >
          Send
        </Button>
      </Flex>
    </form>
  );
}

export default MultipleChoiceInput;
