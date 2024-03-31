import {
  Button,
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
import { getSurveys, logout, shouldLogout } from "../hooks/useApi"
import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

function AdminHomePage() {
  const { data: surveys, isLoading, refetch } = useQuery("surveys", getSurveys)

  const navigate = useNavigate()

  useEffect(() => {
    refetch()
  }, [])

  useEffect(() => {
    if (shouldLogout()) {
      logout()
      navigate("/admin/login")
    }
  }, [
    localStorage.getItem("username"),
    localStorage.getItem("jwt"),
    localStorage.getItem("jwtExp"),
  ])

  if (isLoading || !surveys)
    return (
      <Center mt="3rem">
        <Spinner />
      </Center>
    )

  return (
    <Flex minH="100vh" w="100%" bg="gray.100" minW="80rem">
      <VStack mx="auto" my="5rem" spacing="3rem">
        <Flex alignItems="center" justifyContent="space-between" w="full">
          <Flex w="88px"></Flex>
          <Heading mx="auto" as="h1" fontSize="5xl">
            Recent Surveys
          </Heading>
          <Button
            colorScheme="red"
            variant="outline"
            onClick={() => {
              logout()
              navigate("/admin/login")
            }}
          >
            Logout
          </Button>
        </Flex>
        <Grid templateColumns="repeat(3, 1fr)" gap={12} h="100%" w="70rem">
          <GridItem w="100%" h="20rem">
            <NewSurveyCard />
          </GridItem>
          {surveys?.map((survey) => (
            <GridItem w="100%" h="20rem" key={survey.metadata.survey_id}>
              <SurveyCard survey={survey} />
            </GridItem>
          ))}
        </Grid>
      </VStack>
    </Flex>
  )
}

export default AdminHomePage
