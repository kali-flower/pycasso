import asyncio
import websockets
from collections import deque

CONNECTIONS = {}
next_id = 0

async def handle_client(websocket):
    global next_id, CONNECTIONS 

    # As I understand, accessing client_id like this is safe.
    client_id = next_id
    next_id += 1

    CONNECTIONS[client_id] = websocket
    # await websocket.send(f"You are client {client_id}")
    try:
        async for message in websocket:
            others = [ws for cid,ws in CONNECTIONS.items() if cid != client_id]
            websockets.broadcast(others, message)
    except:
        print("Client closed the connection ungracefully")
    else:
        print("Client closed the connection gracefully")
    
    # remove this websocket from connections
    del CONNECTIONS[client_id]

async def main():
    async with websockets.serve(handle_client, port=8000):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())