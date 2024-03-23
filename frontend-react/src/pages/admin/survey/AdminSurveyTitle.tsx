import { Card, Input } from "@chakra-ui/react"
import { useFormContext } from "react-hook-form"
import { Survey, validate } from "./constants"

function AdminSurveyTitle() {
  const { register } = useFormContext<Survey>()

  return (
    <Card w="48rem" bg="white" p="1.5rem">
      <Input
        placeholder="Untitled"
        variant="flushed"
        size="lg"
        fontSize="4xl"
        fontWeight="bold"
        autoFocus
        {...register("title", { validate })}
      />
      <Input
        placeholder="Description"
        variant="flushed"
        size="md"
        fontSize="xl"
        mt="1rem"
        {...register("description", { validate })}
      />
    </Card>
  )
}

export default AdminSurveyTitle
