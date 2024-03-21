import { Flex, Grid, GridItem } from "@chakra-ui/react"

function AdminHomePage() {
  return (
    <Flex minH="100vh" w="100%" bg="gray.100">
      <Grid
        templateColumns="repeat(3, 1fr)"
        gap={8}
        mx="auto"
        my="10rem"
        h="100%"
        w="60vw"
        bg="gray.300"
      >
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />

        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
        <GridItem w="100%" h="20rem" bg="blue.500" />
      </Grid>
    </Flex>
  )
}

export default AdminHomePage
