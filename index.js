var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
//在使用nodejs里面使用require采用commonjs模块
//在es6里面的js使用impore 通过export或者export default
app.get('/',(req,res)=>{
  res.sendFile(__dirname + '/index.html');
});

io.on("connection",(socket)=> { 
  console.log("用户已连接");
  socket.on("disconnection",()=>{
  console.log("用户未连接");
})
})
const port = process.env.PORT || 7200 ;
http.listen( port,()=> { console .log('正在*：7200'); });




















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
