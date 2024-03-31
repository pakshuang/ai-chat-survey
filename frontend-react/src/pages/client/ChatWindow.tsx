import { Box, SkeletonCircle, Button, Flex } from "@chakra-ui/react";
import { useRef, useEffect, useState } from "react";
import ChatMessage from "./ChatMessage";
import TypingEffect from "./TypingEffect";
import QuestionInput from "./QuestionInput";
import { ChatWindowProps, surveyMessage } from "./constants";

function ChatWindow({
  messages,
  isBotThinking,
  handleQuestionResponse,
  surveyState,
  handleSubmit,
}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [botResponded, setBotResponded] = useState(false);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (messages.slice(-1)[0]?.sender === "bot") {
      setBotResponded(true);
    }
    if (messages.slice(-1)[0]?.sender === "user") {
      setBotResponded(false);
    }
  }, [messages]);
  const disabled=messages.filter((ele) => ele.question!==undefined).some((ele) => ele.question.answer==undefined || ele.question.answer.length === 0 || ele.question.answer==="");
  return (
    <Box
      overflowY="auto"
      flex="1"
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
      <ChatMessage sender="bot">{surveyState.subtitle}</ChatMessage>
      {messages.map((item, index) => {
        if (index === messages.length - 1 && botResponded) {
          if (item.message === surveyMessage) {
            if (surveyState.submitted) {
              return (
                <ChatMessage sender={item.sender}>{item.message}</ChatMessage>
              );
            }
            return (
              <ChatMessage sender={"bot"}>
                <Flex flexDirection="column">
                  <TypingEffect
                    text="Thank you for your responses. Please confirm your answers now, as they can't be changed later. Once confirmed, we'll continue with our discussion."
                    scrollToBottom={scrollToBottom}
                  ></TypingEffect>
                  <Box>
                    <Button onClick={handleSubmit} colorScheme="green" mt="0.5rem" isDisabled={disabled}>
                      Confirm
                    </Button>
                    {disabled &&  `Please complete question(s) ` +messages
                        .filter((ele) => ele.question !== undefined) // Filter out messages without questions
                        .map((ele, index) => {
                          if (ele.question.answer === undefined || ele.question.answer.length === 0 || ele.question.answer === "") {
                            return `${index + 1}`;
                          }
                          return null; // Filter out messages where the question is answered
                        })
                        .filter(Boolean) // Filter out null values
                        .join(", ") +` before submitting.`}

                  </Box>
                </Flex>
              </ChatMessage>
            );
          }
          return (
            <ChatMessage sender="bot">
              <TypingEffect
                text={messages.slice(-1)[0].message}
                scrollToBottom={scrollToBottom}
              />
              {item.question !==undefined &&<QuestionInput
                questionData={item.question}
                handleQuestionResponse={handleQuestionResponse}
                submitted={surveyState.submitted}
              ></QuestionInput>}
            </ChatMessage>
          );
        } else {
          return (
            <ChatMessage sender={item.sender}>
              {item.message}
              {item.question !==undefined &&<QuestionInput
                questionData={item.question}
                handleQuestionResponse={handleQuestionResponse}
                submitted={surveyState.submitted}
              ></QuestionInput> }
            </ChatMessage>
          );
        }
      })}
      {isBotThinking && (
        <ChatMessage sender="bot">
          <SkeletonCircle size="6" />
        </ChatMessage>
      )}
      <div ref={messagesEndRef} />
    </Box>
  );
}

export default ChatWindow;
