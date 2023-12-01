// imports
const express = require("express");
const app = express();
const port = 3000;

// static files
app.use(express.static("public"));
app.use("/css", express.static(__dirname + "public/css"));
app.use("/js", express.static(__dirname + "public/js"));
app.use("/images", express.static(__dirname + "public/images"));

// displays  html files
app.get("", (req, res) => {
  res.sendFile(__dirname + "/views/index.html");
});

app.get("/logged", (req, res) => {
  res.sendFile(__dirname + "/views/logged.html");
});

// listen on port 3000
app.listen(port, () => console.info(`Listening on port ${port}`));
