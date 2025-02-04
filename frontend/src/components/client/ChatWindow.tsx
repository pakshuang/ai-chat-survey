import { Box, SkeletonCircle, Button, Flex, Text } from "@chakra-ui/react"
import { Fragment, useEffect, useState } from "react"
import ChatMessage from "./ChatMessage"
import TypingEffect from "./TypingEffect"
import QuestionInput from "./QuestionInput"
import { ChatWindowProps, surveyMessage } from "./constants"

function ChatWindow({
  messages,
  isBotThinking,
  handleQuestionResponse,
  surveyState,
  handleSubmit,
}: ChatWindowProps) {
  const [botResponded, setBotResponded] = useState(false)

  useEffect(() => {
    if (messages.slice(-1)[0]?.sender === "bot") {
      setBotResponded(true)
    }
    if (messages.slice(-1)[0]?.sender === "user") {
      setBotResponded(false)
    }
  }, [messages])
  return (
    <Box
      overflowY="auto"
      minH="65px"
      flex="1"
      display="flex"
      flexDirection="column-reverse"
      borderRadius="lg"
      bg="gray.50"
      p="1rem"
      w="60rem"
      mx="auto"
      css={{
        "::-webkit-scrollbar": {
          width: "5px",
        },

        "::-webkit-scrollbar-track": {
          background: "#f1f1f1",
        },

        "::-webkit-scrollbar-thumb": {
          background: "#888",
        },

        "::-webkit-scrollbar-thumb:hover": {
          background: "#555",
        },
      }}
    >
      <Box flexDirection="column" display="flex" gap="0.5rem">
        <ChatMessage sender="bot">
          <Text fontSize="xl">{surveyState.subtitle}</Text>
        </ChatMessage>
        {messages.map((item, index) => {
          if (index === messages.length - 1 && botResponded) {
            if (item.message === surveyMessage) {
              if (surveyState.submitted) {
                return (
                  <ChatMessage key={index} sender={item.sender}>
                    <Text fontSize="xl">{item.message}</Text>
                  </ChatMessage>
                )
              }
              return (
                <ChatMessage key={index} sender={"bot"}>
                  <Flex flexDirection="column">
                    <TypingEffect text="Thank you for your responses. Please confirm your answers now, as they can't be changed later. Once confirmed, we'll continue with our discussion." />
                    <Box>
                      <Button
                        onClick={handleSubmit}
                        colorScheme="green"
                        mt="0.5rem"
                      >
                        Confirm
                      </Button>
                    </Box>
                  </Flex>
                </ChatMessage>
              )
            }
            return (
              <ChatMessage key={index} sender="bot">
                <Text fontSize="xl">
                  <TypingEffect text={messages.slice(-1)[0].message} />
                </Text>
              </ChatMessage>
            )
          } else {
            if (!item.question) {
              return (
                <ChatMessage key={index} sender={item.sender}>
                  <Text fontSize="xl">{item.message}</Text>
                </ChatMessage>
              )
            }
            return (
              <Fragment key={index}>
                <ChatMessage sender={item.sender}>
                  <Text fontSize="xl">{item.message}</Text>
                </ChatMessage>
                <ChatMessage sender="user">
                  <QuestionInput
                    questionData={item.question}
                    handleQuestionResponse={handleQuestionResponse}
                    submitted={surveyState.submitted}
                  />
                </ChatMessage>
              </Fragment>
            )
          }
        })}
        {isBotThinking && (
          <ChatMessage sender="bot">
            <SkeletonCircle size="4" alignSelf="center" ml="8px" />
            <SkeletonCircle size="4" alignSelf="center" mx="0px" />
            <SkeletonCircle size="4" alignSelf="center" />
          </ChatMessage>
        )}
      </Box>
    </Box>
  )
}

export default ChatWindow
