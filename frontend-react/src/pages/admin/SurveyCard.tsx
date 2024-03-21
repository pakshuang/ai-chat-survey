import {
  Box,
  Card,
  Flex,
  CardHeader,
  Heading,
  Stack,
  Text,
  StackDivider,
} from "@chakra-ui/react"

function SurveyCard() {
  return (
    <Card
      bg="white"
      h="full"
      w="full"
      borderWidth="1px"
      borderColor="white"
      _hover={{ borderColor: "black" }}
    >
      <CardHeader>
        <Heading size="md" noOfLines={2}>
          Client Report repoert serpoe rposerposerpi werkjawerkljase
          lkjasflkajsndkj
        </Heading>
      </CardHeader>
      <Flex h="full" mx="1rem" overflowY="scroll" mb="1rem">
        <Stack divider={<StackDivider />} spacing="4" h="full">
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Number of Questions
            </Heading>
            <Text pt="2" fontSize="sm">
              View a summary of all your clients over the last month.
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Description
            </Heading>
            <Text pt="2" fontSize="sm">
              Check out the overview of your clients.
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Analysis
            </Heading>
            <Text pt="2" fontSize="sm">
              See a detailed analysis of all your business clients. asdf asdf
              asdf asdf asdf sadf asdf sadf sadf asdf sadf asdf
            </Text>
          </Box>
        </Stack>
      </Flex>
    </Card>
  )
}

export default SurveyCard
