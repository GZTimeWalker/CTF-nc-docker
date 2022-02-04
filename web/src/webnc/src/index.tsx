import {
  ChakraProvider,
  extendTheme,
  withDefaultColorScheme,
} from "@chakra-ui/react";
import { BrowserRouter } from "react-router-dom";
import ReactDOM from "react-dom";
import { App } from "./App";
import "./index.css";

const baseUrl =
  document.getElementsByTagName("base")[0].getAttribute("href") || undefined;
const theme = extendTheme(
  {
    fonts: {
      heading: "JetBrains Mono, Consolas, Microsoft YaHei UI, monospace",
      body: "JetBrains Mono, Consolas, Microsoft YaHei UI, monospace",
    },
    config: {
      initialColorMode: "dark",
    },
    colors: {
      gray: {
        100: "#ebebeb",
        200: "#cfcfcf",
        300: "#b3b3b3",
        400: "#969696",
        500: "#7a7a7a",
        600: "#5e5e5e",
        700: "#414141",
        800: "#252525",
        900: "#202020",
      },
    },
    styles: {
      global: {
        body: {
          bg: "#212121",
        },
      },
    },
  },
  withDefaultColorScheme({ colorScheme: "gray" })
);

ReactDOM.render(
  <ChakraProvider theme={theme}>
    <BrowserRouter basename={baseUrl}>
      <App />
    </BrowserRouter>
  </ChakraProvider>,
  document.getElementById("root")
);
