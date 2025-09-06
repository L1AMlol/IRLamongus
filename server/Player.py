class Player:

    def __init__(self, socket, id, is_alive = True, is_ready = False):
        self.socket = socket
        self.id = id
        self.is_ready = is_ready
        self.is_alive = is_alive
    
    def __str__(self) -> str:
        return f"{self.socket} - {self.id}"