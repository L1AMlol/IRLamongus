const messageInput = document.getElementById("messageInput");
const nameInput = document.getElementById("nameInput");

const sender = Date.now + Math.floor(Math.random() * (106030200));

const ip = location.host.split(':')[0];
const socket = new WebSocket(`ws://${ip}:8765`);

const sendPayload = function (payload) {
    socket.send(JSON.stringify(payload));
}

socket.onopen = () => {
    console.log('Connected to WebSocket server');
    const payload = {
        data: "first from host",
        userType: "player",
        messageType: "auth",
        sender: sender,
    };
    sendPayload(payload);
};

socket.onmessage = (message) => {
    console.log('Received message from server: \n', message.data);
};

socket.onerror = (error) => {
    console.error('WebSocket Error:', error);
};

socket.onclose = e => {
    console.log('WebSocket connection closed');
};


const setName = function() {
    if(!nameInput.value){ return }
    
    const payload = {
        data: nameInput.value,
        userType: "player",
        messageType: "set name",
        sender: sender,
    };
    sendPayload(payload)
};

const sendTestMessage = function() {
    if(!messageInput.value){ return }

    const payload = {
        data: messageInput.value,
        userType: "player",
        messageType: "test message",
        sender: sender,
    };
    sendPayload(payload);
};