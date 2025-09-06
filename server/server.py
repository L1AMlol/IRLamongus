import asyncio
import websockets
import json

hosts = set()
players = set()

async def handle_client(ws):
    
    try:
        first_msg_str = await ws.recv()
        first_msg = json.loads(first_msg_str)
        if first_msg['userType'] == "host":
            if ws not in hosts:
                hosts.add(ws)
                # ToDo: add class host
                is_host = True
                is_player = False
                print("a host has connected")
            
        elif first_msg['userType'] == "player":
            if ws not in players:
                players.add(ws)
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
        if ws in hosts:
            print("a host has disconnected")
        elif ws in players:
            print("a player has disconnected")

    finally:
        if ws in hosts:
            hosts.remove(ws)
        elif ws in players:
            players.remove(ws)
        

async def broadcast_ping():
    while True:
        if hosts:
            for ws in hosts:
                await ws.ping()
        if players:
            for ws in players:
                await ws.ping()
        await asyncio.sleep(5)

async def start_server():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        asyncio.create_task(broadcast_ping())
        await asyncio.Future()

try:
    asyncio.run(start_server())
    
except KeyboardInterrupt:
    print("server closed")
