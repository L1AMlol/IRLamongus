const messageInput = document.getElementById("messageInput");

const sender = Date.now + Math.floor(Math.random() * (106030200));

const socket = new WebSocket("ws://localhost:8765");

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

socket.onmessage = (message) => {
    console.log('Received message from server: \n', message.data);
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
}


