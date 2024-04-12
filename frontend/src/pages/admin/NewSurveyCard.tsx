import { Card, Center, VStack, Heading } from "@chakra-ui/react"
import { AddIcon } from "@chakra-ui/icons"
import { useNavigate } from "react-router-dom"

function NewSurveyCard() {
  const navigate = useNavigate()

  return (
    <Card
      bg="white"
      h="full"
      w="full"
      borderWidth="1px"
      borderColor="white"
      _hover={{ borderColor: "black", cursor: "pointer" }}
      onClick={() => navigate("/admin/survey/create")}
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
