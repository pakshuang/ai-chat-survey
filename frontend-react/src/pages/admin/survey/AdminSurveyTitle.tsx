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
        autoComplete="off"
        {...register("title", { validate })}
      />
      <Input
        placeholder="Description"
        variant="flushed"
        size="md"
        fontSize="xl"
        mt="1rem"
        autoComplete="off"
        {...register("subtitle", { validate })}
      />
      <Input
        placeholder="Overall context for the chatbot"
        variant="flushed"
        size="md"
        fontSize="xl"
        mt="1rem"
        autoComplete="off"
        {...register("chat_context", { validate, maxLength: 1000 })}
      />
    </Card>
  )
}

export default AdminSurveyTitle
