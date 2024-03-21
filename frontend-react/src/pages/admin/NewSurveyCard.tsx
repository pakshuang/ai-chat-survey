import { Card, Center, VStack, Heading } from "@chakra-ui/react"
import { AddIcon } from "@chakra-ui/icons"

function NewSurveyCard() {
  return (
    <Card
      bg="white"
      h="full"
      w="full"
      borderWidth="1px"
      borderColor="white"
      _hover={{ borderColor: "black" }}
    >
      <Center h="full" w="full">
        <VStack spacing="2rem">
          <AddIcon boxSize={20} />
          <Heading size="lg">Create New Survey</Heading>
        </VStack>
      </Center>
    </Card>
  )
}

export default NewSurveyCard
