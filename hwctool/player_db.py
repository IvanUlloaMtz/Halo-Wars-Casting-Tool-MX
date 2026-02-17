import json
import os
import sys
import logging

class PlayerDB:
    def __init__(self):
        self.players = {}
        self.filename = self._get_db_path()
        self.load()

    def _get_db_path(self):
        """Returns the path to players.json relative to the executable or script."""
        if getattr(sys, 'frozen', False):
            # Running as compiled .exe
            base_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # If in hwctool package, go up one level? 
            # script is in hwctool/player_db.py. Application root is up one level.
            base_dir = os.path.dirname(base_dir) 
        
        return os.path.join(base_dir, "players.json")

    def load(self):
        """Loads players from JSON. Creates default if missing."""
        if not os.path.exists(self.filename):
            logging.info(f"Player DB not found. Creating default at {self.filename}")
            self._create_default()
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.players = data.get('players', {})
            logging.info(f"Loaded {len(self.players)} players from DB.")
        except Exception as e:
            logging.error(f"Error loading player DB: {e}")
            self.players = {}

    def save(self):
        """Saves current players to JSON."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({'players': self.players}, f, indent=4, ensure_ascii=False)
            logging.info("Player DB saved.")
        except Exception as e:
            logging.error(f"Error saving player DB: {e}")

    def _create_default(self):
        """Creates a default DB with example data."""
        self.players = {
            "Dark1": {
                "name": "Dark1",
                "rank_1v1": "Onyx 1500",
                "mmr_1v1": "1500",
                "rank_2v2": "Champion 10",
                "mmr_2v2": "1950",
                "rank_3v3": "Diamond 6",
                "mmr_3v3": "1200",
                "playstyle": "Aggressive / Rush",
                "main_leader": "Atriox"
            },
            "Nakamura": {
                "name": "Nakamura",
                "rank_1v1": "Champion 1",
                "mmr_1v1": "2200",
                "rank_2v2": "Champion 1",
                "mmr_2v2": "2100",
                "rank_3v3": "Champion 1",
                "mmr_3v3": "2150",
                "playstyle": "Strategic / Macro",
                "main_leader": "Captain Cutter"
            }
        }
        self.save()

    def get_player(self, name):
        """Case-insensitive retrieval."""
        for p_name, p_data in self.players.items():
            if p_name.lower() == name.lower():
                return p_data
        return None

    def add_update_player(self, name, data):
        """
        Adds or updates a player.
        data dict should contain keys: rank_1v1, rank_2v2, etc.
        """
        # Preserve existing keys if updating partial?
        # For now, we assume full update or overwrite
        # But we want to preserve case of Name if new.
        
        # Check if exists (case insensitive) to overwrite key
        existing_key = None
        for k in self.players:
            if k.lower() == name.lower():
                existing_key = k
                break
        
        target_key = existing_key if existing_key else name
        
        # Merge if existing?
        if existing_key:
            self.players[target_key].update(data)
        else:
            self.players[target_key] = data
            self.players[target_key]['name'] = name # Ensure name field is set
            
        self.save()

    def delete_player(self, name):
        """Deletes a player by name (case-insensitive)."""
        key_to_del = None
        for k in self.players:
            if k.lower() == name.lower():
                key_to_del = k
                break
        
        if key_to_del:
            del self.players[key_to_del]
            self.save()
            return True
        return False

    def get_all_names(self):
        """Returns sorted list of player names."""
        return sorted(list(self.players.keys()), key=str.lower)
