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
  surveyState: any;
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
  questionData?: Question;
  handleQuestionResponse: (id: number, val: string | number) => void;
  submitted: boolean;
};

export type MultipleChoiceInputProps = {
  questionID: number;
  options: string[];
  handleQuestionResponse: (id: number, val: string | number) => void;
}

export type MultipleResponseInputProps = {
  questionID: number;
  options: string[];
  handleQuestionResponse: (id: number, val: string | number) => void;
}

export const surveyMessage =
  "You've submitted the first part of our survey! Hang on tight while we process your responses...";
