import axios from "axios"
import { LoginResponse, LoginSignupData } from "../admin/login/constants"

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
    localStorage.setItem("jwt", res.data.jwt)
    localStorage.setItem("jwtExp", res.data.jwt_exp)
  })
