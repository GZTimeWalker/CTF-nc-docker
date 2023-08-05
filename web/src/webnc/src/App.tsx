import { FC } from "react";
import { Box } from "@chakra-ui/react";
import { Portal } from "./Portal";
import { XTerm } from "./XTerm";
import { Routes, Route } from "react-router-dom";

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
