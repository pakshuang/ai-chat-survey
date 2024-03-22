export enum QuestionType {
  MCQ = "MCQ",
  MRQ = "MRQ",
  ShortAnswer = "Short Answer",
}

export const needOptions = (type: QuestionType): boolean => {
  return type === QuestionType.MCQ || type === QuestionType.MRQ
}

export type Question = {
  question: string
  type: QuestionType
  options?: { value: string }[]
}

export type Survey = {
  title: string
  description: string
  questions: Question[]
}

export const createNewQuestion = (): Question => {
  return {
    question: "",
    type: QuestionType.MCQ,
    options: [{ value: "" }],
  }
}

export const validate = (str: string) => {
  return str.trim().length > 0
}
