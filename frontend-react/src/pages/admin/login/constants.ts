export type LoginSignupData = {
  username: string
  password: string
}

export type LoginResponse = {
  jwt: string
  jwt_exp: string
}
