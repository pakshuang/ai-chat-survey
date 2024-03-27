import {
  Center,
  Flex,
  Grid,
  GridItem,
  Heading,
  Spinner,
  VStack,
} from "@chakra-ui/react"
import SurveyCard from "./SurveyCard"
import NewSurveyCard from "./NewSurveyCard"
import { useQuery } from "react-query"
import { getSurveys } from "../hooks/useApi"

function AdminHomePage() {
  const { data: surveys, isLoading } = useQuery("surveys", getSurveys)

  if (isLoading)
    return (
      <Center mt="3rem">
        <Spinner />
      </Center>
    )

  return (
    <Flex minH="100vh" w="100%" bg="gray.100" minW="80rem">
      <VStack mx="auto" my="5rem" spacing="3rem">
        <Heading mx="auto" as="h1" fontSize="5xl">
          Recent Surveys
        </Heading>
        <Grid templateColumns="repeat(3, 1fr)" gap={12} h="100%" w="70rem">
          <GridItem w="100%" h="20rem">
            <NewSurveyCard />
          </GridItem>
          {surveys?.map((survey) => (
            <GridItem w="100%" h="20rem">
              <SurveyCard survey={survey} />
            </GridItem>
          ))}
        </Grid>
      </VStack>
    </Flex>
  )
}

export default AdminHomePage
