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
  Link,
  Select,
  Spinner,
  Text,
  VStack,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  useDisclosure,
} from "@chakra-ui/react";
import { useQuery } from "react-query";
import {
  ArrowBackIcon,
  InfoIcon,
  DeleteIcon,
  ViewIcon,
} from "@chakra-ui/icons";
import { useNavigate, useParams } from "react-router-dom";
import {
  getSurveyById,
  getSurveys,
  logout,
  shouldLogout,
  deleteSurvey,
} from "../../../hooks/useApi";
import { needOptions, QuestionType } from "../../../components/admin/survey/constants";
import { useEffect } from "react";
import ViewAdminSurveyTitle from "../../../components/admin/survey/ViewAdminSurveyTitle";
import Header from "../../../components/admin/survey/Header";

function ViewAdminSurvey() {
  const { id } = useParams();

  const { data: surveys } = useQuery("surveys", getSurveys);

  const { data: survey, isLoading } = useQuery(`survey-${id}`, () =>
    getSurveyById(id ?? "0")
  );

  const navigate = useNavigate();
  const toast = useToast();

  const { isOpen, onOpen, onClose } = useDisclosure();

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
    <Flex
      minH="100vh"
      w="100%"
      bg="gray.100"
      minW="80rem"
      flexDirection="column"
    >
      <Header />
      <VStack mx="auto" my="3rem" spacing="0" w="48rem">
        <Card w="48rem" bg="gray.50" p="1.5rem" mb="1rem">
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
        <ViewAdminSurveyTitle survey={survey} />
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
                  <Input
                    value={question.question}
                    variant="unstyled"
                    size="md"
                    fontSize="xl"
                    fontWeight="bold"
                    w="42rem"
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
            leftIcon={<ViewIcon />}
            colorScheme="green"
            onClick={() => {
              navigate(`/admin/survey/${id}/responses`);
            }}
          >
            View responses
          </Button>
          <Button leftIcon={<DeleteIcon />} colorScheme="red" onClick={onOpen}>
            Delete survey
          </Button>
        </Box>
        <Modal
          isCentered
          onClose={onClose}
          isOpen={isOpen}
          motionPreset="slideInBottom"
          closeOnOverlayClick={false}
        >
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Delete this survey?</ModalHeader>
            <ModalCloseButton />
            <ModalBody>This action cannot be undone.</ModalBody>
            <ModalFooter>
              <Button variant="ghost" mr={3} onClick={onClose}>
                Close
              </Button>
              <Button
                colorScheme="red"
                onClick={async () => {
                  await deleteSurvey(id ?? "0").then(() => {
                    toast({
                      title: "Survey deleted",
                      status: "success",
                      isClosable: true,
                    });
                  });
                  navigate("/admin/survey");
                }}
              >
                Confirm
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </VStack>
    </Flex>
  );
}

export default ViewAdminSurvey;
