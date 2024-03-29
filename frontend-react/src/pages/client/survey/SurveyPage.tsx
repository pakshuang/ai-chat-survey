import { Box, Text, Button,Flex } from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { useNavigate, useParams } from 'react-router-dom';
import Question from './Question';
import NotFoundPage from './NotFoundPage';
import { getUserSurvey,submitBaseSurvey } from '../../hooks/useApi';

interface Survey {
  title: string;
  subtitle: string;
  chat_context: string;
  metadata: {
    created_at: string;
    created_by: string;
    description: string;
    id: number;
    name: string;
  };
  questions: {
    id: number;
    question_id:number;
    question: string;
    type: string;
    options?: string[];
  }[];
}
interface Props {
  survey_id:number;
}
function SurveyPage({survey_id}:Props) {
  const [survey,setSurvey]=useState<Survey>(null)
  const answersCookie = Cookies.get(`answers_${survey_id}`);
  const answers = answersCookie ? JSON.parse(answersCookie) : [];
  useEffect(()=>{
    getUserSurvey(survey_id).then((rep)=>{
      const answeredQuestions = rep.data.questions.map((question, index) => {
        return {
            ...question,
            answer: answers[index]
        };
      });
      setSurvey({...rep.data,questions: answeredQuestions})
    }
    )
  },[survey_id])

  const handleSubmit = (event) => {
    event.preventDefault();
    const body ={
      "metadata": {
        "survey_id": survey_id
      },
      "answers": survey.questions.map(ele=>{
        ele.question_id=ele.id;
        return ele
      })
    }
    submitBaseSurvey(body)
  };
  const handleQuestionResponse = (id: number, val: string | number) => {
    const updatedQuestions = [...survey.questions];
    updatedQuestions[id-1].answer = val;
    Cookies.set(`answers_${survey_id}`, JSON.stringify(updatedQuestions.filter(ele=>ele.answer!==undefined).map(ele=>{
      return ele.answer
    })));
    setSurvey({...survey,questions: updatedQuestions})
  };
  if (survey==null){
    return null
  }
  return (
    <Box>
      <Box
        maxW="md"
        mx="auto"
        mt={10}
        p={6}
        borderWidth="1px"
        borderRadius="lg"
      >
        <Text fontWeight="bold" fontSize="xl" mb={2}>{survey.title}</Text>
        <Text >{survey.subtitle}</Text>
      </Box>
      <form onSubmit={handleSubmit}>
            {
              survey.questions.map((question)=>{
                return <Box maxW="md" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="lg">
                  <Question questionData={question} handleQuestionResponse={handleQuestionResponse}></Question>
                </Box>
              })
            } 
          <Box maxW="md" mx="auto" mt={6}>
            <Flex justifyContent="flex-end">
                <Button colorScheme="blue"   type="submit" disabled={isLoading}>
                  Submit
                </Button>
            </Flex>
          </Box>
        </form>
    </Box>
  );
}

export default SurveyPage;
