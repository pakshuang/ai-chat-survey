import React from "react";
import { Box, FormControl, FormLabel, Input, Button,Flex,IconButton} from '@chakra-ui/react';
import { StarIcon } from '@chakra-ui/icons';
interface RatingQuestionProps {
    questionData: any; // Adjust the type according to your data structure
    handleQuestionResponse: (id: any, key: any, val: any) => void; // Adjust the parameter types according to your requirements
  }
  
const RatingQuestion = ({questionData,handleQuestionResponse}:RatingQuestionProps)=>{
    return <FormControl id="email">
    <FormLabel fontSize="xl"></FormLabel>
    <Flex>
      {[1, 2, 3, 4, 5].map((star) => (
        <Box key={star} as="span" mr="1">
          <IconButton
            aria-label={`Star ${star}`}
            icon={<StarIcon color={star <= (questionData.rating || 0) ? 'teal.500' : 'gray.200'} />}
            onClick={() => handleQuestionResponse(questionData.id,'rating',star)}
          />
        </Box>
      ))}
    </Flex>
    </FormControl>
}

export RatingQuestion