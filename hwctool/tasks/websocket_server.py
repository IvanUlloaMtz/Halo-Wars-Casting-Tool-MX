import asyncio
import websockets
import json
import logging
from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger('root')

# Silence websockets internal debug logging (causes UnicodeEncodeError on Windows cp1252)
logging.getLogger('websockets').setLevel(logging.WARNING)

class WebSocketServerThread(QThread):
    client_connected = pyqtSignal(str)
    client_disconnected = pyqtSignal(str)

    def __init__(self, port=7305, parent=None):
        super().__init__(parent)
        self.port = port
        self.connected_clients = set()
        self.loop = None
        self.server = None
        self._broadcast_total = 0
        self._broadcast_errors = 0

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            self.loop.run_until_complete(self.serve_forever())
        except Exception as e:
            logger.error(f"Error en servidor WebSocket: {e}")
        finally:
            self.loop.close()
            logger.info("WebSocket loop cerrado.")

    async def serve_forever(self):
        logger.info(f"Iniciando Servidor WebSocket en puerto {self.port}")
        self.server = await websockets.serve(self.handler, "localhost", self.port)
        await asyncio.Future()  # run forever until stopped

    async def handler(self, websocket):
        self.connected_clients.add(websocket)
        path = getattr(websocket, 'path', 'unknown') or 'unknown'
        client_count = len(self.connected_clients)
        logger.info(f"[WS] Cliente conectado: {path} (total: {client_count})")
        self.client_connected.emit(path)
        
        try:
            async for message in websocket:
                pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected_clients.discard(websocket)
            client_count = len(self.connected_clients)
            logger.info(f"[WS] Cliente desconectado: {path} (total: {client_count})")
            self.client_disconnected.emit(path)

    def stop(self):
        """Gracefully shut down the WebSocket server."""
        if self.loop and self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self._shutdown(), self.loop)
            try:
                future.result(timeout=3)
            except Exception as e:
                logger.warning(f"[WS] Error durante apagado: {e}")
            # Stop the loop AFTER the shutdown coroutine completes
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.wait(3000)
        logger.info(f"[WS] Servidor detenido. Broadcasts totales: {self._broadcast_total}, errores: {self._broadcast_errors}")

    async def _shutdown(self):
        """Close server and disconnect clients. Does NOT stop the loop."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        # Close active client connections
        for ws in list(self.connected_clients):
            try:
                await ws.close()
            except Exception:
                pass
        self.connected_clients.clear()

    def broadcast(self, message_dict):
        """Send a JSON message to all connected clients."""
        if self.loop and self.connected_clients:
            message_str = json.dumps(message_dict)
            coro = self._broadcast_async(message_str)
            try:
                asyncio.run_coroutine_threadsafe(coro, self.loop)
            except RuntimeError:
                logger.warning("[WS] Loop cerrado, no se puede broadcast")
    
    async def _broadcast_async(self, message):
        clients = self.connected_clients.copy()
        if not clients:
            return
        self._broadcast_total += 1
        results = await asyncio.gather(
            *[client.send(message) for client in clients],
            return_exceptions=True
        )
        # Clean up dead clients
        for client, result in zip(clients, results):
            if isinstance(result, Exception):
                self._broadcast_errors += 1
                self.connected_clients.discard(client)
                logger.warning(f"[WS] Cliente muerto removido tras error de broadcast")

