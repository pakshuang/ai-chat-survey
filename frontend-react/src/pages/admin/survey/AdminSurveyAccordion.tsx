import { DeleteIcon } from "@chakra-ui/icons"
import {
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Flex,
  Input,
  Select,
  Button,
  VStack,
} from "@chakra-ui/react"
import AdminSurveyOptions from "./AdminSurveyOptions"
import { UseFieldArrayRemove, useFormContext, useWatch } from "react-hook-form"
import { needOptions, QuestionType, Survey, validate } from "./constants"
import { uniq } from "lodash"

function AdminSurveyAccordion({
  index,
  openIndex,
  setOpenIndex,
  remove,
}: {
  index: number
  openIndex: number[]
  setOpenIndex: React.Dispatch<React.SetStateAction<number[]>>
  remove: UseFieldArrayRemove
}) {
  const { register, control, getValues } = useFormContext<Survey>()

  const type = useWatch({
    control,
    name: `questions.${index}.type`,
  })

  const onClick = () => {
    if (openIndex.includes(index)) {
      openIndex = openIndex.filter((i) => i !== index)
    } else {
      openIndex.push(index)
    }
    setOpenIndex(uniq(openIndex))
  }

  return (
    <AccordionItem
      w="48rem"
      bg="white"
      borderTop={0}
      borderRadius={5}
      mt="1rem"
    >
      <AccordionButton
        h="5rem"
        borderBottom="1px"
        borderColor="gray.200"
        onClick={onClick}
      >
        <Flex
          alignItems="center"
          justifyContent="space-between"
          w="full"
          p="0.5rem"
        >
          <Input
            placeholder="Question"
            variant="unstyled"
            size="lg"
            fontSize="2xl"
            fontWeight="bold"
            w="42rem"
            onClick={(e) => e.stopPropagation()}
            onKeyUp={(e) => e.preventDefault()}
            {...register(`questions.${index}.question`, { validate })}
          />
          <AccordionIcon />
        </Flex>
      </AccordionButton>
      <AccordionPanel p="1.5rem">
        <VStack spacing="2rem" alignItems="flex-start">
          <Select
            defaultValue={QuestionType.MCQ}
            {...register(`questions.${index}.type`)}
            _hover={{ cursor: "pointer" }}
          >
            <option value={QuestionType.MCQ}>Multiple Choice Question</option>
            <option value={QuestionType.MRQ}>Multiple Response Question</option>
            <option value={QuestionType.ShortAnswer}>Short Answer</option>
            <option value={QuestionType.LongAnswer}>Long Answer</option>
          </Select>
          {needOptions(type) && (
            <AdminSurveyOptions index={index} control={control} />
          )}
          {getValues(`questions`).length > 1 && (
            <Button
              leftIcon={<DeleteIcon />}
              colorScheme="red"
              variant="outline"
              onClick={() => remove(index)}
            >
              Delete
            </Button>
          )}
        </VStack>
      </AccordionPanel>
    </AccordionItem>
  )
}

export default AdminSurveyAccordion
