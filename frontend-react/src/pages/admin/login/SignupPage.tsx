import {
  Button,
  Card,
  Flex,
  FormControl,
  FormErrorMessage,
  Heading,
  IconButton,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import { useForm, SubmitHandler } from "react-hook-form";
import { useState } from "react";
import { LoginSignupData } from "./constants";
import axios from "axios";
import { useNavigate } from "react-router-dom";

// TODO: abstract out into different files to avoid repeated logic across login/signup

function SignupPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [isTaken, setIsTaken] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();

  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting },
  } = useForm<LoginSignupData>();

  const onSubmit: SubmitHandler<LoginSignupData> = async (values) => {
    try {
      await axios.post("http://localhost:5000/api/v1/admins", values);
      navigate("/admin/survey");
    } catch (error: any) {
      if (
        error.response.status == 400 &&
        error.response.data.message == "Admin already exists"
      ) {
        setIsTaken(true);
      } else {
        toast({
          title: "An unknown error occurred.",
          description: "Please try again later.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    }
  };

  return (
    <Flex
      flexDirection="column"
      minH="100vh"
      bg="gray.100"
      justifyContent="center"
      alignItems="center"
      gap="1rem"
    >
      <Card bg="white" padding="2rem" w="21rem">
        <form onSubmit={handleSubmit(onSubmit)}>
          <VStack spacing="1rem">
            <Heading size="lg">Create an account</Heading>
            <VStack spacing="0.5rem" w="100%">
              {isTaken && (
                <Text color="red" fontSize="sm">
                  Your username has been taken. Please choose a different
                  username.
                </Text>
              )}
              <FormControl isInvalid={errors.username ? true : undefined}>
                <Input
                  variant="flushed"
                  placeholder="Username"
                  {...register("username", {
                    required: "This field is required.",
                    maxLength: {
                      value: 255,
                      message:
                        "Your username must be no longer than 255 characters.",
                    },
                    pattern: {
                      value: /^[A-Za-z0-9]*$/,
                      message:
                        "Your username must contain only letters (A-Z, a-z) and numbers (0-9).",
                    },
                  })}
                ></Input>
                <FormErrorMessage>
                  {errors.username && errors.username.message}
                </FormErrorMessage>
              </FormControl>
              <FormControl isInvalid={errors.password ? true : undefined}>
                <InputGroup size="md">
                  <Input
                    variant="flushed"
                    pr="1.75rem"
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    {...register("password", {
                      required: "This field is required.",
                      maxLength: {
                        value: 255,
                        message:
                          "Your password must be no longer than 255 characters.",
                      },
                    })}
                  />
                  <InputRightElement width="1.75rem">
                    <IconButton
                      variant="flushed"
                      h="1.75rem"
                      aria-label="View Password"
                      size="sm"
                      onClick={() => setShowPassword(!showPassword)}
                      icon={showPassword ? <ViewOffIcon /> : <ViewIcon />}
                    />
                  </InputRightElement>
                </InputGroup>
                <FormErrorMessage>
                  {errors.password && errors.password.message}
                </FormErrorMessage>
              </FormControl>
            </VStack>
            <Button
              bg="gray.100"
              w="100%"
              isLoading={isSubmitting}
              type="submit"
            >
              Sign up
            </Button>
          </VStack>
        </form>
      </Card>
      <Text>
        Already have an account?{" "}
        <Link fontWeight="700" href="/admin/login">
          Log in
        </Link>
      </Text>
    </Flex>
  );
}

export default SignupPage;
