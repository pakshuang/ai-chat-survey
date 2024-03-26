import React, { useState } from 'react';
import {
  Box,
  Flex,
  FormControl,
  FormLabel,
  Input,
  Button,
} from '@chakra-ui/react';
interface personalData {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  address: string;
}

interface Props {
  personalData: personalData;
  setpersonalData: (data: personalData)=>void;
  handleSubmit: (e) => void;

}
const PersonalInfo = ({personalData,setpersonalData,handleSubmit}:Props) => {

  const handleChange = (e) => {
    const { name, value } = e.target;
    setpersonalData({
      ...personalData,
      [name]: value,
    });
  };

  return (
    <Box maxW="md" mx="auto" mt={10} p={5} borderWidth="1px" borderRadius="lg">
      <form onSubmit={handleSubmit}>
        <FormControl id="firstName" isRequired>
          <FormLabel>First Name</FormLabel>
          <Input
            type="text"
            name="firstName"
            value={personalData.firstName}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl id="lastName" isRequired mt={4}>
          <FormLabel>Last Name</FormLabel>
          <Input
            type="text"
            name="lastName"
            value={personalData.lastName}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl id="email" isRequired mt={4}>
          <FormLabel>Email</FormLabel>
          <Input
            type="email"
            name="email"
            value={personalData.email}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl id="phone" isRequired mt={4}>
          <FormLabel>Phone</FormLabel>
          <Input
            type="tel"
            name="phone"
            value={personalData.phone}
            onChange={handleChange}
          />
        </FormControl>
        <FormControl id="address" isRequired mt={4}>
          <FormLabel>Address</FormLabel>
          <Input
            type="text"
            name="address"
            value={personalData.address}
            onChange={handleChange}
          />
        </FormControl>
        <Flex justifyContent='flex-end'>
        <Button
          type="submit"
          disabled={true}
          colorScheme="blue"
          mt={5}
        >
         Next
        </Button>
        </Flex>
      </form>
    </Box>
  );
};

export default PersonalInfo;
