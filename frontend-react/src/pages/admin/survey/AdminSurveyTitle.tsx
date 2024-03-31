import { Card, Input, Textarea } from "@chakra-ui/react"
import { useFormContext } from "react-hook-form"
import { Survey, validate } from "./constants"

function AdminSurveyTitle() {
  const { register } = useFormContext<Survey>()

  return (
    <Card w="48rem" bg="white" p="1.5rem">
      <Input
        placeholder="Untitled"
        variant="flushed"
        size="md"
        fontSize="3xl"
        fontWeight="bold"
        autoFocus
        autoComplete="off"
        {...register("title", { validate })}
      />
      <Textarea
        placeholder="Description"
        size="md"
        fontSize="lg"
        mt="1rem"
        autoComplete="off"
        rows={2}
        resize="vertical"
        {...register("subtitle", { validate })}
      />
      <Textarea
        placeholder="Overall context for the chatbot"
        size="md"
        fontSize="md"
        mt="1rem"
        autoComplete="off"
        rows={3}
        resize="vertical"
        {...register("chat_context", { validate, maxLength: 1000 })}
      />
    </Card>
  )
}

export default AdminSurveyTitle
