import { Card, Input, Text, Textarea } from "@chakra-ui/react"
import { GetSurvey } from "../../../pages/admin/survey/constants"

function ViewAdminSurveyTitle({ survey }: { survey: GetSurvey }) {
  return (
    <Card w="48rem" bg="white" p="1.5rem">
      <Input
        value={survey.title}
        variant="flushed"
        size="md"
        fontSize="2xl"
        fontWeight="bold"
        borderColor="gray.200"
        isReadOnly
      />
      <Text as="b" mt="0.5rem">
        Subtitle
      </Text>
      <Textarea
        value={survey.subtitle}
        size="md"
        fontSize="lg"
        rows={2}
        resize="vertical"
        borderColor="gray.200"
        isReadOnly
      />
      <Text as="b" mt="0.5rem">
        Chat Context
      </Text>
      <Textarea
        value={survey.chat_context}
        size="md"
        fontSize="md"
        rows={3}
        resize="vertical"
        borderColor="gray.200"
        isReadOnly
      />
    </Card>
  )
}

export default ViewAdminSurveyTitle
