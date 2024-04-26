import { RouterProvider, createBrowserRouter } from "react-router-dom"

import Home from "./pages/Home"
import AdminHomePage from "./pages/admin/survey/AdminHomePage"
import AdminSurveyPage from "./pages/admin/survey/AdminSurveyPage"
import SignupPage from "./pages/admin/login/SignupPage"
import LoginPage from "./pages/admin/login/LoginPage"
import ChatPage from "./pages/client/ChatPage"
import { ChakraProvider } from "@chakra-ui/react"
import { theme } from "./components/theme"
import { QueryClient, QueryClientProvider } from "react-query"
import ViewAdminSurvey from "./pages/admin/survey/ViewAdminSurvey"
import NotFoundPage from "./pages/NotFoundPage"
import AdminSurveyResponses from "./pages/admin/survey/AdminSurveyResponses"

const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/admin", element: <LoginPage /> },
  { path: "/admin/signup", element: <SignupPage /> },
  { path: "/admin/login", element: <LoginPage /> },
  { path: "/admin/survey", element: <AdminHomePage /> },
  { path: "/admin/survey/:id", element: <ViewAdminSurvey /> },
  { path: "/admin/survey/:id/responses", element: <AdminSurveyResponses /> },
  { path: "/admin/survey/create", element: <AdminSurveyPage /> },
  { path: "/chat/:id", element: <ChatPage /> },
  { path: "*", element: <NotFoundPage /> },
])

function App() {
  const queryClient = new QueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider theme={theme}>
        <RouterProvider router={router} />
      </ChakraProvider>
    </QueryClientProvider>
  )
}

export default App
