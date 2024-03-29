import { AddIcon, MinusIcon } from "@chakra-ui/icons"
import { Button, HStack, Input } from "@chakra-ui/react"
import {
  UseFieldArrayInsert,
  UseFieldArrayRemove,
  useFormContext,
} from "react-hook-form"
import { Survey, validate } from "./constants"

function AdminSurveyOption({
  index,
  k,
  insert,
  remove,
}: {
  index: number
  k: number
  insert: UseFieldArrayInsert<Survey, "questions.0.options">
  remove: UseFieldArrayRemove
}) {
  const { register, getValues } = useFormContext<Survey>()

  return (
    <HStack spacing="1rem" justifyContent="flex-start" w="40rem">
      <Input
        variant="flushed"
        placeholder="Option"
        w="25rem"
        autoComplete="off"
        {...register(`questions.${index}.options.${k}.value`, { validate })}
      />
      <Button
        w="3rem"
        colorScheme="blue"
        variant="outline"
        onClick={() => insert(k + 1, { value: "" })}
      >
        <AddIcon />
      </Button>
      {(getValues(`questions.${index}.options`)?.length ?? 0) > 1 && (
        <Button
          w="3rem"
          colorScheme="red"
          variant="outline"
          onClick={() => remove(k)}
        >
          <MinusIcon />
        </Button>
      )}
    </HStack>
  )
}

export default AdminSurveyOption
