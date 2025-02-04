import { SubmitHandler } from "react-hook-form";
import { useState, useEffect } from "react";
import { LoginSignupData, errorToast } from "../../../components/admin/login/constants";
import { useNavigate } from "react-router-dom";
import { login } from "../../../hooks/useApi";
import { LoginSignupForm } from "../../../components/admin/login/LoginSignupForm";
import { useToast } from "@chakra-ui/react";

function LoginPage() {
  const [isUnauthorised, setIsUnauthorised] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();

  useEffect(() => {
    if (sessionStorage.getItem("redirected") == "1") {
      toast({
        title: "Your account has been created.",
        description: "Go ahead and log in.",
        status: "success",
        duration: 9000,
        isClosable: true,
      });
      sessionStorage.removeItem("redirected");
    }
  });

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
