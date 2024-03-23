import { Box, Button,Flex} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'
import PersonalInfo from './PersonalInfo';

interface Props {
  survey_id: number;
}

function SurveyPage({survey_id}:Props) {
  const [currentQuestion, setCurrentQuestion] = useState<number>(0);
  const [completedQuestion, setCompletedQuestion] = useState<number>(0);
  const [personalInfoSubmitted,setPersonalInfoSubmitted] = useState<boolean>(false);
  const [questions, setQuestions] = useState([]);
    useEffect(()=>{
      axios.get(`/api/v1/surveys/${survey_id}`).then((rep)=>{
        setQuestions(
          []
        )
      }
      ).catch((error)=>{
        console.log(error)
      })
    },[])
    const navigate = useNavigate();
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      console.log('Form submitted');
      navigate('/chat');
    };


    const audio = new Audio('/assets/survey/verify-step-complete');
    const goToNextQuestion = () => {
      if (completedQuestion===currentQuestion){
        setCompletedQuestion(currentQuestion+1)
        audio.play();
      }
      setCurrentQuestion(currentQuestion + 1);
    };
  
    const goToPreviousQuestion = () => {
      setCurrentQuestion(currentQuestion - 1);
    };
    const handleQuestionResponse = (id, key, val) => {
      setQuestions(questions => {
        questions[id] = {
          ...questions[id],
          [key]: val
        };
        return questions;
      });
    };
    if (!personalInfoSubmitted){
      return <PersonalInfo setPersonalInfoSubmitted={setPersonalInfoSubmitted}>

      </PersonalInfo>
    }
    return (
      <Box maxW="md" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="lg">
        <form onSubmit={handleSubmit}>
          <Flex mt={6} justifyContent="flex-end">
              {currentQuestion > 0 && (
                <Button colorScheme="blue" onClick={goToPreviousQuestion} mr={2}>
                  Previous
                </Button>
              )}
              {currentQuestion < questions.length - 1 ? (
                <Button colorScheme="blue" onClick={goToNextQuestion}>
                  Next
                </Button>
              ) : (
                <Button colorScheme="blue" type="submit">
                  Submit
                </Button>
              )}
          </Flex>
        </form>
      </Box>
    );
  }

export default SurveyPage;
