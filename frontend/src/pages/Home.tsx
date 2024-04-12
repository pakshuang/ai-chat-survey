import { Button, Flex, Heading, Highlight, Link, Text } from "@chakra-ui/react";

function Home() {
  return (
    <Flex
      flexDirection="column"
      minH="100vh"
      bg="gray.100"
      justifyContent="center"
      alignItems="center"
      textAlign="center"
      gap="1rem"
      p="4rem"
    >
      <Heading as="h1" size="2xl">
        AI Chat Survey 💬
      </Heading>
      <Text fontSize="2xl">
        <Highlight
          query="AI-driven conversations."
          styles={{ px: "2", py: "1", rounded: "full", bg: "white" }}
        >
          Transform your surveys with AI-driven conversations.
        </Highlight>
      </Text>
      <Link
        href="/admin/signup"
        _hover={{ textDecoration: "none" }}
        w="fit-content"
      >
        <Button colorScheme="blue">Try it out</Button>
      </Link>
    </Flex>
  );
}

export default Home;
