import asyncio
import websockets
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
            print(f"name set for player: {player.name}")

        case "test message":
            print(f"{player.name} -> {data}")
    



async def handle_host(host:Host):
    pass

async def handle_client(ws):
    
    try:
        first_msg = await wait_on_message(ws)
        if first_msg['userType'] == "host":
            if ws not in host_clients:
                host_clients.add(ws)
                host = Host(ws, first_msg['sender'])
                is_host = True
                is_player = False
                print("a host has connected")
            
        elif first_msg['userType'] == "player":
            if ws not in player_clients:
                player_clients.add(ws)
                player = Player(ws, first_msg['sender'])
                is_host = False
                is_player = True
                print("a player has connected")
        while True:
            if is_host:
                await handle_host(host)
            elif is_player:
                await handle_player(player)


    except websockets.exceptions.ConnectionClosed:
        if ws in host_clients:
            print("a host has disconnected")
        elif ws in player_clients:
            print("a player has disconnected")

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

async def start_server():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        asyncio.create_task(broadcast_ping())
        await asyncio.Future()


asyncio.run(start_server())
    
