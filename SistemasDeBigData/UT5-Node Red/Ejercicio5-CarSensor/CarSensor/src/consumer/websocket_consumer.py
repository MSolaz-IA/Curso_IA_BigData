import asyncio
import websockets

import json

class WebSocketConsumer:

    def __init__(self, url, processor):
        self.__url=url
        asyncio.run(self.__consume(processor=processor))

    async def __consume(self, processor):
        async with websockets.connect(self.__url) as websocket:
            while True:
                event = await websocket.recv()
                print(f"Received: {event}")
                processor(json.loads(event))

