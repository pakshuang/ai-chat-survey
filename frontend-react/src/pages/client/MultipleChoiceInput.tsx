import { Radio, RadioGroup, Button, Flex } from "@chakra-ui/react";

function MultipleChoiceInput() {
  const options = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus mollis.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus mollis..",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus mollis...",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus mollis....",
  ];
  return (
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
      >
        Send
      </Button>
    </Flex>
  );
}

export default MultipleChoiceInput;
