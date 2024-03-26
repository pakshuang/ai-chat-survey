import { Box, Button,Flex} from '@chakra-ui/react';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PersonalInfo from './PersonalInfo';
import Question from './Question';
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
  const [personalInfoCompleted,setPersonalInfoCompleted] = useState<boolean>(false);
  const [imageVisible, setImageVisible] = useState(false);
  const [questions, setQuestions] = useState<Question[]>(sampleQuestions);
  const [personalData, setpersonalData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
  });
    useEffect(()=>{
      fetch(`/api/v1/surveys/${survey_id}`).then((rep)=>{
        rep.json().then((data)=>{
          setQuestions(
            []
          )
        })
      }
      ).catch((error)=>{
        console.log(error)
      })
    },[])

    const audio = new Audio('/src/assets/survey/verify-step-complete.mp3');
    audio.volume=1

  const handleSubmit = () => {
    setImageVisible(true);
    audio.play()
    setTimeout(() => {
      navigate('/chat');
    }, 1000);
  };
    const goToNextQuestion = () => {
      setCurrentQuestion(currentQuestion + 1);
    };
  
    const goToPreviousQuestion = () => {
      if (currentQuestion > 0){
        setCurrentQuestion(currentQuestion - 1);
      } else{
        setPersonalInfoCompleted(false)
      }
    };
    const handleQuestionResponse = (id: number, val: string | number) => {
      setQuestions(questions => {
        const updatedQuestions = [...questions];
        updatedQuestions[id].answer = val;
        return updatedQuestions;
      });
    };
    const handlePersonalDataSubmit = (e)=>{
      e.preventDefault();
      setPersonalInfoCompleted(true);
    }
    if (!personalInfoCompleted){
      return <PersonalInfo personalData={personalData} setpersonalData={setpersonalData} handleSubmit={ handlePersonalDataSubmit}>
      </PersonalInfo>
    }
    return (
      <Box maxW="md" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="lg">
          { imageVisible ? <Box>
          <img src="src/assets/survey/tick.svg" alt="Image" />
          Now, lets get onto your talk!
          </Box>
           : <form>
           <Question questionData={questions[currentQuestion]} handleQuestionResponse={handleQuestionResponse}></Question>
            <Flex mt={6} justifyContent="space-between">
                  <Button colorScheme="blue" onClick={goToPreviousQuestion} mr={2}>
                    Previous
                  </Button>
                {currentQuestion < questions.length-1 ? (
                  <Button colorScheme="blue" onClick={goToNextQuestion}  isDisabled={!questions[currentQuestion].answer}>
                    Next
                  </Button>
                ) : (
                  <Button colorScheme="blue" onClick={handleSubmit} isDisabled={!questions[currentQuestion].answer}>
                    Submit
                  </Button>
                )}
            </Flex>
          </form>
            }
      </Box>
    );
  }

export default SurveyPage;
