import { RouterProvider, createBrowserRouter } from "react-router-dom";

import Home from "./pages/Home";
import AdminHomePage from "./pages/admin/AdminHomePage";
import AdminSurveyPage from "./pages/admin/survey/AdminSurveyPage";
import SignupPage from "./pages/admin/login/SignupPage";
import LoginPage from "./pages/admin/login/LoginPage";
import SurveyPage from "./pages/client/survey/SurveyPage";
import ChatPage from "./pages/client/chat/ChatPage";
import { ChakraProvider } from "@chakra-ui/react";
import { theme } from "./components/theme";

const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/admin/signup", element: <SignupPage /> },
  { path: "/admin/login", element: <LoginPage /> },
  { path: "/admin/survey", element: <AdminHomePage /> },
  { path: "/admin/survey/create", element: <AdminSurveyPage /> },
  { path: "/survey", element: <SurveyPage /> },
  { path: "/chat", element: <ChatPage /> },
]);

function App() {
  return (
    <ChakraProvider theme={theme}>
      <RouterProvider router={router} />
    </ChakraProvider>
  );
}

export default App;
