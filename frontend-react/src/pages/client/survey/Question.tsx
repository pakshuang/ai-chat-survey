import { Box, FormControl, FormLabel, Flex, Button, Textarea, Radio, RadioGroup, Stack, Input } from '@chakra-ui/react';
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
}

const Question = ({ questionData, handleQuestionResponse }: QuestionProps) => {
  const { id, question, type, options,answer } = questionData;
  const renderQuestionType = () => {
    switch (type) {
      case 'rating':
        return (
          <FormControl isRequired>
          <FormLabel>{question}</FormLabel>
          <Flex>
            {[1, 2, 3, 4, 5].map((rating) => (
              <Box key={rating} as="span" mr="1">
                <Button
                  variant={rating === answer ? "solid" : "outline"}
                  colorScheme={rating == answer ? "teal" : "gray"}
                  onClick={() => handleQuestionResponse(id, rating)}
                >
                  {rating}
                </Button>
              </Box>
            ))}
          </Flex>
        </FormControl>
        );
      case 'Multiple Choice':
        return (
          <FormControl isRequired>
            <FormLabel>{question}</FormLabel>
            <RadioGroup value={answer} onChange={(e) => {
              handleQuestionResponse(id, e)
            }}>
              <Stack direction="column">
                {options.map((option: string, index: number) => (
                  <Radio key={index} value={option}>
                    {option}
                  </Radio>
                ))}
              </Stack>
            </RadioGroup>
          </FormControl>
        );
      case 'short_answer':
        return (
          <FormControl isRequired>
            <FormLabel>{question}</FormLabel>
            <Input type="text" value={answer}  onChange={(e) => handleQuestionResponse(id, e.target.value)} />
          </FormControl>
        );
      case 'Open-ended':
        return (
          <FormControl isRequired>
            <FormLabel>{question}</FormLabel>
            <Textarea  value={answer} onChange={(e) => handleQuestionResponse(id, e.target.value)} />
          </FormControl>
        );
      default:
        return null;
    }
  };

  return (
      renderQuestionType()
  );
};

export default Question;
