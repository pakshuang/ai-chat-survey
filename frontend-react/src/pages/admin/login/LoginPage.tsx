import { SubmitHandler } from "react-hook-form";
import { useState } from "react";
import { LoginSignupData, errorToast } from "./constants";
import { useNavigate, useSearchParams } from "react-router-dom";
import { login } from "../../hooks/useApi";
import { LoginSignupForm } from "./LoginSignupForm";
import { useToast } from "@chakra-ui/react";

function LoginPage() {
  const [searchParams] = useSearchParams();
  const [redirectToasted, setRedirectToasted] = useState(false);
  const [isUnauthorised, setIsUnauthorised] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();

  if (searchParams.get("redirect") && !redirectToasted) {
    toast({
      title: "Your account has been created.",
      description: "Go ahead and log in.",
      status: "success",
      duration: 9000,
      isClosable: true,
    });
    setRedirectToasted(true);
  }

  const onSubmit: SubmitHandler<LoginSignupData> = async (values) => {
    try {
      await login(values);
      navigate("/admin/survey");
    } catch (error: any) {
      if (error.response.status === 401) {
        setIsUnauthorised(true);
      } else {
        errorToast();
      }
    }
  };

  return (
    <LoginSignupForm
      onSubmit={onSubmit}
      heading="Welcome back"
      hasSubmitError={isUnauthorised}
      submitErrorMessage="Your username or password is incorrect. Please try again."
      submitButtonText="Log in"
      redirectText="Don't have an account yet?"
      redirectLink="/admin/signup"
      redirectTo="Sign up"
    />
  );
}

export default LoginPage;
