import asyncio
import websockets
import json
import logging
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger('root')

class WebSocketServerThread(QThread):
    client_connected = pyqtSignal(str)
    client_disconnected = pyqtSignal(str)

    def __init__(self, port=7305, parent=None):
        super().__init__(parent)
        self.port = port
        self.connected_clients = set()
        self.loop = None
        self.server = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            self.loop.run_until_complete(self.serve_forever())
        except Exception as e:
            logger.error(f"Error en servidor WebSocket: {e}")
        finally:
            self.loop.close()

    async def serve_forever(self):
        logger.info(f"Iniciando Servidor WebSocket en puerto {self.port}")
        async with websockets.serve(self.handler, "localhost", self.port):
            await asyncio.Future()  # run forever

    async def handler(self, websocket):
        self.connected_clients.add(websocket)
        path = getattr(websocket, 'path', 'unknown')
        logger.debug(f"Cliente conectado: {path}")
        self.client_connected.emit(f"Cliente conectado: {path}")
        
        try:
            async for message in websocket:
                pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected_clients.discard(websocket)
            logger.debug("Cliente desconectado")
            self.client_disconnected.emit("Cliente desconectado")

    def stop(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.wait()

    def broadcast(self, message_dict):
        """Send a JSON message to all connected clients."""
        if self.loop and self.connected_clients:
            message_str = json.dumps(message_dict)
            coro = self._broadcast_async(message_str)
            try:
                asyncio.run_coroutine_threadsafe(coro, self.loop)
            except RuntimeError:
                logger.warning("WebSocket loop closed, cannot broadcast")
    
    async def _broadcast_async(self, message):
        # Copy the set to avoid modification during iteration
        clients = self.connected_clients.copy()
        if clients:
            await asyncio.gather(
                *[client.send(message) for client in clients],
                return_exceptions=True
            )
