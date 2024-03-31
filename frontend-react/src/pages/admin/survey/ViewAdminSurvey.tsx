import {
  Accordion,
  AccordionButton,
  Box,
  Button,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Card,
  Center,
  Flex,
  HStack,
  Input,
  Textarea,
  Link,
  Select,
  Spinner,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";
import { useQuery } from "react-query";
import { ArrowBackIcon, InfoIcon, WarningIcon } from "@chakra-ui/icons";
import { useNavigate, useParams } from "react-router-dom";
import {
  getSurveyById,
  getSurveys,
  logout,
  shouldLogout,
  deleteSurvey,
} from "../../hooks/useApi";
import { needOptions, QuestionType } from "./constants";
import { useEffect } from "react";

function ViewAdminSurvey() {
  const { id } = useParams();

  const { data: surveys } = useQuery("surveys", getSurveys);

  const { data: survey, isLoading } = useQuery(`survey-${id}`, () =>
    getSurveyById(id ?? "0")
  );

  const navigate = useNavigate();
  const toast = useToast();

  useEffect(() => {
    const ids = surveys?.map((s) => s.metadata.survey_id);
    if (ids && !ids.includes(parseInt(id ?? "0"))) navigate("/admin/404");
  }, [surveys]);

  useEffect(() => {
    if (shouldLogout()) {
      logout();
      navigate("/admin/login");
    }
  }, [
    localStorage.getItem("username"),
    localStorage.getItem("jwt"),
    localStorage.getItem("jwtExp"),
  ]);

  if (isLoading || !survey)
    return (
      <Center mt="3rem">
        <Spinner />
      </Center>
    );

  return (
    <Flex minH="100vh" w="100%" bg="gray.100" minW="80rem">
      <VStack mx="auto" my="5rem" spacing="0" w="48rem">
        <Card w="48rem" bg="gray.50" p="1.5rem">
          <HStack>
            <InfoIcon />
            <Text>
              Want to view the survey interface instead? Click{" "}
              <Link fontWeight="700" href={`/chat/${id}`}>
                here.
              </Link>
            </Text>
          </HStack>
        </Card>
        <Card w="48rem" bg="white" p="1.5rem" mt="1rem">
          <Textarea
            value={survey.title}
            variant="flushed"
            size="lg"
            fontSize="4xl"
            fontWeight="bold"
            rows={1}
            resize="none"
            isReadOnly
          />
          <Textarea
            value={survey.subtitle}
            variant="flushed"
            size="md"
            fontSize="xl"
            mt="1rem"
            rows={1}
            resize="none"
            isReadOnly
          />
          <Textarea
            value={survey.chat_context}
            variant="flushed"
            size="md"
            fontSize="xl"
            mt="1rem"
            rows={1}
            resize="none"
            isReadOnly
          />
        </Card>
        <Accordion
          allowMultiple
          defaultIndex={survey.questions?.map((_, i) => i)}
        >
          {survey.questions?.map((question) => (
            <AccordionItem
              w="48rem"
              bg="white"
              borderTop={0}
              borderRadius={5}
              mt="1rem"
              key={question.question_id}
            >
              <AccordionButton
                h="5rem"
                borderBottom="1px"
                borderColor="gray.200"
              >
                <Flex
                  alignItems="center"
                  justifyContent="space-between"
                  w="full"
                  p="0.5rem"
                >
                  <Textarea
                    value={question.question}
                    variant="unstyled"
                    size="lg"
                    fontSize="2xl"
                    fontWeight="bold"
                    w="42rem"
                    rows={1}
                    resize="none"
                    isReadOnly
                  />
                  <AccordionIcon />
                </Flex>
              </AccordionButton>
              <AccordionPanel p="1.5rem">
                <VStack spacing="2rem" alignItems="flex-start">
                  <Select value={question.type} isDisabled>
                    <option value={QuestionType.MCQ}>
                      Multiple Choice Question
                    </option>
                    <option value={QuestionType.MRQ}>
                      Multiple Response Question
                    </option>
                    <option value={QuestionType.FreeResponse}>
                      Free Response
                    </option>
                  </Select>
                  {needOptions(question.type) &&
                    question.options?.map((o, i) => (
                      <Input
                        // @ts-ignore
                        value={o}
                        variant="flushed"
                        w="25rem"
                        isReadOnly
                        key={i}
                      />
                    ))}
                </VStack>
              </AccordionPanel>
            </AccordionItem>
          ))}
        </Accordion>
        <Box mt="2rem" display="flex" gap="0.5rem">
          <Button
            leftIcon={<ArrowBackIcon />}
            colorScheme="blue"
            onClick={() => {
              navigate("/admin/survey");
            }}
          >
            Back to home
          </Button>
          <Button
            leftIcon={<WarningIcon />}
            colorScheme="red"
            onClick={async () => {
              await deleteSurvey(id ?? "0").then((res) => {
                toast({
                  title: "Survey deleted",
                  status: "success",
                  isClosable: true,
                });
              });
              navigate("/admin/survey");
            }}
          >
            Delete survey
          </Button>
        </Box>
      </VStack>
    </Flex>
  );
}

export default ViewAdminSurvey;
