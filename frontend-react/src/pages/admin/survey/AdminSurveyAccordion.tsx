import { DeleteIcon } from "@chakra-ui/icons"
import {
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Flex,
  Input,
  Select,
  Button,
  VStack,
} from "@chakra-ui/react"
import AdminSurveyOptions from "./AdminSurveyOptions"

function AdminSurveyAccordion() {
  return (
    <AccordionItem
      w="48rem"
      bg="white"
      borderTop={0}
      borderRadius={5}
      mt="1rem"
    >
      <AccordionButton h="5rem" borderBottom="1px" borderColor="gray.200">
        <Flex
          alignItems="center"
          justifyContent="space-between"
          w="full"
          p="0.5rem"
        >
          <Input
            placeholder="Question"
            variant="unstyled"
            size="lg"
            fontSize="2xl"
            fontWeight="bold"
            w="42rem"
            onClick={(e) => e.stopPropagation()}
            onKeyUp={(e) => e.preventDefault()}
          />
          <AccordionIcon />
        </Flex>
      </AccordionButton>
      <AccordionPanel p="1.5rem">
        <VStack spacing="2rem" alignItems="flex-start">
          <Select defaultValue={"option1"}>
            <option value="option1">Multiple Choice Question</option>
            <option value="option2">Multiple Response Question</option>
            <option value="option3">Short Answer</option>
          </Select>
          <AdminSurveyOptions />
          <Button leftIcon={<DeleteIcon />} colorScheme="red" variant="outline">
            Delete
          </Button>
        </VStack>
      </AccordionPanel>
    </AccordionItem>
  )
}

export default AdminSurveyAccordion
