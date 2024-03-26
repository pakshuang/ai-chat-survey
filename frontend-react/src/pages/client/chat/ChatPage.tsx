import { useEffect, useState } from "react";
import { Flex } from "@chakra-ui/react";

import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";

interface Messages {
  sender: "user" | "bot";
  message: string;
}

function ChatPage() {
  const [messages, setMessages] = useState<Messages[]>([
    { sender: "user", message: "Hello" },
    { sender: "bot", message: "Hello, how are you?" },
    {
      sender: "bot",
      message:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et cursus purus. Ut gravida ac eros a fermentum. Praesent imperdiet sapien eget mauris vulputate, at mollis justo pharetra. Vestibulum ultricies pulvinar dolor nec iaculis. Vivamus tincidunt efficitur egestas. Donec sed diam vel augue imperdiet viverra. Sed turpis urna, tempus at tellus vel, finibus lacinia tellus. Nulla dictum orci vel volutpat imperdiet. Proin id dui vitae lacus rutrum molestie. Curabitur lobortis porta arcu vitae efficitur. Maecenas mollis odio eros, at vulputate quam lacinia et. Ut tincidunt dui ut mauris sodales, ac egestas sapien maximus. Vestibulum vitae posuere dolor, id mollis felis.",
    },
  ]);

  const [token, setToken] = useState("test");
  const [surveyID, setSurveyID] = useState(0);
  const [responseID, setResponseId] = useState(0);

  function sendMessage(message: string) {
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
      .then((data) =>
        setMessages(
          messages.concat(
            { sender: "user", message: message },
            { sender: "bot", message: data["content"] }
          )
        )
      );

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

    // dummy survey creation
    const create = async () => {
      const dummy_survey = {
        metadata: {
          id: tmp_sid,
          name: "Test Survey",
          description: "This is a test survey",
          created_by: "admin",
          created_at: "2024-03-22 15:24:10",
        },
        title: "Test Title",
        subtitle: "Test Subtitle",
        questions: [
          {
            id: 1,
            type: "multiple_choice",
            question: "Which performance did you enjoy the most?",
            options: ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
          },
          {
            id: 2,
            type: "short_answer",
            question: "What did you like about the performance?",
            options: [],
          },
          {
            id: 3,
            type: "long_answer",
            question: "Do you have any feedback about the venue?",
            options: [],
          },
        ],
        chat_context:
          "Full Stack Entertainment is an events company that organises performances such as concerts.",
      };

      const response = await fetch("http://localhost:5000/api/v1/surveys", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${tmp_token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dummy_survey),
      });
      const responseData = await response.json();
      setSurveyID(responseData["survey_id"]);
      tmp_sid = responseData["survey_id"];
    };

    // dummy survey response
    const answer = async () => {
      const dummy_answer = {
        metadata: {
          survey_id: tmp_sid,
        },
        answers: [
          {
            question_id: 1,
            type: "multiple_choice",
            question: "Which performance did you enjoy the most?",
            options: ["Clowns", "Acrobats", "Jugglers", "Magicians", "Choon"],
            answer: "Clowns",
          },
          {
            question_id: 2,
            type: "short_answer",
            question: "What did you like about the performance?",
            options: [],
            answer: "I enjoyed the acrobatic stunts.",
          },
          {
            question_id: 3,
            type: "long_answer",
            question: "Do you have any feedback about the venue?",
            options: [],
            answer: "The venue was spacious and well-maintained.",
          },
        ],
      };
      const response = await fetch("http://localhost:5000/api/v1/responses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dummy_answer),
      });
      const responseData = await response.json();
      setResponseId(responseData["response_id"]);
      tmp_rid = responseData["response_id"];
      console.log(responseData);
    };

    // test api for initial message
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
      setMessages([{ sender: "bot", message: responseData["content"] }]);
    };

    const run = async () => {
      console.log("signing up ...");
      await signup();
      console.log("done");
      console.log("logging in ...");
      await login();
      console.log("done");
      // console.log(tmp_token);
      console.log("Creating survey ...");
      await create();
      console.log("done");
      console.log("answering survey ...");
      await answer();
      console.log("done");
      console.log("initializing message ...");
      await init_message();
      console.log("done");
    };

    // console.log("use effect running");
    run();
    // console.log("use effect done");
  }, []);

  return (
    <Flex flexDirection="column" bg="gray.100" h="100vh" p="1">
      <ChatWindow messages={messages} />
      <ChatInput sendMessage={sendMessage} />
    </Flex>
  );
}
export default ChatPage;
