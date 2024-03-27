import axios from "axios"
import { LoginResponse, LoginSignupData } from "../admin/login/constants"
import { Survey } from "../admin/survey/constants"

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

export const submitSurvey = (data: Survey) =>
  AdminApiService(localStorage.getItem("jwt") ?? "")
    .post("/surveys", data)
    .then((res) => {
      console.log(res)
    })
    .catch((e) => {
      console.log(e)
    })
