import { Box, Text, Button,Flex, CircularProgress} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';
import Question from './Question';
import NotFoundPage from './NotFoundPage';
import ResumeSnackbar from './ResumeToast';
const sampleQuestions = [
  {
    id: 0,
    question: "What is your favorite color?",
    type: "multiple_choice",
    options: ["Red", "Blue", "Green", "Yellow"]
  },
  {
    id: 1,
    question: "Rate your experience with our service:",
    type: "rating"
  },
  {
    id: 2,
    question: "What is the capital of France?",
    type: "short_answer"
  },
  {
    id: 3,
    question: "Please provide feedback:",
    type: "long_answer"
  }
];

const sampleSurvey ={
  "metadata": {
    "id": "integer",
    "name": "string",
    "description": "string",
    "created_by": "string",
    "created_at": "string",
  },
  "title": "title",
  "subtitle": "subtitle",
  'questions':sampleQuestions,
}

interface Props {
  survey_id: number;
}


function SurveyPage({survey_id}:Props) {
  const navigate = useNavigate();
  const [submitted, setSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [survey,setSurvey]=useState(sampleSurvey)
  const [error,setError]=useState(false);
  const answersCookie = Cookies.get(`answers_${survey_id}`);
  const answers = answersCookie ? JSON.parse(answersCookie) : [];
  useEffect(()=>{
    axios.get(`/api/v1/surveys/${survey_id}`).then((rep)=>{
      setSurvey(rep.data)
    }
    ).catch((error)=>{

    }).finally(()=>{
        const answeredQuestions = survey.questions.map((question, index) => {
            return {
                ...question,
                id: index,
                answer: answers[index]
            };
        });
        setSurvey({...survey,questions: answeredQuestions})
    })
  },[survey_id])
  const audio = new Audio('/src/assets/survey/verify-step-complete.mp3');
  audio.volume=1

  const handleSubmit = () => {
    const body ={
      "metadata": {
        "survey_id": survey_id
      },
      "answers": survey.questions
    }
    setIsLoading(true);
    setSubmitted(true);
    audio.play()
    setTimeout(() => {
      navigate('/chat');
    }, 1000);
    axios.post(`/api/v1/responses`,body).then(()=>{

    }).catch((error)=>{

    }).finally(()=>{
      setIsLoading(false);
    })
  };
  const handleQuestionResponse = (id: number, val: string | number) => {
    const updatedQuestions = [...survey.questions];
    updatedQuestions[id].answer = val;
    Cookies.set(`answers_${survey_id}`, JSON.stringify(updatedQuestions.filter(ele=>ele.answer!==undefined).map(ele=>{
      return ele.answer
    })));
    setSurvey({...survey,questions: updatedQuestions})
  };
  if (error){
    return <NotFoundPage></NotFoundPage>
  }
  if (submitted){
    return <Box maxW="md" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="lg">
    <Flex align="center">
      <img src="src/assets/survey/tick.svg" alt="Image" />
      <Text ml={3}>Now, let's get onto your talk!</Text>
    </Flex>
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
      <form>
            {
              survey.questions.map((question)=>{
                return <Box maxW="md" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="lg">
                  <Question questionData={question} handleQuestionResponse={handleQuestionResponse}></Question>
                </Box>
              })
            } 
          <Box maxW="md" mx="auto" mt={6}>
            <Flex justifyContent="flex-end">
              {isLoading ? <CircularProgress> </CircularProgress> :
                <Button colorScheme="blue" onClick={handleSubmit} >
                  Submit
                </Button>
              }
            </Flex>
          </Box>
        </form>
    </Box>
  );
}

export default SurveyPage;
