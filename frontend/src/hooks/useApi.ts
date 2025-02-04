import axios, { AxiosResponse } from "axios"
import { LoginResponse, LoginSignupData } from "../components/admin/login/constants"
import { GetSurvey, Response, Survey } from "../components/admin/survey/constants"
import dayjs from "dayjs"

const baseUrl: string = import.meta.env.VITE_BASE_URL

export const ApiService = axios.create({
  baseURL: baseUrl,
})

export const AdminApiService = (token: string) =>
  axios.create({
    baseURL: baseUrl,
    headers: { Authorization: `Bearer ${token}` },
  })

export const signup = (data: LoginSignupData) =>
  ApiService.post("/admins", data)

export const login = (data: LoginSignupData) =>
  ApiService.post<LoginResponse>("/admins/login", data).then((res) => {
    localStorage.setItem("username", data.username)
    localStorage.setItem("jwt", res.data.jwt)
    localStorage.setItem("jwtExp", res.data.jwt_exp)
  })

export const logout = () => {
  localStorage.removeItem("username")
  localStorage.removeItem("jwt")
  localStorage.removeItem("jwtExp")
}

export const isJwtExpired = () => {
  if (!localStorage.getItem("jwtExp")) return true
  return dayjs(localStorage.getItem("jwtExp")).isBefore(dayjs())
}

export const shouldLogout = () => {
  return (
    !localStorage.getItem("username") ||
    !localStorage.getItem("jwt") ||
    isJwtExpired()
  )
}

export const submitSurvey = (data: Survey) =>
  AdminApiService(localStorage.getItem("jwt") ?? "").post("/surveys", data)

export const getSurveys = async (): Promise<GetSurvey[]> => {
  const username = localStorage.getItem("username") ?? ""
  return AdminApiService(localStorage.getItem("jwt") ?? "")
    .get(`surveys?admin=${username}`)
    .then((res) => res.data)
}

export const getUserSurvey = (survey_id: number): Promise<AxiosResponse> => {
  return ApiService.get(`/surveys/${survey_id}`)
}

export const submitBaseSurvey = (
  survey_id: string,
  body: object
): Promise<AxiosResponse> => {
  return ApiService.post(`/surveys/${survey_id}/responses`, body)
}

export const getSurveyById = async (id: string): Promise<GetSurvey> => {
  return ApiService.get(`/surveys/${id}`).then((res) => res.data)
}

export const getResponseBySurveyId = async (
  id: string
): Promise<Response[]> => {
  return AdminApiService(localStorage.getItem("jwt") ?? "")
    .get(`surveys/${id}/responses`)
    .then((res) => res.data)
}

export const deleteSurvey = (id: string) =>
  AdminApiService(localStorage.getItem("jwt") ?? "")
    .delete(`/surveys/${id}`)
    .then((res) => res.data)

export const sendMessageApi = (
  responseID: number,
  surveyID: number,
  message: string
): Promise<AxiosResponse> => {
  return ApiService.post(
    `/surveys/${surveyID}/responses/${responseID}/chat`,
    { content: message },
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  )
}
