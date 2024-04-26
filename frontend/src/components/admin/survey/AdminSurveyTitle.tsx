import {
  Box,
  Card,
  Input,
  Textarea,
  Text,
  FormControl,
  FormHelperText,
  Tooltip,
} from "@chakra-ui/react";
import { useFormContext } from "react-hook-form";
import { Survey, validate } from "./constants";
import { QuestionIcon } from "@chakra-ui/icons";

function AdminSurveyTitle() {
  const { register } = useFormContext<Survey>();

  return (
    <Card w="48rem" bg="white" p="1.5rem">
      <FormControl>
        <Input
          placeholder="Untitled"
          variant="flushed"
          size="md"
          fontSize="3xl"
          fontWeight="bold"
          autoFocus
          autoComplete="off"
          {...register("title", { validate })}
        />
      </FormControl>
      <FormControl>
        <Textarea
          placeholder="Description"
          size="md"
          fontSize="lg"
          mt="1rem"
          autoComplete="off"
          rows={2}
          resize="vertical"
          {...register("subtitle", { validate })}
        />
      </FormControl>
      <FormControl>
        <Textarea
          placeholder="Overall chat context for the chatbot"
          size="md"
          fontSize="md"
          mt="1rem"
          autoComplete="off"
          rows={3}
          resize="vertical"
          {...register("chat_context", { validate, maxLength: 1000 })}
        />
        <Tooltip
          hasArrow
          label={
            <Text>
              Chat context gives the chatbot specific information on what
              insights you want to glean from your respondents so it can
              finetune the questions it generates accordingly. It will not be
              shown to your respondents.
            </Text>
          }
        >
          <Box w="fit-content">
            <FormHelperText>
              <QuestionIcon mr="5px" />
              What's chat context?
            </FormHelperText>
          </Box>
        </Tooltip>
      </FormControl>
    </Card>
  );
}

export default AdminSurveyTitle;
