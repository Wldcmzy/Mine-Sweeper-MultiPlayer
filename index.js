var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/test1.html');
});

io.on("connection", (socket) => {
  console.log("用户已连接");
  socket.on("disconnection", () => {
    console.log("用户未连接");
  })
  socket.emit("dev", 'hello clint');
  socket.on("str", (x) => {
    console.log(x);
  })
})

const port = process.env.PORT || 7200;
http.listen(port, () => { console.log('正在*：7200'); });




















/*
const { createServer } = require("http");
const { Server } = require("socket.io");

const httpServer = createServer();
const io = new Server(httpServer, { });

io.on("connection", (socket) => {

  socket.on("connect", () => {
    console.log("user connect"); // undefined
  });
  
  socket.on("disconnect", () => {
    console.log("user disconnect"); // undefined
  });
});
const port = process.env.port || 7200;
httpServer.listen(port , () =>console.log(`server running ${port}`));
*/
