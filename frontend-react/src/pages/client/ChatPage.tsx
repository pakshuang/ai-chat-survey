import { useEffect, useState } from "react";
import { Button,Flex, Heading, Text } from "@chakra-ui/react";
import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";
import {
  getUserSurvey,
  sendMessageApi,
  submitBaseSurvey,
} from "../hooks/useApi";
import { useParams } from "react-router-dom";
import { SurveyState,Question, surveyMessage } from "./constants";
import ChatMessage from "./ChatMessage";
import Cookies from 'js-cookie';

function ChatPage() {
  const { id } = useParams();
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [surveyState, setSurveyStateInternal] = useState<SurveyState>(() => {
    // Load surveyState from cookie on component mount
    const savedSurveyState = Cookies.get(`surveyState_${id}`);
    return savedSurveyState ? JSON.parse(savedSurveyState) : {
      displayIndex: 0,
      submitted: false,
      subtitle: "",
      title: "",
      messages:[]
    };
  });
  const setSurveyState = (newSurveyState:SurveyState) => {
    setSurveyStateInternal(newSurveyState);
    Cookies.set(`surveyState_${id}`, JSON.stringify(newSurveyState), { expires: 7 });
  };
  const [responseId, setResponseId] = useState(1);
  const [isLast,setIslast]=useState(false)
  async function sendMessage(message: string) {
      setIsLoading(true);
      setSurveyState({...surveyState,messages:[...surveyState.messages, { sender: "user", message: message }]})
      try{
        const res = await sendMessageApi(responseId, id, message)
        const data = res.data
        if (data.is_last){
          setIslast(true)
        }
        setSurveyState({...surveyState,messages:[...surveyState.messages, { sender: "bot", message: data["content"] },]})
      } catch(error){
        setSurveyState({...surveyState,messages:[...surveyState.messages, { sender: "bot", message: "Error generating response" }]})
      }
      setIsLoading(false);
  }

  useEffect(() => {
    if (surveyState.title==="" ||surveyState.messages.length===0){
      getUserSurvey(id).then((rep) => {
        const answeredQuestions = rep.data.questions.map((question, index) => {
          return {
            sender: "bot",
            message: question.question,
            question: question,
          };
        });
        setSurveyState({
          displayIndex: 0,
          submitted: false,
          subtitle: rep.data.subtitle,
          title: rep.data.title,
          messages:[
            ...answeredQuestions,
            { sender: "bot", message: surveyMessage },
          ]
        });
      });
    }
    setIsLoading(false)
    
  }, []);

  const handleQuestionResponse = (id: number, val: string | number) => {
    const updatedQuestions = [...surveyState.messages];
    updatedQuestions[id - 1].question.answer = val;
    let updId=surveyState.displayIndex;
    if (val){
      updId = Math.max(id, surveyState.displayIndex);
    }
    setSurveyState({ ...surveyState, displayIndex: updId });;
  };

  const handleSubmit = async () => {
    const body = {
      metadata: {
        survey_id: id,
      },
      answers:  JSON.parse(JSON.stringify(surveyState.messages))
        .slice(0, surveyState.messages.length - 1)
        .map((ele) => ele["question"])
    };
    // https://stackoverflow.com/questions/9885821/copying-of-an-array-of-objects-to-another-array-without-object-reference-in-java
    // need to deep copy
    body["answers"].forEach((ele: any) => {
      if (!Array.isArray(ele.answer)) {
        ele.answer = [ele.answer];
      }
    });
    try {
      setSurveyState({ ...surveyState, submitted: true })
      setIsLoading(true)
      const rep = await submitBaseSurvey(body);
      setResponseId(rep.data.response_id);
      const res = await sendMessageApi(rep.data.response_id, id, "")
      const data = res.data;
      setSurveyState({...surveyState,messages:[...surveyState.messages, { sender: "bot", message: data["content"] }]})
    } catch (error) {
      setSurveyState({...surveyState,messages:[...surveyState.messages, { sender: "bot", message: "Error generating response" }]})
    }
    setSurveyState({ ...surveyState, submitted: true })
    setIsLoading(false)
  };
  const clearCookies = () => {
    Cookies.remove(`surveyState_${id}`);
  };
  const displayedMessages = surveyState.submitted ? surveyState.messages : surveyState.messages.slice(0,surveyState.displayIndex+1)
  return (
    <Flex
      flexDirection="column"
      bg="gray.100"
      h="100vh"
      w="100%"
      minW="65rem"
    >
      <Flex justifyContent="center">
        <Heading fontSize="xl" p="1rem">{surveyState.title}</Heading>
        {false &&<Button onClick={clearCookies}> s</Button>}
      </Flex>
      <ChatWindow
        handleSubmit={handleSubmit}
        messages={displayedMessages}
        isBotThinking={isLoading}
        handleQuestionResponse={handleQuestionResponse}
        surveyState={surveyState}
      />
      {surveyState.submitted && !isLast && (
        <ChatInput onSubmitMessage={sendMessage} isSubmitting={isLoading} />
      )}
      {isLast && (
        <ChatMessage sender="bot">
          The survey is over. Thank you for your responses. You can close the
          page.
        </ChatMessage>
      )}
    </Flex>
  );
}
export default ChatPage;
