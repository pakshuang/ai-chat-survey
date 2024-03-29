import { useEffect, useState } from "react";
import { Flex ,Button} from "@chakra-ui/react";

import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";
import { getUserSurvey,submitBaseSurvey } from '../../hooks/useApi';
import QuestionInput from "./QuestionInput";

interface Messages {
  sender: "user" | "bot";
  message: string;
  question:any,
}

function ChatPage() {
  const [messages, setMessages] = useState<Messages[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [surveyState,setSurveyState] =useState({displayIndex:0,submitted:false})
  const [token, setToken] = useState("test");
  const [surveyID, setSurveyID] = useState(1);
  const [responseID, setResponseId] = useState(0);
  function sendMessage(message: string) {
    setIsLoading(true);
    setMessages([...messages, { sender: "user", message: message }]);

    // test bot thinking
    // setTimeout(() => {
    //   setMessages((prevMessages) => [
    //     ...prevMessages,
    //     {
    //       sender: "bot",
    //       message:
    //         "Lorem ipsum dolor sit amet consectetur adipisicing elit. Doloremque asperiores ratione incidunt quasi accusamus facilis beatae a cupiditate aut minus. Autem ab sit voluptate commodi ducimus quis at officia mollitia.",
    //     },
    //   ]);
    //   setIsLoading(false);
    // }, 1000);

    // TODO: replace with axios
    // test api for subsequent messages
    fetch(
      `http://localhost:5000/api/v1/responses/${responseID}/chat?survey=${surveyID}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: message }),
      }
    )
      .then((res) => res.json())
      .then((data) => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", message: data["content"] },
        ]);
        setIsLoading(false);
      });

    // dummy messages
    // setMessages(
    //   messages.concat(
    //     { sender: "user", message: message },
    //     { sender: "bot", message: "Hi, I'm a bot" }
    //   )
    // );
  }

  useEffect(() => {
    let tmp_token = "";
    let tmp_sid = 3;
    let tmp_rid = 1;
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
      console.log(tmp_token);
    };
    getUserSurvey(surveyID).then((rep)=>{
        const answeredQuestions = rep.data.questions.map((question, index) => {
          return {
              sender:'bot',
              message:question.question,
              question:question
          };
        });
        setMessages([...answeredQuestions])
      }
    )
    const run = async () => {
      // console.log("signing up ...");
      // await signup();
      // console.log("done");
      // console.log("logging in ...");
      // await login();
      // await init_message();
      console.log("done");
      setIsLoading(false);
    };

    // console.log("use effect running");
    run();
    // console.log("use effect done");
  }, []);
  const handleQuestionResponse = (id: number, val: string | number) => {
    const updatedQuestions = [...messages];
    updatedQuestions[id-1].question.answer = val;
    const updId=Math.max(id,surveyState.displayIndex)
    setSurveyState({...surveyState, displayIndex:updId});
    setMessages(updatedQuestions)
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const body ={
      "metadata": {
        "survey_id": surveyID
      },
      "answers": messages.map(ele=>{
        ele.question.question_id=ele.question.id;
        return ele.question
      })
    }
    await submitBaseSurvey(body)
    setSurveyState({...surveyState,submitted:true})
    let tmp_token = ""
    let tmp_sid = 3;
    let tmp_rid = 1;
    const init_message = async () => {
      const response = await fetch(
        `http://localhost:5000/api/v1/responses/${tmp_rid}/chat?survey=${tmp_sid}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${tmp_token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: "" }),
        }
      );
      const responseData = await response.json();
      console.log(responseData);
      setMessages([...messages,{ sender: "bot", message: responseData["content"] }]);
    };
    await init_message()
  };
  console.log(messages.length)
  const displayMessages = surveyState.submitted ? messages:messages.slice(0,surveyState.displayIndex+1)
  return (
    <Flex flexDirection="column" bg="gray.100" h="100vh" p="1">
       <ChatWindow messages={displayMessages} isBotThinking={isLoading} handleQuestionResponse={handleQuestionResponse} submitted={surveyState.submitted}/>
      {messages.length===surveyState.displayIndex &&  !surveyState.submitted && <Button onClick={handleSubmit}>
            Submit
          </Button>}
      { surveyState.submitted &&<ChatInput onSubmitMessage={sendMessage} isSubmitting={isLoading} />}
    </Flex>
  );
}
export default ChatPage;
