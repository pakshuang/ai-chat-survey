import { Flex, Grid, GridItem } from "@chakra-ui/react"
import SurveyCard from "./SurveyCard"
import NewSurveyCard from "./NewSurveyCard"

function AdminHomePage() {
  return (
    <Flex minH="100vh" w="100%" bg="gray.100" minW="80rem">
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap={12}
        mx="auto"
        my="10rem"
        h="100%"
        w="70rem"
      >
        <GridItem w="100%" h="20rem">
          <NewSurveyCard />
        </GridItem>
        <GridItem w="100%" h="20rem">
          <SurveyCard />
        </GridItem>
        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />

        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />
        <GridItem w="100%" h="20rem" />
      </Grid>
    </Flex>
  )
}

export default AdminHomePage
