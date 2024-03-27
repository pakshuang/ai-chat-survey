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
import { submitSurvey } from "../../hooks/useApi"
import dayjs from "dayjs"
import { useNavigate } from "react-router-dom"

function AdminSurveyPage() {
  const methods = useForm<Survey>({
    defaultValues: {
      title: "",
      subtitle: "",
      chat_context: "",
      questions: [createNewQuestion()],
      metadata: {
        name: "",
        description: "",
        created_by: localStorage.getItem("username") ?? "",
        created_at: "",
      },
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
  const navigate = useNavigate()

  const { handleSubmit } = methods

  const onSubmit = (data: Survey) => {
    data.questions.forEach((q, i) => {
      q.id = i
      // @ts-ignore
      const options: string[] = q.options?.map((o) => o.value) ?? []
      q.options = options
    })
    data.metadata.created_at = dayjs().format("YYYY-MM-DD HH:mm:ss")
    console.log(data)
    submitSurvey(data)
      .then((res) => {
        console.log(res)
        toast({
          title: "New survey created",
          status: "success",
          isClosable: true,
        })
        navigate("/admin/survey")
      })
      .catch((e) => {
        console.log(e)
      })
  }

  const onInvalid = () => {
    const errors = methods.formState.errors
    const errorKeys = Object.keys(methods.formState.errors)
    if (
      errorKeys.includes("chat_context") &&
      errors["chat_context"]?.type === "maxLength"
    ) {
      toast({
        title: "Please keep chatbot context less than 1000 characters",
        status: "error",
        isClosable: true,
      })
      return
    }
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
