import { Flex, Grid, GridItem, Heading, VStack } from "@chakra-ui/react"
import SurveyCard from "./SurveyCard"
import NewSurveyCard from "./NewSurveyCard"

function AdminHomePage() {
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
          <GridItem w="100%" h="20rem">
            <SurveyCard />
          </GridItem>
          <GridItem w="100%" h="20rem">
            <SurveyCard />
          </GridItem>
          <GridItem w="100%" h="20rem">
            <SurveyCard />
          </GridItem>
          <GridItem w="100%" h="20rem">
            <SurveyCard />
          </GridItem>
        </Grid>
      </VStack>
    </Flex>
  )
}

export default AdminHomePage
