import { Card, Divider, Text, VStack } from "@chakra-ui/react"
import { Response } from "./constants"

function AdminSurveyResponse({ response }: { response: Response }) {
  return (
    <Card w="48rem" bg="white" p="1.5rem">
      <VStack>
        {response.answers.map((ans, index) => (
          <VStack key={index} w="full" alignItems="start">
            <Text as="b" fontSize="lg">
              {ans.question}
            </Text>
            <Text>{ans.answer}</Text>
            <Divider orientation="horizontal" />
          </VStack>
        ))}
      </VStack>
    </Card>
  )
}

export default AdminSurveyResponse
