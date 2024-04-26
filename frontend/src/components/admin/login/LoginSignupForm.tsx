import React, { useState } from "react";
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
} from "@chakra-ui/react";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import { useForm, SubmitHandler } from "react-hook-form";
import { LoginSignupData } from "../../../pages/admin/login/constants";

interface LoginSignupProps {
  onSubmit: SubmitHandler<LoginSignupData>;
  heading: string;
  hasSubmitError: boolean;
  submitErrorMessage: string;
  submitButtonText: string;
  redirectText: string;
  redirectLink: string;
  redirectTo: string;
}

export const LoginSignupForm: React.FC<LoginSignupProps> = ({
  onSubmit,
  heading,
  hasSubmitError,
  submitErrorMessage,
  submitButtonText,
  redirectText,
  redirectLink,
  redirectTo,
}) => {
  const [showPassword, setShowPassword] = useState(false);

  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting },
  } = useForm<LoginSignupData>();

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
            <Heading size="lg">{heading}</Heading>
            <VStack spacing="0.5rem" w="100%">
              {hasSubmitError && (
                <Text color="red" fontSize="sm">
                  {submitErrorMessage}
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
              {submitButtonText}
            </Button>
          </VStack>
        </form>
      </Card>
      <Text>
        {redirectText}{" "}
        <Link fontWeight="700" href={redirectLink}>
          {redirectTo}
        </Link>
      </Text>
    </Flex>
  );
};

export default LoginSignupForm;
