

import React from 'react';
import { Box, Heading, Text, Button } from '@chakra-ui/react';
import { Link } from 'react-router-dom'; // If using React Router

const NotFoundPage = () => {
  return (
    <Box textAlign="center" mt={20}>
      <Heading as="h1" size="2xl" mb={4}>
        404 - Survey Not Found
      </Heading>
      <Text fontSize="xl" mb={8}>
        Oops! The survey you are looking for could not be found.
      </Text>
      <Button as={Link} to="/" colorScheme="blue">
        Go Home
      </Button>
    </Box>
  );
};

export default NotFoundPage;
