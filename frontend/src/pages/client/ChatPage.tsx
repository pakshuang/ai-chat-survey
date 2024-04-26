import { useEffect, useState } from "react";
import { Flex, Heading, Box, Link, Text, VStack } from "@chakra-ui/react";
import ChatWindow from "../../components/client/ChatWindow";
import ChatInput from "../../components/client/ChatInput";
import {
  getUserSurvey,
  sendMessageApi,
  submitBaseSurvey,
} from "../../hooks/useApi";
import { useParams } from "react-router-dom";
import { Messages, Question, surveyMessage } from "../../components/client/constants";
import ChatMessage from "../../components/client/ChatMessage";
import MultipleChoiceInput from "../../components/client/MultipleChoiceInput";
import MultipleResponseInput from "../../components/client/MultipleResponseInput";
import FreeResponseInput from "../../components/client/FreeResponseInput";

function ChatPage() {
  const { id } = useParams();
  const [messages, setMessages] = useState<Messages[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [surveyState, setSurveyState] = useState({
    displayIndex: 0,
    submitted: false,
    subtitle: "",
    title: "",
  });
  const [responseId, setResponseId] = useState(1);
  const [isLast, setIslast] = useState(false);

  async function sendMessage(message: string) {
    setIsLoading(true);
    setMessages([...messages, { sender: "user", message: message }]);
    try {
      const res = await sendMessageApi(responseId, Number(id), message);
      const data = res.data;
      if (data.is_last) {
        setIslast(true);
      }
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", message: data["content"] },
      ]);
    } catch (error) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", message: "Error generating response" },
      ]);
    }
    setIsLoading(false);
  }

  useEffect(() => {
    getUserSurvey(Number(id)).then((rep) => {
      const answeredQuestions = rep.data.questions.map((question: Question) => {
        return {
          sender: "bot",
          message: question.question,
          question: question,
        };
      });
      setIsLoading(false);
      setSurveyState({
        ...surveyState,
        subtitle: rep.data.subtitle,
        title: rep.data.title,
      });
      setMessages([
        ...answeredQuestions,
        { sender: "bot", message: surveyMessage },
      ]);
    });
  }, []);

  const handleQuestionResponse = (id: number, val: string | string[]) => {
    const updatedQuestions = [...messages];
    if (updatedQuestions[id - 1]?.question) {
      updatedQuestions[id - 1].question!.answer = val;
    }
    const updId = Math.max(id, surveyState.displayIndex);
    setSurveyState({ ...surveyState, displayIndex: updId });
    setMessages(updatedQuestions);
  };

  const handleSubmit = async () => {
    const body = {
      metadata: {
        survey_id: id,
      },
      answers: [...messages]
        .slice(0, messages.length - 1)
        .map((ele) => ele["question"]),
    };

    body["answers"].forEach((ele: any) => {
      if (!Array.isArray(ele.answer)) {
        ele.answer = [ele.answer];
      }
    });

    try {
      setSurveyState({ ...surveyState, submitted: true });
      setIsLoading(true);
      const rep = await submitBaseSurvey(id!, body);
      setResponseId(rep.data.response_id);
      const res = await sendMessageApi(rep.data.response_id, Number(id), "");
      const data = res.data;
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", message: data["content"] },
      ]);
    } catch (error) {
      console.log(error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", message: "Error generating response" },
      ]);
    }
    setIsLoading(false);
  };

  const displayMessages = surveyState.submitted
    ? messages
    : messages.slice(0, surveyState.displayIndex + 1);

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
        messages={displayMessages}
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
  );
}
export default ChatPage;
