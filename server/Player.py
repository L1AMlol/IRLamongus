import websockets

class Player:

    name = ""
    
    def __init__(self, socket:websockets.WebSocketServerProtocol, id:str, is_alive:bool = True, is_ready:bool = False):
        self.socket = socket
        self.id = id
        self.is_ready = is_ready
        self.is_alive = is_alive
    
    def __str__(self) -> str:
        return f"{self.socket} - {self.id}"