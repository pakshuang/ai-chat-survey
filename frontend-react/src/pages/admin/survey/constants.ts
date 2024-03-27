export enum QuestionType {
  MCQ = "multiple_choice",
  MRQ = "multiple_response",
  ShortAnswer = "short_answer",
  LongAnswer = "long_answer",
}

export const needOptions = (type: QuestionType): boolean => {
  return type === QuestionType.MCQ || type === QuestionType.MRQ
}

export type Question = {
  id: number
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
    id: 0,
    question: "",
    type: QuestionType.MCQ,
    options: [{ value: "" }],
  }
}

export const validate = (str: string) => {
  return str.trim().length > 0
}
