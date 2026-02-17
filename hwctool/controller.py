import logging
import keyboard
from PyQt6.QtCore import QObject, QTimer
from hwctool.matchdata import MatchData
from hwctool.settings.config import ConfigManager
from hwctool.tasks.websocket_server import WebSocketServerThread
from hwctool.tasks.http_server import HTTPServerThread

logger = logging.getLogger('root')

class MainController(QObject):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.match_data = MatchData()
        self.view = None
        
        # Start WebSocket Server
        ws_port = self.config_manager.get("websocket_port", 7305)
        self.ws_server = WebSocketServerThread(port=ws_port)
        self.ws_server.start()

        self._last_total_score = 0

        # Start HTTP Server
        http_port = self.config_manager.get("http_port", 8000)
        self.http_server = HTTPServerThread(port=http_port, root_dir="casting_html")
        self.http_server.start()

        # Connect signals
        self.match_data.data_changed.connect(self.on_data_changed)
        self.ws_server.client_connected.connect(self.on_client_connected)
        
        # Setup Hotkeys
        self.setup_hotkeys()

    def on_client_connected(self, client_info):
        self.broadcast_score()

    def set_view(self, view):
        self.view = view
        if self.view:
            self.view.update_from_model(self.match_data)

    def setup_hotkeys(self):
        hotkeys = self.config_manager.get("hotkeys", {})
        try:
            keyboard.add_hotkey(hotkeys.get("show_intro_p1", "F5"), self.show_intro_p1)
            keyboard.add_hotkey(hotkeys.get("show_intro_p2", "F6"), self.show_intro_p2)
            keyboard.add_hotkey(hotkeys.get("toggle_score", "F7"), self.toggle_score)
            keyboard.add_hotkey(hotkeys.get("reset_all", "F8"), self.reset_all)
            logger.info("Hotkeys registrados correctamente.")
        except Exception as e:
            logger.error(f"Error registrando hotkeys: {e}")

    def on_data_changed(self):
        # Check for score increase to trigger Game Over
        current_total = self.match_data.player1_score + self.match_data.player2_score
        if current_total > self._last_total_score:
            self.trigger_game_over()
        self._last_total_score = current_total

        self.broadcast_score()

    # Actions
    def show_intro_p1(self):
        logger.info("Mostrando Intro Jugador 1")
        match, _ = self.match_data.get_current_match()
        data = {
            "type": "show_intro",
            "data": {
                "player": self.match_data.player1_name,
                "team": self.match_data.player1_team,
                "leader": match.get('p1_leader', 'Atriox')
            }
        }
        self.ws_server.broadcast(data)

    def show_intro_p2(self):
        logger.info("Mostrando Intro Jugador 2")
        match, _ = self.match_data.get_current_match()
        data = {
            "type": "show_intro",
            "data": {
                "player": self.match_data.player2_name,
                "team": self.match_data.player2_team,
                "leader": match.get('p2_leader', 'Cutter')
            }
        }
        self.ws_server.broadcast(data)

    def toggle_score(self):
        logger.info("Toggle Score")
        self.broadcast_score()

    def broadcast_score(self):
        data = {
            "type": "update_score",
            "data": self.match_data.to_dict()
        }
        self.ws_server.broadcast(data)

    def trigger_player_card(self, player_data, side='left', slot=1):
        """Sends a 'show_card' event to the overlay with context-aware data."""
        logger.info(f"Triggering Player Card for {player_data.get('name')} ({side}, Slot {slot})")
        
        # Determine relevant rank based on Team Size
        ts = self.match_data.team_size
        rank_key = 'rank_1v1'
        mmr_key = 'mmr_1v1'
        if ts == 2: 
            rank_key = 'rank_2v2'
            mmr_key = 'mmr_2v2'
        elif ts == 3: 
            rank_key = 'rank_3v3'
            mmr_key = 'mmr_3v3'
        
        payload = {
            "type": "show_card",
            "data": {
                "name": player_data.get('name', 'Unknown'),
                "rank": player_data.get(rank_key, "Unranked"),
                "mmr": player_data.get(mmr_key, ""),
                "playstyle": player_data.get('playstyle', '-'),
                "main_leader": player_data.get('main_leader', 'Atriox'),
                "side": side,
                "slot": slot,
                "team_size": ts
            }
        }
        self.ws_server.broadcast(payload)
            
    def trigger_player_cards_batch(self, players_data_list):
        """
        Accepts a list of dicts: {'data': player_data, 'side': 'left'/'right', 'slot': 1..6}
        Uses QTimer for non-blocking stagger instead of time.sleep().
        """
        self._card_queue = list(players_data_list)
        self._send_next_card()

    def _send_next_card(self):
        """Sends the next card from the queue with a 200ms non-blocking delay."""
        if not self._card_queue:
            return
        item = self._card_queue.pop(0)
        self.trigger_player_card(item['data'], item['side'], item['slot'])
        if self._card_queue:
            QTimer.singleShot(200, self._send_next_card)

    def trigger_game_over(self):
        logger.info("Triggering Game Over")
        data = {
            "type": "game_over"
        }
        self.ws_server.broadcast(data)

    def reset_all(self):
        logger.info("Reset All - Resetting scores to 0")
        self.match_data.reset_scores()
        self.match_data.disconnection = False
        self.match_data.mirror_match = False
        self._last_total_score = 0
        if self.view:
            self.view.disconnect_cb.setChecked(False)
            self.view.mirror_cb.setChecked(False)
            self.view.update_from_model(self.match_data)
            self.view.refresh_match_rows()
        self.broadcast_score()
