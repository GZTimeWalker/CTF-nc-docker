import React, { FC } from "react";
import { Box } from "@chakra-ui/react";
import { Route, Routes } from "react-router";
import { Portal } from "./Portal";
import { XTerm } from "./XTerm";

export const App: FC = () => {
  return (
    <Box minH="100vh" width="100vw">
      <Routes>
        <Route path="/">
          <Route index element={<Portal />} />
          <Route path=":port" element={<XTerm />} />
        </Route>
      </Routes>
    </Box>
  );
};
