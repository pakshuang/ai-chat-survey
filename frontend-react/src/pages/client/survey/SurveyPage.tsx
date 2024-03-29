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
function SurveyPage() {
  const navigate = useNavigate();
  const {survey_id} =useParams()
  const [submitted, setSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [survey,setSurvey]=useState<Survey>(null)
  const [notFound,setNotFound]=useState(false);
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
    ).catch((error)=>{
      setNotFound(true)
    })
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
    console.log(body)
    submitBaseSurvey(body)
    setIsLoading(true);
    setSubmitted(true);
    audio.play()
    setTimeout(() => {
      navigate('/chat');
    }, 1000);
  };
  const handleQuestionResponse = (id: number, val: string | number) => {
    const updatedQuestions = [...survey.questions];
    updatedQuestions[id-1].answer = val;
    Cookies.set(`answers_${survey_id}`, JSON.stringify(updatedQuestions.filter(ele=>ele.answer!==undefined).map(ele=>{
      return ele.answer
    })));
    setSurvey({...survey,questions: updatedQuestions})
  };
  if (notFound){
    return <NotFoundPage></NotFoundPage>
  }
  if (survey==null){
    return null
  }
  if (submitted){
    return <Box maxW="md" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="lg">
      <img src="/src/assets/survey/tick.svg" alt="Image" />
      <Text>Now, let's get onto your talk!</Text>
  </Box>
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
