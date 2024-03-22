import {
  Accordion,
  Button,
  Flex,
  HStack,
  VStack,
  useToast,
} from "@chakra-ui/react"
import AdminSurveyAccordion from "./AdminSurveyAccordion"
import { AddIcon, ExternalLinkIcon } from "@chakra-ui/icons"
import { useForm, FormProvider, useFieldArray } from "react-hook-form"
import { createNewQuestion, Survey } from "./constants"
import AdminSurveyTitle from "./AdminSurveyTitle"
import { useState } from "react"

function AdminSurveyPage() {
  const methods = useForm<Survey>({
    defaultValues: {
      title: "",
      description: "",
      questions: [createNewQuestion()],
    },
    mode: "onSubmit",
  })

  const [openIndex, setOpenIndex] = useState([0])

  const {
    fields: questions,
    append,
    remove,
  } = useFieldArray({
    control: methods.control,
    name: "questions",
  })

  const toast = useToast()

  const { handleSubmit } = methods

  const onSubmit = (data: Survey) => console.log(data)

  const onInvalid = () => {
    if (Object.keys(methods.formState.errors).length > 0) {
      toast({
        title: "Please fill all fields",
        status: "error",
        isClosable: true,
      })
    }
  }

  return (
    <FormProvider {...methods}>
      <Flex minH="100vh" w="100%" bg="gray.100" minW="80rem">
        <VStack mx="auto" my="5rem" spacing="0" w="48rem">
          <AdminSurveyTitle />
          <Accordion allowMultiple index={openIndex}>
            {questions.map((question, index) => (
              <AdminSurveyAccordion
                key={question.id}
                index={index}
                openIndex={openIndex}
                setOpenIndex={setOpenIndex}
                remove={remove}
              />
            ))}
          </Accordion>
          <HStack mt="1rem" w="full">
            <Button
              leftIcon={<AddIcon />}
              colorScheme="green"
              h="3rem"
              w="50%"
              onClick={() => {
                append(createNewQuestion())
                setOpenIndex(openIndex.concat(questions.length))
              }}
            >
              Add Question
            </Button>
            <Button
              leftIcon={<ExternalLinkIcon />}
              colorScheme="messenger"
              h="3rem"
              w="50%"
              onClick={handleSubmit(onSubmit, onInvalid)}
            >
              Create Survey
            </Button>
          </HStack>
        </VStack>
      </Flex>
    </FormProvider>
  )
}

export default AdminSurveyPage
