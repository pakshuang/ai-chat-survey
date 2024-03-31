import React from "react";

export type ChatMessageProps = {
  children: React.ReactNode;
  sender: "user" | "bot";
};
export type Messages = {
  sender: "user" | "bot";
  message: string;
  question?: Question;
};

export type ChatWindowProps = {
  messages: Messages[];
  isBotThinking: boolean;
  surveyState:SurveyState;
  handleQuestionResponse: (id: number, val: string | number) => void;
  handleSubmit: () => void;
};

export type Question = {
  question_id: number;
  question: string;
  type: string;
  options?: string[];
  answer?: string | number | string[];
};
export type QuestionProps = {
  questionData: Question;
  handleQuestionResponse: (id: number, val: string | number) => void;
  submitted: boolean;
};

export type SurveyState ={
  displayIndex: number,
  submitted: boolean
  subtitle: string,
  title: string,
  messages:Messages[],
}