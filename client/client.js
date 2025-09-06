const testBtn = document.getElementById("testBtn");

const rand = Math.floor(Math.random() * (1000 - 0 + 1)) + 0;

const socket = new WebSocket("ws://localhost:8765");

socket.onopen = () => {
    console.log('Connected to WebSocket server');
};

// When the server sends a message back
socket.onmessage = (message) => {
    console.log('Received message from server: \n', message.data);

    if (message.data === 'ping') {
        console.log('Received ping, sending pong');
        socket.send('pong');
    }
};

// If there is an error in the WebSocket connection
socket.onerror = (error) => {
    console.error('WebSocket Error:', error);
};

// When the connection is closed
socket.onclose = e => {
    console.log('WebSocket connection closed');
};

testBtn.addEventListener('click', () => {
    const payload = {
        message: "test",
        sender: rand,
    }
    socket.send(JSON.stringify(payload));
});