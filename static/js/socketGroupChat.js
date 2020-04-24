var socket = io();

socket.on('connect', function () {
    socket.emit('opened', {})
});

socket.on('message', function (json_msg) {
    console.log(json_msg);
    var msg = JSON.parse(json_msg);
    if (Number.parseInt('{{ chat.id }}') === msg.chat_id) {
        var li = document.createElement("P");
        li.innerHTML = `${msg.username}: <span class='text-muted'>${msg.text}</span>`;
        li.className = "message";
        document.getElementById('history').appendChild(li);
        var objDiv = document.getElementById("history");
        objDiv.scrollTop = objDiv.scrollHeight;
        socket.emit('notify', {type: 'message', 'message_id': msg.message_id, 'user_id': '{{ current_user.id }}',
                                'chat_id': msg.chat_id})
    } else {
        document.getElementById('messages').innerHTML = "<span style='color: red;'>Messages (!)</span>";
    }
});

document.getElementById('send').onclick = function () {
    var input = document.getElementById('input');
    var msg = input.value;
    input.value = "";
    var li = document.createElement("P");
    li.innerHTML = `<span class='text-muted'>${msg}</span>`;
    li.className = "message";
    li.style = "text-align: right; margin-right: 5%";
    socket.send({text: msg, chat_id: "{{chat.id}}", user_id: "{{ current_user.id }}"});
    document.getElementById('history').appendChild(li);
    var objDiv = document.getElementById("history");
    objDiv.scrollTop = objDiv.scrollHeight;
};

var input = document.getElementById("input");
input.addEventListener("keyup", function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById("send").click();
    }
});