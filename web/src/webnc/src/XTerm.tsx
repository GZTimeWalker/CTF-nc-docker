import React, { FC, useRef, useEffect } from "react";
import { Center } from "@chakra-ui/react";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { WebglAddon } from "xterm-addon-webgl";
import { useParams } from "react-router-dom";
import { AttachAddon } from "xterm-addon-attach";
import "xterm/css/xterm.css";

export const XTerm: FC = () => {
  const params = useParams();
  const port = params.port ?? "65198";
  const url = document.location.origin.replace(/^http/, "ws") + "/shell";

  const xterm = useRef<Terminal>(
    new Terminal({
      cursorBlink: true,
      fontFamily: "JetBrains Mono, Consolas, Microsoft YaHei UI, monospace",
      fontSize: 16,
      cursorStyle: "underline",
      cursorWidth: 5,
      theme: {
        background: "#252525",
      },
    })
  );

  const socket = useRef<WebSocket>(
    new WebSocket(`${url}/${port}`)
  );
  const fitAddon = useRef<FitAddon>(new FitAddon());
  const termdiv = useRef<HTMLDivElement>(null);

  socket.current.onclose = _ => {
    xterm.current.writeln("\nConnection closed.");
  }

  useEffect(() => {
    xterm.current.loadAddon(fitAddon.current);
    xterm.current.open(termdiv.current!!);
    try {
      xterm.current.loadAddon(new WebglAddon());
    } catch {
      console.log("WebGL load failed.");
    }
    xterm.current.loadAddon(new AttachAddon(socket.current));
    fitAddon.current.fit();
    xterm.current.focus();
  }, []);

  return (
    <Center minH="100vh">
      <Center boxShadow="2xl" m="0 50px">
        <Center rounded="lg" bg="gray.800" p="20px">
          <div ref={termdiv} />
        </Center>
      </Center>
    </Center>
  );
};
