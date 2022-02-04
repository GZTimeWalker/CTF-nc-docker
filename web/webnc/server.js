const express = require("express");
const app = express();
const _ = require("express-ws")(app);
const pty = require("node-pty");
const { resolve } = require('path')

app.use(express.static("static"));

const args = process.argv.slice(2);

let allow_ports_str = (args[1] ?? "65100-65100").split("-");
let allow_ports = [];

allow_ports_str.forEach((i) => allow_ports.push(parseInt(i)));

if (allow_ports.length != 2) allow_ports = [65100, 65100];

app.ws("/shell/:port", (ws, req) => {
  if (!req.params.port) ws.close(1008, "Port not allowed.");

  let port = parseInt(req.params.port);

  if (port < allow_ports[0] || port > allow_ports[1])
    return ws.close(1008, "Port not allowed.");

  console.log(`[+] New connection received. [${port}]`);

  var shell = pty.spawn("/bin/nc", ["localhost", req.params.port]);

  shell.on("data", (data) => {
    ws.send(data);
  });

  ws.on("message", (msg) => {
    shell.write(msg);
  });

  shell.on("close", () => {
    ws.close();
  });

  ws.on("close", () => {
    shell.kill();
    console.log(`[+] Connection closed. [${port}]`);
  });
});

app.get("/wnc/*", (req, res) => {
  res.sendFile(resolve("./static/wnc/index.html"));
});

app.listen(parseInt(args[0]), () => {
  console.log("[+] Listening on port " + args[0]);
});
