import axios, { AxiosResponse } from "axios"
import { LoginResponse, LoginSignupData } from "../admin/login/constants"
import { GetSurvey, Response, Survey } from "../admin/survey/constants"
import dayjs from "dayjs"
import { getCookie, removeCookie, setCookie } from "typescript-cookie"

const baseUrl: string = import.meta.env.VITE_BASE_URL

export const ApiService = axios.create({
  baseURL: baseUrl,
})

export const AdminApiService = () => {
  const token = getCookie("jwt")
  return axios.create({
    baseURL: baseUrl,
    headers: { Authorization: `Bearer ${token}` },
  })
}

export const signup = (data: LoginSignupData) =>
  ApiService.post("/admins", data)

export const login = (data: LoginSignupData) =>
  ApiService.post<LoginResponse>("/admins/login", data).then((res) => {
    const date = dayjs(res.data.jwt_exp).toDate()
    setCookie("username", data.username)
    setCookie("jwt", res.data.jwt, {
      expires: date,
      httpOnly: true,
      secure: true,
      sameSite: "strict",
    })
  })

export const logout = () => {
  removeCookie("username")
  removeCookie("jwt")
}

export const isJwtExpired = () => {
  return !getCookie("jwt")
}

export const shouldLogout = () => {
  return !getCookie("username") || isJwtExpired()
}

export const submitSurvey = (data: Survey) =>
  AdminApiService().post("/surveys", data)

export const getSurveys = async (): Promise<GetSurvey[]> => {
  const username = getCookie("username")
  return AdminApiService()
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
  return AdminApiService()
    .get(`surveys/${id}/responses`)
    .then((res) => res.data)
}

export const deleteSurvey = (id: string) =>
  AdminApiService()
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
