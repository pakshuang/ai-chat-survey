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

  const [token, setToken] = useState({
    jwt: "",
  });

  function sendMessage(message: string) {
    // TODO: replace with axios
    // fetch("http://localhost:5000/api/v1/responses/1/chat", {
    //   method: "POST",
    //   headers: {
    //     Authentication: `Bearer ${token}`,
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({ content: message }),
    // })
    //   .then((res) => res.json())
    //   .then((data) =>
    //     setMessages(
    //       messages.concat(
    //         { sender: "user", message: message },
    //         { sender: "bot", message: data["content"] }
    //       )
    //     )
    //   );

    // dummy messages
    setMessages(
      messages.concat(
        { sender: "user", message: message },
        { sender: "bot", message: "Hi, I'm a bot" }
      )
    );
  }

  useEffect(() => {
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
      setToken({ ...token, jwt: responseData["jwt"] });
      console.log(responseData);
      console.log(token);
    };

    signup();
    login();
  }, []);

  return (
    <Flex flexDirection="column" bg="gray.100" h="100vh" p="1">
      <ChatWindow messages={messages} />
      <ChatInput sendMessage={sendMessage} />
    </Flex>
  );
}
export default ChatPage;
