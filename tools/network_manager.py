from PyQt6.QtCore import QObject, pyqtSignal
import asyncio

class NetworkManager(QObject):
    peer_connected = pyqtSignal(str)          
    peer_disconnected = pyqtSignal(str)
    remote_state_changed = pyqtSignal(dict)   
    error_occurred = pyqtSignal(str)

    def __init__(self, local_peer_id, room_id, parent=None):
        super().__init__(parent)
        self._local_id = local_peer_id
        self._room_id = room_id
        self._running = False

    async def start(self):
        self._running = True

    async def stop(self):
        self._running = False