import { useEffect, useState } from "react"
import { Flex, Heading, Box, Link, Text, VStack } from "@chakra-ui/react"
import ChatWindow from "./ChatWindow"
import ChatInput from "./ChatInput"
import {
  getUserSurvey,
  sendMessageApi,
  submitBaseSurvey,
} from "../hooks/useApi"
import { useParams } from "react-router-dom"
import { SurveyState, Question, surveyMessage, Messages } from "./constants"
import ChatMessage from "./ChatMessage"
import Cookies from "js-cookie"
import MultipleChoiceInput from "./MultipleChoiceInput"
import MultipleResponseInput from "./MultipleResponseInput"
import FreeResponseInput from "./FreeResponseInput"

function ChatPage() {
  const { id } = useParams()
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [messages, setMessagesInteral] = useState<Messages[]>(() => {
    const savedMessages = Cookies.get(`messages_${id}`)
    return savedMessages ? JSON.parse(savedMessages) : []
  })
  const [surveyState, setSurveyStateInternal] = useState<SurveyState>(() => {
    const savedSurveyState = Cookies.get(`surveyState_${id}`)
    return savedSurveyState
      ? JSON.parse(savedSurveyState)
      : {
          displayIndex: 0,
          submitted: false,
          subtitle: "",
          title: "",
        }
  })
  const setMessages = (messages: Messages[]) => {
    setMessagesInteral(messages)
    Cookies.set(`messages_${id}`, JSON.stringify(messages), { expires: 7, httpOnly: true })
  }
  const setSurveyState = (newSurveyState: SurveyState) => {
    setSurveyStateInternal(newSurveyState)
    Cookies.set(`surveyState_${id}`, JSON.stringify(newSurveyState), { expires: 7, httpOnly: true })
  }
  const [responseId, setResponseId] = useState(1)
  const [isLast, setIslast] = useState(false)
  async function sendMessage(message: string) {
    setIsLoading(true)
    const newMessages = [...messages, { sender: "user", message: message }]
    setMessages(newMessages)
    try {
      const res = await sendMessageApi(responseId, Number(id), message)
      const data = res.data
      if (data.is_last) {
        setIslast(true)
        Cookies.remove(`messages_${id}`);
        Cookies.remove(`surveyState_${id}`);
      }
      setMessages([...newMessages, { sender: "bot", message: data["content"] }])
    } catch (error) {
      setMessages([
        ...newMessages,
        { sender: "bot", message: "Error generating response" },
      ])
    }
    setIsLoading(false)
  }

  useEffect(() => {
    if (surveyState.title === "" || messages.length === 0) {
      getUserSurvey(Number(id)).then((rep) => {
        const answeredQuestions = rep.data.questions.map(
          (question: Question) => {
            return {
              sender: "bot",
              message: question.question,
              question: question,
            }
          }
        )
        setSurveyState({
          displayIndex: 0,
          submitted: false,
          subtitle: rep.data.subtitle,
          title: rep.data.title,
        })
        setMessages([
          ...answeredQuestions,
          { sender: "bot", message: surveyMessage },
        ])
      })
    }
    setIsLoading(false)
  }, [])

  const handleQuestionResponse = (id: number, val: string | string[]) => {
    const updatedQuestions = [...messages]
    if (updatedQuestions[id - 1]?.question) {
      updatedQuestions[id - 1].question!.answer = val
    }
    let updId = surveyState.displayIndex
    if (val) {
      updId = Math.max(id, surveyState.displayIndex)
    }
    setMessages(updatedQuestions)
    setSurveyState({ ...surveyState, displayIndex: updId })
  }

  const handleSubmit = async () => {
    const body = {
      metadata: {
        survey_id: id,
      },
      answers: JSON.parse(JSON.stringify(messages))
        .slice(0, messages.length - 1)
        .map((ele) => ele["question"]),
    }
    // https://stackoverflow.com/questions/9885821/copying-of-an-array-of-objects-to-another-array-without-object-reference-in-java
    // need to deep copy
    body["answers"].forEach((ele: any) => {
      if (!Array.isArray(ele.answer)) {
        ele.answer = [ele.answer]
      }
    })

    try {
      setSurveyState({ ...surveyState, submitted: true })
      setIsLoading(true)
      const rep = await submitBaseSurvey(id!, body)
      setResponseId(rep.data.response_id)
      const res = await sendMessageApi(rep.data.response_id, Number(id), "")
      const data = res.data
      setMessages([...messages, { sender: "bot", message: data["content"] }])
    } catch (error) {
      setMessages([
        ...messages,
        { sender: "bot", message: "Error generating response" },
      ])
    }
    setIsLoading(false)
  }

  const displayedMessages = surveyState.submitted
    ? messages
    : messages.slice(0, surveyState.displayIndex + 1)
  return (
    <Flex
      flexDirection="column"
      bg="gray.100"
      h="100vh"
      w="100%"
      minW="65rem"
      gap="1rem"
      py="1rem"
    >
      <Heading fontSize="xl" p="0.5rem" textAlign="center">
        {surveyState.title}
      </Heading>
      <ChatWindow
        handleSubmit={handleSubmit}
        messages={displayedMessages}
        isBotThinking={isLoading}
        handleQuestionResponse={handleQuestionResponse}
        surveyState={surveyState}
      />
      {!surveyState.submitted &&
        messages.length > 0 &&
        messages[surveyState.displayIndex].question?.type ===
          "multiple_choice" && (
          <MultipleChoiceInput
            questionID={
              messages[surveyState.displayIndex].question!.question_id
            }
            options={messages[surveyState.displayIndex].question!.options!}
            handleQuestionResponse={handleQuestionResponse}
          />
        )}
      {!surveyState.submitted &&
        messages.length > 0 &&
        messages[surveyState.displayIndex].question?.type ===
          "multiple_response" && (
          <MultipleResponseInput
            questionID={
              messages[surveyState.displayIndex].question!.question_id
            }
            options={messages[surveyState.displayIndex].question!.options!}
            handleQuestionResponse={handleQuestionResponse}
          />
        )}
      {!surveyState.submitted &&
        messages.length > 0 &&
        messages[surveyState.displayIndex].question?.type ===
          "free_response" && (
          <FreeResponseInput
            questionID={
              messages[surveyState.displayIndex].question!.question_id
            }
            handleQuestionResponse={handleQuestionResponse}
          />
        )}
      {surveyState.submitted && !isLast && (
        <ChatInput onSubmitMessage={sendMessage} isSubmitting={isLoading} />
      )}
      {isLast && (
        <Box w="60rem" mx="auto" pr="5px">
          <ChatMessage sender="bot">
            The survey is over. Thank you for your responses. You can close the
            page.
          </ChatMessage>
        </Box>
      )}
      <VStack
        pos="absolute"
        bottom="0.5rem"
        left="0.5rem"
        alignItems="start"
        spacing={0}
      >
        <Text fontSize="0.5rem" color="gray.400">
          Bot icon by{" "}
          <Link href="https://freeicons.io/profile/722" isExternal>
            Fasil
          </Link>{" "}
          on{" "}
          <Link href="https://freeicons.io" isExternal>
            freeicons.io
          </Link>
        </Text>

        <Text fontSize="0.5rem" color="gray.400">
          User icon by{" "}
          <Link href="https://freeicons.io/profile/433683" isExternal>
            Pexelpy
          </Link>{" "}
          on{" "}
          <Link href="https://freeicons.io" isExternal>
            freeicons.io
          </Link>
        </Text>
      </VStack>
    </Flex>
  )
}
export default ChatPage
