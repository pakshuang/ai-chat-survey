import { SubmitHandler } from "react-hook-form";
import { useState } from "react";
import { LoginSignupData, errorToast } from "../../../components/admin/login/constants";
import { useNavigate } from "react-router-dom";
import { signup } from "../../../hooks/useApi";
import { LoginSignupForm } from "../../../components/admin/login/LoginSignupForm";

function SignupPage() {
  const [isTaken, setIsTaken] = useState(false);
  const navigate = useNavigate();

  const onSubmit: SubmitHandler<LoginSignupData> = async (values) => {
    try {
      await signup(values);
      sessionStorage.setItem("redirected", "1");
      navigate("/admin/login");
    } catch (error: any) {
      if (
        error.response.status === 400 &&
        error.response.data.message == "Admin already exists"
      ) {
        setIsTaken(true);
      } else {
        errorToast();
      }
    }
  };

  return (
    <LoginSignupForm
      onSubmit={onSubmit}
      heading="Create an account"
      hasSubmitError={isTaken}
      submitErrorMessage="Your username has been taken. Please choose another username."
      submitButtonText="Sign up"
      redirectText="Already have an account?"
      redirectLink="/admin/login"
      redirectTo="Log in"
    />
  );
}

export default SignupPage;
