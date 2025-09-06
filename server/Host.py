import websockets

class Host:
    def __init__(self, socket: websockets.WebSocketServerProtocol, id: str):
        self.socket = socket
        self.id = id
    
    def __str__(self) -> str:
        return f"{self.socket} - {self.id}"