import { AddIcon, MinusIcon } from "@chakra-ui/icons"
import { Button, HStack, Input } from "@chakra-ui/react"

function AdminSurveyOption() {
  return (
    <HStack spacing="1rem" justifyContent="flex-start" w="70%">
      <Input variant="flushed" placeholder="Option" />
      <Button w="3rem" colorScheme="blue" variant="outline">
        <AddIcon />
      </Button>
      <Button w="3rem" colorScheme="red" variant="outline">
        <MinusIcon />
      </Button>
    </HStack>
  )
}

export default AdminSurveyOption
