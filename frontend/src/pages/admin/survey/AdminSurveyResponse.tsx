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
        {response.messages.map((mes, index) => (
          <VStack key={`mes-${index}`} w="full" alignItems="start">
            {mes.role === "user" ? (
              <Text>{mes.content}</Text>
            ) : (
              <Text as="b">{mes.content}</Text>
            )}
          </VStack>
        ))}
      </VStack>
    </Card>
  )
}

export default AdminSurveyResponse
