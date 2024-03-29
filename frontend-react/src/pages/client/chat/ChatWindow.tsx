import { Box, SkeletonCircle ,Button, Text, Flex} from "@chakra-ui/react";
import { useRef, useEffect, useState } from "react";
import ChatMessage from "./ChatMessage";
import TypingEffect from "./TypingEffect";
import QuestionInput from "./QuestionInput";
interface ChatWindowProps {
  messages: { sender: "user" | "bot"; message: string }[];
  isBotThinking: boolean;
  surveyState: any;
  handleQuestionResponse: (id: number, val: string  | number) => void;
  handleSubmit: ()=>void
}

function ChatWindow({ messages, isBotThinking ,handleQuestionResponse,surveyState,handleSubmit}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [botResponded, setBotResponded] = useState(false);
  const [showConfirm,setShowConfirm]= useState(false)
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    if (messages[surveyState.displayIndex]){
      setShowConfirm(true)
    }
  };


  useEffect(() => {
    if (messages.slice(-1)[0]?.sender === "bot" ) {
      setBotResponded(true);
    }
    if (messages.slice(-1)[0]?.sender === "user") {
      setBotResponded(false);
    }
    scrollToBottom();
  }, [messages]);
  return (
    <Box
      overflowY="auto"
      flex="1"
      p="3"
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
      <ChatMessage sender="bot">
        {surveyState.subtitle}
      </ChatMessage>
      {messages.map((item, index) => {

        if (index === messages.length - 1 && botResponded) {
          if (item.message==='You submitted the pre-survey'){
            return <ChatMessage sender={'bot'}>
              <Flex flexDirection='column'>
                <TypingEffect 
                text="Thank you for your responses. Please confirm your answers now, as they can't be changed later. Once confirmed, we'll continue with our discussion"
                scrollToBottom={scrollToBottom} >
                </TypingEffect>
              <Box>
              <Button onClick={handleSubmit} colorScheme="green">
                Confirm
              </Button>
              </Box>
              </Flex>
          </ChatMessage>
          }
          return (
            <ChatMessage sender="bot">
              <TypingEffect
                text={messages.slice(-1)[0].message}
                scrollToBottom={scrollToBottom}
              />
              {
              item.question  && item.question.type !=='Open-ended' && 
              <QuestionInput questionData={item.question} handleQuestionResponse={handleQuestionResponse} submitted={surveyState.submitted}></QuestionInput>
                }
            </ChatMessage>
          )
        } else {
          return <ChatMessage sender={item.sender}>{item.message}
              {item.question &&<QuestionInput questionData={item.question} handleQuestionResponse={handleQuestionResponse} submitted={surveyState.submitted}></QuestionInput>}
            </ChatMessage>

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
