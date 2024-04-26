export enum QuestionType {
  MCQ = "multiple_choice",
  MRQ = "multiple_response",
  FreeResponse = "free_response",
}

export const needOptions = (type: QuestionType): boolean => {
  return type === QuestionType.MCQ || type === QuestionType.MRQ
}

export type Question = {
  question_id: number
  question: string
  type: QuestionType
  options?: (string | { value: string })[]
}

export type Survey = {
  title: string
  subtitle: string
  chat_context: string
  questions: Question[]
  metadata: SurveyMetadata
}

export type SurveyMetadata = {
  name: string
  description: string
  created_by: string
  created_at: string
}

export const createNewQuestion = (): Question => {
  return {
    question_id: 0,
    question: "",
    type: QuestionType.MCQ,
    options: [{ value: "" }],
  }
}

export const validate = (str: string) => {
  return str.trim().length > 0
}

export type GetSurveyMetadata = SurveyMetadata & {
  survey_id: number
}

export type GetSurvey = {
  title: string
  subtitle: string
  chat_context: string
  questions: Question[]
  metadata: GetSurveyMetadata
}

export type Answer = {
  question_id: number
  type: string
  question: string
  options: string[]
  answer: string[]
}

export type Response = {
  metadata: {
    survey_id: number
    response_id: number
    submitted_at: string
  }
  answers: Answer[]
  messages: {
    content: string
    role: string
  }[]
}
