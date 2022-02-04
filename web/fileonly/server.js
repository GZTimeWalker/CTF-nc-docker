const express = require("express");
const app = express();

const args = process.argv.slice(2)

app.use(express.static("static"));
app.listen(parseInt(args[0]), () => { console.log("Listening on port " + args[0]) });
