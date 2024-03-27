import { Box, Button,Flex, CircularProgress} from '@chakra-ui/react';
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


interface Props {
  survey_id: number;
}


function SurveyPage({survey_id}:Props) {
  const navigate = useNavigate();
  const [currentQuestion, setCurrentQuestion] = useState<number>(0);
  const [submitted, setSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error,setError]=useState(false);
  const [questions, setQuestions] = useState<Question[]>(sampleQuestions);
  const answersCookie = Cookies.get(`answers_${survey_id}`);
  const answers = answersCookie ? JSON.parse(answersCookie) : [];
  useEffect(()=>{
    axios.get(`/api/v1/surveys/${survey_id}`).then((rep)=>{
      setQuestions(
        rep.questions.map((ele,index)=>{
          ele.id=index
          return ele
        })
      )
    }
    ).catch((error)=>{
    }).finally(()=>{
      console.log(answers)
      setCurrentQuestion(Math.min(answers.length,questions.length-1))
        const mappedQuestions = questions.map((question, index) => {
            return {
                ...question,
                id: index,
                answer: answers[index]
            };
        });
        setQuestions(mappedQuestions)
    })
  },[survey_id])
  const audio = new Audio('/src/assets/survey/verify-step-complete.mp3');
  audio.volume=1

  const handleSubmit = () => {
    const body ={
      "metadata": {
        "survey_id": survey_id
      },
      "answers": questions
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
  const goToNextQuestion = () => {
    setCurrentQuestion(currentQuestion + 1);
  };

  const goToPreviousQuestion = () => {
    if (currentQuestion > 0){
      setCurrentQuestion(currentQuestion - 1);
    } 
  };
  const handleQuestionResponse = (id: number, val: string | number) => {
    setQuestions(questions => {
      const updatedQuestions = [...questions];
      updatedQuestions[id].answer = val;
      Cookies.set(`answers_${survey_id}`, JSON.stringify(updatedQuestions.filter(ele=>ele.answer!==undefined).map(ele=>{
        return ele.answer
      })));
      return updatedQuestions;
    });
  };
  if (error){
    return <NotFoundPage></NotFoundPage>
  }
  return (
    <>
    <Box maxW="md" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="lg">
        { submitted ? <Box>
        <img src="src/assets/survey/tick.svg" alt="Image" />
        Now, lets get onto your talk!
        </Box>
          : <form>
          <Question questionData={questions[currentQuestion]} handleQuestionResponse={handleQuestionResponse}></Question>
          <Flex mt={6} justifyContent="flex-end">
          {currentQuestion >0 &&<Button colorScheme="blue" onClick={goToPreviousQuestion} mr={2}>
                  Previous
                </Button>}
              {currentQuestion < questions.length-1 ? (
                <Button colorScheme="blue" onClick={goToNextQuestion}  isDisabled={!questions[currentQuestion].answer}>
                  Next
                </Button>
              ) : (
              isLoading ? <CircularProgress> </CircularProgress> :
                <Button colorScheme="blue" onClick={handleSubmit} isDisabled={!questions[currentQuestion].answer}>
                  Submit
                </Button>
              )}
          </Flex>
        </form>
          }
    </Box>
    <ResumeSnackbar answers ={answers}/>
    </>
  );
}

export default SurveyPage;
