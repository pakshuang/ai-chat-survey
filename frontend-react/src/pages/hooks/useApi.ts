import axios from "axios"

const baseUrl = "http://localhost:5000/api/v1"

export const ApiService = axios.create({
  baseURL: baseUrl,
})

export const AdminApiService = (token: string) =>
  axios.create({
    baseURL: baseUrl,
    headers: { Authorization: `Bearer ${token}` },
  })
