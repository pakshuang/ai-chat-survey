import { Box, Flex, Button, Textarea, Radio, RadioGroup, Stack, Input } from '@chakra-ui/react';
interface Question {
  id:number,
  question:string,
  type:string,
  options:[],
  answer:string | number,
}
interface QuestionProps {
  questionData: Question;
  handleQuestionResponse: (id: number, val: string  | number) => void;
  submitted:boolean,
}

const QuestionInput = ({ questionData, handleQuestionResponse ,submitted}: QuestionProps) => {
  const { id, type, options,answer } = questionData;
  const renderQuestionType = () => {
    switch (type) {
      case 'rating':
        return (
          <Flex>
            {[1, 2, 3, 4, 5].map((rating) => (
              <Box key={rating} as="span" mr="1">
                <Button
                  isDisabled={submitted}
                  variant={rating === answer ? "solid" : "outline"}
                  colorScheme={rating == answer ? "teal" : "gray"}
                  onClick={() => handleQuestionResponse(id, rating)}
                >
                  {rating}
                </Button>
              </Box>
            ))}
          </Flex>
        );
      case 'Multiple Choice':
        return (
            <RadioGroup 
            isDisabled={submitted}
            value={answer} onChange={(e) => {
              handleQuestionResponse(id, e)
            }}>
              <Stack direction="column">
                {options.map((option: string, index: number) => (
                  <Radio  isDisabled={submitted} key={index} value={option}>
                    {option}
                  </Radio>
                ))}
              </Stack>
            </RadioGroup>
        );
      case 'short_answer':
        return (
            <Input type="text" value={answer}  onChange={(e) => handleQuestionResponse(id, e.target.value)} />
        );
      case 'Open-ended':
        return (
            <Textarea  isDisabled={submitted}value={answer} onChange={(e) => handleQuestionResponse(id, e.target.value)} />
        );
      default:
        return null;
    }
  };

  return (
      renderQuestionType()
  );
};

export default QuestionInput;
