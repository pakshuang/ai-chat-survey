import {
  Center,
  Flex,
  HStack,
  IconButton,
  Spinner,
  Text,
  VStack,
} from "@chakra-ui/react";
import { useNavigate, useParams } from "react-router-dom";
import ViewAdminSurveyTitle from "../../../components/admin/survey/ViewAdminSurveyTitle";
import { useQuery } from "react-query";
import {
  getResponseBySurveyId,
  getSurveyById,
  getSurveys,
} from "../../../hooks/useApi";
import { useEffect, useState } from "react";
import AdminSurveyResponse from "../../../components/admin/survey/AdminSurveyResponse";
import { ChevronLeftIcon, ChevronRightIcon } from "@chakra-ui/icons";
import Header from "../../../components/admin/survey/Header";

function AdminSurveyResponses() {
  const { id } = useParams();

  const { data: surveys } = useQuery("surveys", getSurveys);

  const { data: survey, isLoading } = useQuery(`survey-${id}`, () =>
    getSurveyById(id ?? "0")
  );

  const { data: responses, isLoading: loading } = useQuery(
    `survey-${id}-responses`,
    () => getResponseBySurveyId(id ?? "0")
  );

  const navigate = useNavigate();

  const [index, setIndex] = useState(0);

  useEffect(() => {
    const ids = surveys?.map((s) => s.metadata.survey_id);
    if (ids && !ids.includes(parseInt(id ?? "0"))) navigate("/admin/404");
  }, [surveys]);

  if (isLoading || loading || !survey || !responses)
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
      <VStack mx="auto" my="3rem" spacing="1rem" w="48rem">
        <ViewAdminSurveyTitle survey={survey} />
        {responses.length === 0 ? (
          <Text>No responses</Text>
        ) : (
          <>
            <HStack>
              <IconButton
                aria-label="prev"
                icon={<ChevronLeftIcon />}
                size="lg"
                onClick={() =>
                  setIndex((index - 1 + responses.length) % responses.length)
                }
              />
              <Text>{`${index + 1}/${responses.length}`}</Text>
              <IconButton
                aria-label="next"
                icon={<ChevronRightIcon />}
                size="lg"
                onClick={() => setIndex((index + 1) % responses.length)}
              />
            </HStack>
            <AdminSurveyResponse response={responses[index]} />
          </>
        )}
      </VStack>
    </Flex>
  );
}

export default AdminSurveyResponses;
