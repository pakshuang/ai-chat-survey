import { useEffect, useState } from "react";
import { Flex ,Text} from "@chakra-ui/react";

import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";
import { getUserSurvey,sendMessageApi,submitBaseSurvey,init_message } from '../../hooks/useApi';
import { useParams } from "react-router-dom";
import NotFoundPage from "./NotFound";
interface Question {
  id: number;
  question_id:number;
  question: string;
  type: string;
  options?: string[];
  answer?:string,
}
interface Messages {
  sender: "user" | "bot";
  message: string;
  question?:Question
}

function ChatPage() {
  const {surveyID} = useParams();
  const [messages, setMessages] = useState<Messages[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [surveyState,setSurveyState] =useState({displayIndex:0,submitted:false,subtitle:"",title:""})
  const [token, setToken] = useState("test");
  const [responseID, setResponseId] = useState(0);
  function sendMessage(message: string) {
    if (surveyState.submitted){
      setIsLoading(true);
      setMessages([...messages, { sender: "user", message: message }]);
      sendMessageApi(responseID,surveyID,message)
        .then((res) => res.data)
        .then((data) => {
          setMessages((prevMessages) => [
            ...prevMessages,
            { sender: "bot", message: data["content"] },
          ]);
          setIsLoading(false);
        });
  
    } else {  
      handleQuestionResponse(surveyState.displayIndex+1,message);
    }
  }

  useEffect(() => {
    let tmp_token = "";
    // dummy signup and login to test api
    const signup = async () => {
      await fetch("http://localhost:5000/api/v1/admins", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: "admin", password: "admin" }),
      });
    };

    const login = async () => {
      const response = await fetch(
        "http://localhost:5000/api/v1/admins/login",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: "admin", password: "admin" }),
        }
      );
      const responseData = await response.json();
      console.log(responseData);
      setToken(responseData["jwt"]);
      tmp_token = responseData["jwt"];
    };
    getUserSurvey(surveyID).then((rep)=>{
        const answeredQuestions = rep.data.questions.map((question, index) => {
          return {
              sender:'bot',
              message:question.question,
              question:question
          };
        });
        setIsLoading(false)
        setSurveyState({...surveyState,subtitle:rep.data.subtitle,title:rep.data.title})
        setMessages([...answeredQuestions,{'sender':'bot','message':"You submitted the pre-survey"}])
      }
    )
  }, []);
  const handleQuestionResponse = (id: number, val: string | number) => {
    const updatedQuestions = [...messages];
    updatedQuestions[id-1].question.answer = val;
    const updId=Math.max(id,surveyState.displayIndex)
    setSurveyState({...surveyState, displayIndex:updId});
    setMessages(updatedQuestions)
  };
  const handleSubmit = async () => {
    const body ={
      "metadata": {
        "survey_id": surveyID
      },
      "answers": messages.slice(0,messages.length-1).map(ele=>{
        ele.question.question_id=ele.question.id;
        return ele.question
      })
    }
    await submitBaseSurvey(body)

    setSurveyState({...surveyState,submitted:true})
    let tmp_token = ""
    let tmp_sid = 3;
    let tmp_rid = 1;
    init_message(surveyID,tmp_rid,tmp_token).then(
      (rep)=>{
        const responseData = rep.data
        setMessages([...messages,{ sender: "bot", message: responseData["content"] }])
      }
    )
  };
  const displayMessages = surveyState.submitted ? messages:messages.slice(0,surveyState.displayIndex+1)

  if (surveyID===undefined){
    return <NotFoundPage></NotFoundPage>
  }
  return (
    <Flex flexDirection="column" bg="gray.100" h="100vh" p="1">
      <Flex justifyContent='center'>
        <Text fontSize="xl">
          {surveyState.title}
        </Text>
      </Flex>
       <ChatWindow handleSubmit={handleSubmit} messages={displayMessages} isBotThinking={isLoading} handleQuestionResponse={handleQuestionResponse} surveyState={surveyState}/>
      { surveyState.submitted  &&<ChatInput onSubmitMessage={sendMessage} isSubmitting={isLoading} />}
    </Flex>
  );
}
export default ChatPage;
