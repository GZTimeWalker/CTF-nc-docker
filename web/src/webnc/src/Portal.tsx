import React, { FC, useState } from "react";
import {
  VStack,
  Input,
  Button,
  FormLabel,
  FormControl,
  Heading,
  Center,
  Box,
} from "@chakra-ui/react";

export const Portal: FC = () => {
  // const [hostname, setHostname] = useState("localhost");
  const [port, setPort] = useState("");

  const onConnect = () => {
    if (port) {
      window.location.href = port;
    } else {
      window.location.href = `65100`;
    }
  };

  return (
    <Center minH="100vh">
      <Box boxShadow="2xl" bg="gray.800" rounded="lg" px="48px" py="24px">
        <VStack spacing={4}>
          <Heading size="lg">CTF-web-nc</Heading>
          <FormControl id="hostname" my="12px">
            <FormLabel>Hostname</FormLabel>
            <Input
              value="localhost"
              readOnly
              // value={hostname}
              // onChange={(e) => {
              //   setHostname(e.target.value);
              // }}
              placeholder="localhost"
            />
          </FormControl>
          <FormControl id="port" my="12px">
            <FormLabel>Port</FormLabel>
            <Input
              value={port}
              onChange={(e) => {
                setPort(e.target.value);
              }}
              onKeyUp={(e) => {
                if (e.key === "Enter") {
                  onConnect();
                }
              }}
              placeholder="65100"
            />
          </FormControl>
          <Button onClick={onConnect}>Connect</Button>
        </VStack>
      </Box>
    </Center>
  );
};
