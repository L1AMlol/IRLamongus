import asyncio
import websockets
import json
from Player import Player
from Host import Host

host_clients = set()
player_clients = set()

async def handle_client(ws):
    
    try:
        first_msg_str = await ws.recv()
        first_msg = json.loads(first_msg_str)
        if first_msg['userType'] == "host":
            if ws not in host_clients:
                host_clients.add(ws)
                # ToDo: add class host
                is_host = True
                is_player = False
                print("a host has connected")
            
        elif first_msg['userType'] == "player":
            if ws not in player_clients:
                player_clients.add(ws)
                # ToDo: add class player
                is_host = False
                is_player = True
                print("a player has connected")
        while True:
            payload_str = await ws.recv()
            payload = json.loads(payload_str)
            if is_host:
                print(f"host sent: {payload['message']}")
            elif is_player:
                print(f"player sent: {payload['message']}")


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
    
