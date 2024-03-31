import { useEffect, useState } from "react";
import { Flex, Text } from "@chakra-ui/react";
import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";
import {
  getUserSurvey,
  sendMessageApi,
  submitBaseSurvey,
} from "../hooks/useApi";
import { useParams } from "react-router-dom";
import { Messages } from "./constants";

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

  async function sendMessage(message: string) {
      setIsLoading(true);
      setMessages([...messages, { sender: "user", message: message }]);
      try{
        const res = await sendMessageApi(responseId, id, message)
        const data = res.data
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", message: data["content"] },
        ]);
      } catch( error){
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", message: "Error generating response" },
        ]);
      }
      setIsLoading(false);
  }

  useEffect(() => {
    getUserSurvey(id).then((rep) => {
      const answeredQuestions = rep.data.questions.map((question, index) => {
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
        { sender: "bot", message: "You submitted the pre-survey" },
      ]);
    });
  }, []);

  const handleQuestionResponse = (id: number, val: string | number) => {
    const updatedQuestions = [...messages];
    updatedQuestions[id - 1].question.answer = val;
    const updId = Math.max(id, surveyState.displayIndex);
    setSurveyState({ ...surveyState, displayIndex: updId });
    setMessages(updatedQuestions);
  };

  const handleSubmit = async () => {
    const body = {
      metadata: {
        survey_id: id,
      },
      answers: messages
        .slice(0, messages.length - 1)
        .map((ele) => ele["question"]),
    };

    body["answers"].forEach((ele: any) => {
      if (!Array.isArray(ele.answer)) {
        ele.answer = [ele.answer];
      }
    });

    try {
      const rep = await submitBaseSurvey(body);
      setSurveyState({ ...surveyState, submitted: true });
      setResponseId(rep.data.response_id);
      const res = sendMessageApi(rep.data.response_id, id, "")
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
    setIsLoading(false)
  };

  const displayMessages = surveyState.submitted
    ? messages
    : messages.slice(0, surveyState.displayIndex + 1);

  return (
    <Flex flexDirection="column" bg="gray.100" h="100vh" p="1">
      <Flex justifyContent="center">
        <Text fontSize="xl">{surveyState.title}</Text>
      </Flex>
      <ChatWindow
        handleSubmit={handleSubmit}
        messages={displayMessages}
        isBotThinking={isLoading}
        handleQuestionResponse={handleQuestionResponse}
        surveyState={surveyState}
      />
      {surveyState.submitted && (
        <ChatInput onSubmitMessage={sendMessage} isSubmitting={isLoading} />
      )}
    </Flex>
  );
}
export default ChatPage;
