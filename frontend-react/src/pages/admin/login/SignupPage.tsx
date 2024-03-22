import {
  Flex,
  Card,
  Button,
  Input,
  InputGroup,
  InputRightElement,
  VStack,
  Text,
  Heading,
  Link,
  IconButton,
} from "@chakra-ui/react";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";

import { useState } from "react";

function SignupPage() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <Flex
      flexDirection="column"
      minH="100vh"
      bg="gray.100"
      justifyContent="center"
      alignItems="center"
      gap="1rem"
    >
      <Card bg="white" padding="2rem">
        <VStack spacing="1rem">
          <Heading size="lg">Create an account</Heading>
          <VStack spacing="0.5rem" w="100%">
            <Input variant="flushed" placeholder="Username"></Input>
            <InputGroup size="md">
              <Input
                variant="flushed"
                pr="1.75rem"
                type={showPassword ? "text" : "password"}
                placeholder="Password"
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
          </VStack>
          <Button bg="gray.100" w="100%">
            Sign up
          </Button>
        </VStack>
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
