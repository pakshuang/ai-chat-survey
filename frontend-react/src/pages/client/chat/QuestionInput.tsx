import { CheckboxGroup ,Checkbox, Textarea, Radio, RadioGroup, Stack, Input } from '@chakra-ui/react';
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
      case 'multiple_choice':
        return (
            <RadioGroup 
            isDisabled={submitted}
            value={answer} onChange={(e) => {
              handleQuestionResponse(id, e)
            }}>
              <Stack direction="column"  >
                {options.map((option: string, index: number) => (
                  <Radio  borderColor="black"  colorScheme='green'  isDisabled={submitted} key={index} value={option}>
                    {option}
                  </Radio>
                ))}
              </Stack>
            </RadioGroup>
        );
      case 'multiple_response':
        return (
          <CheckboxGroup 
          isDisabled={submitted}
          value={answer} 
          onChange={(values) => {
            handleQuestionResponse(id, values)
          }}
        >
          <Stack direction="column">
            {options.map((option: string, index: number) => (
              <Checkbox  
                borderColor="black"  
                colorScheme='green'  
                isDisabled={submitted} 
                key={index} 
                value={option}
              >
                {option}
              </Checkbox>
            ))}
          </Stack>
        </CheckboxGroup>
        );
      case 'short_answer':
          return (
            <Input
            background="white"
            borderColor="gray.500"
            _hover={{ borderColor: "gray.500" }}
            _focus={{
              borderColor: "gray.500",
              boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
            }}
            onChange={(e) => handleQuestionResponse(id, e.target.value)}
            value={answer}
            isDisabled={submitted}
            />
          );
      case 'long_answer':
        return (
          <Textarea
          background="white"
          borderColor="gray.500"
          _hover={{ borderColor: "gray.500" }}
          _focus={{
            borderColor: "gray.500",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
          }}
          onChange={(e) => handleQuestionResponse(id, e.target.value)}
          value={answer}
          isDisabled={submitted}
          />
        );
      default:
        return type;
    }
  };

  return (
      renderQuestionType()
  );
};

export default QuestionInput;
