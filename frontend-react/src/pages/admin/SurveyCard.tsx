import {
  Box,
  Card,
  Flex,
  CardHeader,
  Heading,
  Stack,
  Text,
  StackDivider,
} from "@chakra-ui/react"
import { GetSurvey } from "./survey/constants"
import dayjs from "dayjs"
import { useNavigate } from "react-router-dom"

function SurveyCard({ survey }: { survey: GetSurvey }) {
  const navigate = useNavigate()

  return (
    <Card
      bg="white"
      h="full"
      w="full"
      borderWidth="1px"
      borderColor="white"
      _hover={{ borderColor: "black", cursor: "pointer" }}
      onClick={() => navigate(`/admin/survey/${survey.metadata.survey_id}`)}
    >
      <CardHeader>
        <Heading size="md" noOfLines={2}>
          {survey.title}
        </Heading>
      </CardHeader>
      <Flex h="full" ml="1rem" mr="0.5rem" overflowY="scroll" mb="1rem">
        <Stack divider={<StackDivider />} spacing="4" h="full" w="full">
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Description
            </Heading>
            <Text pt="2" fontSize="sm">
              {survey.subtitle}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Chatbot Context
            </Heading>
            <Text pt="2" fontSize="sm">
              {survey.chat_context}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Number of Questions
            </Heading>
            <Text pt="2" fontSize="sm">
              {survey.questions.length}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Created at
            </Heading>
            <Text pt="2" fontSize="sm">
              {dayjs(survey.metadata.created_at).format(
                "ddd, D MMM YYYY HH:mm:ss"
              )}
            </Text>
          </Box>
        </Stack>
      </Flex>
    </Card>
  )
}

export default SurveyCard
