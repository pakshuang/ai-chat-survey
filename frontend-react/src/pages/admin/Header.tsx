import { Avatar, Box, Button, Flex, Tooltip } from "@chakra-ui/react";
import { logout } from "../hooks/useApi";
import { useNavigate } from "react-router-dom";

function Header() {
  const navigate = useNavigate();
  const username = localStorage.getItem("username") || "";

  return (
    <Box w="100%" p="1rem" bg="white" boxShadow="base">
      <Flex justifyContent="flex-end" alignItems="center" gap="1rem">
        <Button
          colorScheme="red"
          variant="outline"
          onClick={() => {
            logout();
            navigate("/admin/login");
          }}
        >
          Logout
        </Button>
        <Tooltip hasArrow label={username}>
          <Avatar name={username} />
        </Tooltip>
      </Flex>
    </Box>
  );
}

export default Header;
