import { VStack } from "@chakra-ui/react"
import AdminSurveyOption from "./AdminSurveyOption"

function AdminSurveyOptions() {
  return (
    <VStack w="100%" alignItems="flex-start">
      <AdminSurveyOption />
      <AdminSurveyOption />
      <AdminSurveyOption />
    </VStack>
  )
}

export default AdminSurveyOptions
