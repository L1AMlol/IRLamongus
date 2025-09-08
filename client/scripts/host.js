const messageInput = document.getElementById("messageInput");
const readyList = document.getElementById("players-ready");
const notReadyList = document.getElementById("players-not-ready");

const sender = Date.now + Math.floor(Math.random() * (106030200));
let readyPlayers = []

const ip = location.host.split(':')[0];
const socket = new WebSocket(`ws://${ip}:8765`);

const sendPayload = function (payload) {
    socket.send(JSON.stringify(payload));
}

socket.onopen = () => {
    console.log('Connected to WebSocket server');
    const payload = {
        data: "first from host",
        userType: "host",
        messageType: "auth",
        sender: sender,
    };
    sendPayload(payload);
};

socket.onmessage = ({data}) => {
    const message = JSON.parse(data);
    let player
    switch(message.messageType) {
        case "set name":
            player = {
                player_name: message.player_name,
                player_id: message.player_id
            };
            notReadyList.append(player);
            addPlayerDOMList(player, "not ready");
            break;

        case "player is ready":
            console.log(`player ${message.player_name} is ready`);
            player = {
                player_name: message.player_name,
                player_id: message.player_id
            };
            readyList.append(player);
            addPlayerDOMList(player, "ready");
            removePlayerDOMList(player);
            break;
            
        case "player is not ready":
            console.log(`player ${message.player_name} is not ready`);
            player = {
                player_name: message.player_name,
                player_id: message.player_id
            };
            readyList.append(player);
            addPlayerDOMList(player, "not ready");
            removePlayerDOMList(player);
            break;
                
        default:
            console.log('Received message from server: \n', message.data);
            break;
            

    }
};

socket.onerror = (error) => {
    console.error('WebSocket Error:', error);
};

socket.onclose = e => {
    console.log('WebSocket connection closed');
};

const sendTestMessage = function() {
    if(!messageInput.value){ return }

    const message = messageInput.value;
    const payload = {
        data: message,
        userType: "host",
        messageType: "test message",
        sender: sender,
    };
    sendPayload(payload);
};

const addPlayerDOMList = function(player, list) {
    let targetList
    if(list == "ready") {
        targetList = readyList;
    }
    else if(list == "not ready") {
        targetList = notReadyList;
    }
    else {
        console.warn("wrong DOM list given");
    }

    const html = "<li>test</li>";
    // const html = `<li id="id_${player.player_id}">${player.player_name}</li>`;
    console.log(html);
    console.log(targetList.innerHTML);
    targetList.innerHTML += html;
};

const removePlayerDOMList = function(player) {
    const elements = document.querySelectorAll(`#id_${player.player_id}`);
    elements.forEach(el => {
        el.remove();
    });
};
