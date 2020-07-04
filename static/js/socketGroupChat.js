
let socket = io();

socket.on('connect', function () {
    socket.emit('opened', {})
});

socket.on('message', function (json_msg) {
    console.log(json_msg);
    let msg = JSON.parse(json_msg);
    if (Number.parseInt('{{ chat.id }}') === msg.chat_id) {
        let li = document.createElement("P");
        li.innerHTML = `${msg.username}: <span class='text-muted'>${msg.text}</span>`;
        li.className = "message";
        document.getElementById('history').appendChild(li);
        let objDiv = document.getElementById("history");
        objDiv.scrollTop = objDiv.scrollHeight;
        socket.emit('notify', {type: 'message', 'message_id': msg.message_id, 'user_id': '{{ current_user.id }}',
                                'chat_id': msg.chat_id})
    } else {
        document.getElementById('messages').innerHTML = "<span style='color: red;'>Messages (!)</span>";
    }
});

document.getElementById('send').onclick = function () {
    let input = document.getElementById('input');
    let msg = input.value;
    input.value = "";
    let li = document.createElement("P");
    li.innerHTML = `<span class='text-muted'>${msg}</span>`;
    li.className = "message";
    li.style = "text-align: right; margin-right: 5%";
    socket.send({text: msg, chat_id: "{{chat.id}}", user_id: "{{ current_user.id }}"});
    document.getElementById('history').appendChild(li);
    let objDiv = document.getElementById("history");
    objDiv.scrollTop = objDiv.scrollHeight;
};

let input = document.getElementById("input");
input.addEventListener("keyup", function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById("send").click();
    }
});