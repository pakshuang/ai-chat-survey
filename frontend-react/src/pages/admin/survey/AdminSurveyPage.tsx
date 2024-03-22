import {
  Accordion,
  Button,
  Card,
  Flex,
  HStack,
  Input,
  VStack,
} from "@chakra-ui/react"
import AdminSurveyAccordion from "./AdminSurveyAccordion"
import { AddIcon, ExternalLinkIcon } from "@chakra-ui/icons"

function AdminSurveyPage() {
  return (
    <Flex minH="100vh" w="100%" bg="gray.100" minW="80rem">
      <VStack mx="auto" my="5rem" spacing="0" w="48rem">
        <Card w="48rem" bg="white" p="1.5rem">
          <Input
            placeholder="Untitled"
            variant="flushed"
            size="lg"
            fontSize="4xl"
            fontWeight="bold"
            autoFocus
          />
          <Input
            placeholder="Description"
            variant="flushed"
            size="md"
            fontSize="xl"
            mt="1rem"
          />
        </Card>
        <Accordion allowMultiple allowToggle defaultIndex={[0, 1]}>
          <AdminSurveyAccordion />
          <AdminSurveyAccordion />
        </Accordion>
        <HStack mt="1rem" w="full">
          <Button leftIcon={<AddIcon />} colorScheme="green" h="3rem" w="50%">
            Add Question
          </Button>
          <Button
            leftIcon={<ExternalLinkIcon />}
            colorScheme="messenger"
            h="3rem"
            w="50%"
          >
            Create Survey
          </Button>
        </HStack>
      </VStack>
    </Flex>
  )
}

export default AdminSurveyPage
