
var socket = io();

socket.on('connect', function () {
    socket.emit('opened', {})
});

socket.on('message', function (msg) {
    document.getElementById('messages').innerHTML = "<span style='color: red;'>Messages (!)</span>";
    // socket.emit('notify', {type: 'message', 'message_id': msg.message_id, user: '{{ current_user.id }}'});
});