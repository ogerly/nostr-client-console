import websockets
import asyncio
import json
from .logger import setup_logger

logger = setup_logger(__name__)

class RelayManager:
    def __init__(self, config):
        self.relays = config.get_config()['relays']
        self.connections = {}

    async def connect_all(self):
        for relay in self.relays:
            try:
                self.connections[relay] = await websockets.connect(relay)
                logger.info(f"Verbunden mit Relay: {relay}")
            except Exception as e:
                logger.error(f"Verbindungsfehler zu {relay}: {str(e)}")

    async def send_event(self, event):
        for relay, conn in self.connections.items():
            try:
                await conn.send(json.dumps(event))
                logger.debug(f"Event an {relay} gesendet")
            except Exception as e:
                logger.error(f"Sende-Fehler an {relay}: {str(e)}")