import { Button, Flex, CheckboxGroup, Checkbox, Box } from "@chakra-ui/react";
import { useState } from "react";
import { MultipleResponseInputProps } from "./constants";

function MultipleResponseInput({
  questionID,
  options,
  handleQuestionResponse,
}: MultipleResponseInputProps) {
  const [answers, setAnswers] = useState<(string | number)[]>([]);
  const isAnswered = answers.length > 0;

  function handleSubmit(e: React.MouseEvent<HTMLButtonElement>) {
    e.preventDefault();
    handleQuestionResponse(
      questionID,
      answers.map((item) => String(item))
    );
    setAnswers([]);
  }

  return (
    <form>
      <Flex flexDirection="row" p="0.5rem" w="60rem" mx="auto">
        <CheckboxGroup size="lg" onChange={(ans) => setAnswers(ans)}>
          <Box
            p="1rem"
            maxH="2000px"
            overflowY="auto"
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
          >
            {options.map((option: string, index: number) => (
              <Checkbox
                borderColor="black"
                colorScheme="blue"
                key={index}
                value={option}
              >
                {option}
              </Checkbox>
            ))}
          </Box>
        </CheckboxGroup>
        <Button
          size="lg"
          type="submit"
          colorScheme="blue"
          borderColor="gray.500"
          borderLeftRadius="0"
          height="auto"
          onClick={handleSubmit}
          isDisabled={!isAnswered}
        >
          Send
        </Button>
      </Flex>
    </form>
  );
}

export default MultipleResponseInput;
