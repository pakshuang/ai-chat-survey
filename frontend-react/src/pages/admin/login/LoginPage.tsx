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
import { useNavigate } from "react-router-dom";
import { login } from "../../hooks/useApi";

// TODO: abstract out into different files to avoid repeated logic across login/signup

function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [isUnauthorised, setIsUnauthorised] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();

  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting },
  } = useForm<LoginSignupData>();

  const onSubmit: SubmitHandler<LoginSignupData> = async (values) => {
    try {
      await login(values);
      navigate("/admin/survey");
    } catch (error: any) {
      console.error("Login failed:", error.response?.data);
      if (error.response.status === 401) {
        setIsUnauthorised(true);
      } else {
        toast({
          title: "Error",
          description: "An error occurred. Please try again later.",
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
            <Heading size="lg">Welcome back</Heading>
            <VStack spacing="0.5rem" w="100%">
              {isUnauthorised && (
                <Text color="red" fontSize="sm">
                  Your username or password is incorrect. Please try again.
                </Text>
              )}
              <FormControl isInvalid={errors.username ? true : undefined}>
                <Input
                  variant="flushed"
                  placeholder="Username"
                  {...register("username", {
                    required: "This field is required.",
                    // not sure if login fields typically have these checks
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
              Log in
            </Button>
          </VStack>
        </form>
      </Card>
      <Text>
        Don't have an account yet?{" "}
        <Link fontWeight="700" href="/admin/signup">
          Sign up
        </Link>
      </Text>
    </Flex>
  );
}

export default LoginPage;
