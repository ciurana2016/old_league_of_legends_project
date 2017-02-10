var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);


io.on('connection', function(socket){

	// Adds summoners to theyr room
	socket.on('ADD_summoner', function(room){
		socket.room = room;
		socket.join(room);
		// console.log('ADD_summoner to room: ',room);
	});

	// Match has started
	// ( someone clicked on match start, and the riotAPI confirmed )
	socket.on('IO_MATCH_start', function(){
		socket.broadcast.to(socket.room).emit('RECEIVE_match_start');
	});

	// Someone SENDS spell ( clicked on spell )
	socket.on('SEND_spell', function(data){
		// console.log('SEND_spell data= ', data);
		// console.log('Sending spell to room:', socket.room);
		socket.broadcast.to(socket.room).emit('RECEIVE_spell', data);
	});

	// Guy who created the room is closing it
	socket.on('CLOSE_room', function(){
		socket.broadcast.to(socket.room).emit('RECEIVE_close_room');
		socket.leave(socket.room);
	});

	// Remove me form room 
	// ( when noone is in room it automatically deletes itself,  or so I'v read )
	socket.on('REMOVE_me', function(){
		socket.leave(socket.room);
	});

});


// Test !
app.get('/', function(req, res){
	res.sendFile(__dirname + '/index.html');
});

http.listen(3000, function(){
	console.log('listening on *:3000');
});