import asyncio
import websockets
import socket
import json
from Player import Player
from Host import Host

host_clients = set()
player_clients = set()
hosts = set()
clients = set()

async def wait_on_message(ws:websockets.WebSocketServerProtocol):
    message_str = await ws.recv()
    message = json.loads(message_str)
    return message

async def handle_player(player:Player):
    payload = await wait_on_message(player.socket)
    data = payload['data']
    
    match payload['messageType']:
        case "set name":
            player.name = str(data)
            print(f"[set name] --> {player.name}")

        case "test message":
            if player.name:
                print(f"[test message] --> {player.name} -> {data}")
            else:
                print(f"[test message] --> player? -> {data}")
    



async def handle_host(host:Host):
    payload = await wait_on_message(host.socket)
    data = payload['data']

    match payload['messageType']:
        case "test message":
            print(f"[test message] --> host -> {data}")

async def handle_client(ws):
    
    try:
        first_msg = await wait_on_message(ws)
        if first_msg['userType'] == "host":
            if ws not in host_clients:
                host_clients.add(ws)
                host = Host(ws, first_msg['sender'])
                is_host = True
                is_player = False
                print("[connection] --> a host has connected")
            
        elif first_msg['userType'] == "player":
            if ws not in player_clients:
                player_clients.add(ws)
                player = Player(ws, first_msg['sender'])
                is_host = False
                is_player = True
                print("[connection] --> a player has connected")
        while True:
            if is_host:
                await handle_host(host)
            elif is_player:
                await handle_player(player)


    except websockets.exceptions.ConnectionClosed:
        if ws in host_clients:
            print("[connection] --> a host has disconnected")
        elif ws in player_clients:
            print("[connection] --> a player has disconnected")

    finally:
        if ws in host_clients:
            host_clients.remove(ws)
        elif ws in player_clients:
            player_clients.remove(ws)
        

async def broadcast_ping():
    while True:
        if host_clients:
            for ws in host_clients:
                await ws.ping()
        if player_clients:
            for ws in player_clients:
                await ws.ping()
        await asyncio.sleep(5)

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"  # Fallback to localhost

async def start_server():
    ip = get_local_ip()
    async with websockets.serve(handle_client, "localhost", 8765):
        print(f"Server started at {ip}:8765")
        asyncio.create_task(broadcast_ping())
        await asyncio.Future()


asyncio.run(start_server())
    
