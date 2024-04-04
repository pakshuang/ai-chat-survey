import {
  CheckboxGroup,
  Checkbox,
  Textarea,
  Radio,
  RadioGroup,
  Stack,
  Text,
  Box,
} from "@chakra-ui/react";
import { useState } from "react";
import { QuestionProps } from "./constants";

const QuestionInput = ({
  questionData,
  handleQuestionResponse,
  submitted,
}: QuestionProps) => {
  const { question_id, type, options, answer } = questionData;
  const [tempAnswer, setTempAnswer] = useState(answer);
  const handleInputChange = (e) => {
    setTempAnswer(e.target.value);
  };

  const handleInputBlur = () => {
    handleQuestionResponse(question_id, tempAnswer);
  };

  const handleInputKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleQuestionResponse(question_id, tempAnswer);
    }
  };

  const renderQuestionType = () => {
    switch (type) {
      case "multiple_choice":
        return (
          <RadioGroup
            isDisabled={submitted}
            value={tempAnswer}
            onChange={(e) => {
              handleQuestionResponse(question_id, e);
            }}
          >
            <Stack direction="column">
              {options.map((option: string, index: number) => (
                <Radio
                  borderColor="black"
                  colorScheme="green"
                  isDisabled={submitted}
                  key={index}
                  value={option}
                >
                  {option}
                </Radio>
              ))}
            </Stack>
          </RadioGroup>
        );
      case "multiple_response":
        return (
          <>
           <Text >(You may pick more than one option.)</Text>
            <CheckboxGroup
              isDisabled={submitted}
              value={tempAnswer}
              onChange={(values) => {
                handleQuestionResponse(question_id, values);
              }}
            >
              <Stack direction="column">
                {options.map((option: string, index: number) => (
                  <Checkbox
                    borderColor="black"
                    colorScheme="green"
                    isDisabled={submitted}
                    key={index}
                    value={option}
                  >
                    {option}
                  </Checkbox>
                ))}
              </Stack>
            </CheckboxGroup>
          </>
        );
      case "free_response":
        return (
          <Textarea
            background="white"
            borderColor="gray.500"
            _hover={{ borderColor: "gray.500" }}
            _focus={{
              borderColor: "gray.500",
              boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
            }}
            onChange={handleInputChange}
            onBlur={handleInputBlur}
            onKeyPress={handleInputKeyPress}
            value={tempAnswer}
            isDisabled={submitted}
          />
        );
      default:
        return type;
    }
  };

  return renderQuestionType();
};

export default QuestionInput;
