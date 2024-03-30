import { Box, Heading, Text } from "@chakra-ui/react";

const NotFoundPage = () => {
  return (
    <Box textAlign="center" mt={20}>
      <Heading as="h1" size="2xl" mb={4}>
        404 - Page Not Found
      </Heading>
      <Text fontSize="xl" mb={8}>
        Oops! The page you are looking for could not be found.
      </Text>
    </Box>
  );
};

export default NotFoundPage;
