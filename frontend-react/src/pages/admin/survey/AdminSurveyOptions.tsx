import { VStack } from "@chakra-ui/react"
import AdminSurveyOption from "./AdminSurveyOption"
import { Control, useFieldArray } from "react-hook-form"
import { Survey } from "./constants"

function AdminSurveyOptions({
  index,
  control,
}: {
  index: number
  control: Control<Survey>
}) {
  const { fields, insert, remove } = useFieldArray({
    control,
    name: `questions.${index}.options` as `questions.0.options`,
  })

  return (
    <VStack w="100%" alignItems="flex-start">
      {fields.map((option, k) => (
        <AdminSurveyOption
          key={option.id}
          index={index}
          k={k}
          insert={insert}
          remove={remove}
        />
      ))}
    </VStack>
  )
}

export default AdminSurveyOptions
