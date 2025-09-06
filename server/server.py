import asyncio
import websockets

connected_clients = set()

async def handle_client(ws):
    connected_clients.add(ws)
    print(f"New client connected: {ws.remote_address}")
    try:
        while True:
            payload = await ws.recv()
            print(payload)

    except websockets.exceptions.ConnectionClosed:
        print(f"Client {ws.remote_address} disconnected")

    finally:
        connected_clients.remove(ws)

async def broadcast_ping():
    while True:
        if connected_clients:
            for ws in connected_clients:
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
