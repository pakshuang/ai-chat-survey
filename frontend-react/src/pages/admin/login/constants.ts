import { useToast } from "@chakra-ui/react";

export type LoginSignupData = {
  username: string
  password: string
}

export type LoginResponse = {
  jwt: string
  jwt_exp: string
}

export const errorToast = () => {
  const toast = useToast();
  toast({
    title: "Error",
    description: "An error occurred. Please try again later.",
    status: "error",
    duration: 3000,
    isClosable: true,
  });
};
