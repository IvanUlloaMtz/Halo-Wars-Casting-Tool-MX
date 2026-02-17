from PyQt6.QtCore import QObject, pyqtSignal

# Shared leader list — used by matchdata, mainwindow, and players tab
LEADERS = [
    "Atriox", "Decimus", "Voridus", "Pavium", "Colony",
    "YapYap The Destroyer", "The Arbiter", "Shipmaster",
    "Captain Cutter", "Isabel", "Professor Anders", "Sergeant Forge",
    "Serina", "Kinsano", "Sergeant Johnson", "Commander Jerome"
]

class MatchData(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._player1_name = "Jugador 1"
        self._player1_team = "Equipo A"
        self._player1_leader = "Atriox"
        self._player1_score = 0
        self._player1_color = "#CC2222"
        self._player1_country = "mx"

        self._player2_name = "Jugador 2"
        self._player2_team = "Equipo B"
        self._player2_leader = "Cutter"
        self._player2_score = 0
        self._player2_color = "#1155FF"
        self._player2_country = "mx"
        
        self._best_of = 3
        self._game_type = "Deathmatch"
        self._team_size = 1 # 1=1v1, 2=2v2, 3=3v3
        self._current_map = "Ashes"
        self._map_popup_enabled = False
        self._map_enter_sec = 3
        self._map_visible_sec = 25
        self._map_exit_sec = 3
        self._map_hidden_sec = 20
        self._show_team_names = False
        self._disconnection = False
        self._mirror_match = False
        
        # Extra Players (Team 1: P3, P5)
        self._player3_name = "Jugador 3"
        self._player3_leader = "Anders"
        self._player3_color = "#FF6600"
        self._player3_country = "mx"
        self._player5_name = "Jugador 5"
        self._player5_leader = "Forge"
        self._player5_color = "#FFCC00"
        self._player5_country = "mx"
        
        # Extra Players (Team 2: P4, P6)
        self._player4_name = "Jugador 4"
        self._player4_leader = "Decimus"
        self._player4_color = "#00CCFF"
        self._player4_country = "mx"
        self._player6_name = "Jugador 6"
        self._player6_leader = "Pavium"
        self._player6_color = "#22CC44"
        self._player6_country = "mx"
        
        # Initialize matches structure
        self.init_matches()

    def to_dict(self):
        current_match, match_num = self.get_current_match()
        return {
            "p1": { "name": self._player1_name, "leader": self._player1_leader, "score": self._player1_score, "color": self._player1_color, "country": self._player1_country },
            "p2": { "name": self._player2_name, "leader": self._player2_leader, "score": self._player2_score, "color": self._player2_color, "country": self._player2_country },
            "p3": { "name": self._player3_name, "leader": self._player3_leader, "color": self._player3_color, "country": self._player3_country },
            "p4": { "name": self._player4_name, "leader": self._player4_leader, "color": self._player4_color, "country": self._player4_country },
            "p5": { "name": self._player5_name, "leader": self._player5_leader, "color": self._player5_color, "country": self._player5_country },
            "p6": { "name": self._player6_name, "leader": self._player6_leader, "color": self._player6_color, "country": self._player6_country },
            "best_of": self._best_of,
            "game_type": self._game_type,
            "team_size": self._team_size,
            "current_map": self._current_map,
            "map_popup": {
                "enabled": self._map_popup_enabled,
                "enter_sec": self._map_enter_sec,
                "visible_sec": self._map_visible_sec,
                "exit_sec": self._map_exit_sec,
                "hidden_sec": self._map_hidden_sec,
            },
            "current_match": {
                "number": match_num,
                "p1_leader": current_match.get('p1_leader', 'Atriox'),
                "p2_leader": current_match.get('p2_leader', 'Captain Cutter'),
                "p3_leader": current_match.get('p3_leader', 'Professor Anders'),
                "p4_leader": current_match.get('p4_leader', 'Decimus'),
                "p5_leader": current_match.get('p5_leader', 'Sergeant Forge'),
                "p6_leader": current_match.get('p6_leader', 'Pavium'),
            },
            "matches": self.matches,
            "show_team_names": self._show_team_names,
            "team1_name": self._player1_team,
            "team2_name": self._player2_team,
            "disconnection": self._disconnection,
            "mirror_match": self._mirror_match,
        }

    # Getters and Setters for Core Properties
    @property
    def team_size(self): return self._team_size
    @team_size.setter
    def team_size(self, value):
        self._team_size = int(value)
        self.init_matches()
        self.data_changed.emit()

    def get_slots_for_team(self, team_idx):
        """
        Returns a list of player slots (int) for the given team based on current team_size.
        team_idx: 1 (Left/Red) or 2 (Right/Blue)
        """
        slots = []
        ts = self._team_size
        if team_idx == 1: # Left: 1, 3, 5
            slots = [1]
            if ts >= 2: slots.append(3)
            if ts >= 3: slots.append(5)
        else: # Right: 2, 4, 6
            slots = [2]
            if ts >= 2: slots.append(4)
            if ts >= 3: slots.append(6)
        return slots

    @property
    def show_team_names(self): return self._show_team_names
    @show_team_names.setter
    def show_team_names(self, value):
        self._show_team_names = value
        self.data_changed.emit()

    @property
    def disconnection(self): return self._disconnection
    @disconnection.setter
    def disconnection(self, value):
        self._disconnection = value
        self.data_changed.emit()

    @property
    def mirror_match(self): return self._mirror_match
    @mirror_match.setter
    def mirror_match(self, value):
        self._mirror_match = value
        self.data_changed.emit()

    # ... Existing P1/P2 Getters/Setters ...
    # (P1 and P2 methods are below, assumed unchanged unless I overwrite them)
    
    # Extra Player Properties (Simplified for brevity in edit, typically would be full getters/setters)
    @property
    def player3_name(self): return self._player3_name
    @player3_name.setter
    def player3_name(self, v): self._player3_name = v; self.data_changed.emit()
    
    @property
    def player3_leader(self): return self._player3_leader
    @player3_leader.setter
    def player3_leader(self, v): self._player3_leader = v; self.data_changed.emit()

    @property
    def player3_color(self): return self._player3_color
    @player3_color.setter
    def player3_color(self, v): self._player3_color = v; self.data_changed.emit()

    @property
    def player3_country(self): return self._player3_country
    @player3_country.setter
    def player3_country(self, v): self._player3_country = v; self.data_changed.emit()

    @property
    def player4_name(self): return self._player4_name
    @player4_name.setter
    def player4_name(self, v): self._player4_name = v; self.data_changed.emit()
    
    @property
    def player4_leader(self): return self._player4_leader
    @player4_leader.setter
    def player4_leader(self, v): self._player4_leader = v; self.data_changed.emit()

    @property
    def player4_color(self): return self._player4_color
    @player4_color.setter
    def player4_color(self, v): self._player4_color = v; self.data_changed.emit()

    @property
    def player4_country(self): return self._player4_country
    @player4_country.setter
    def player4_country(self, v): self._player4_country = v; self.data_changed.emit()

    @property
    def player5_name(self): return self._player5_name
    @player5_name.setter
    def player5_name(self, v): self._player5_name = v; self.data_changed.emit()
    
    @property
    def player5_leader(self): return self._player5_leader
    @player5_leader.setter
    def player5_leader(self, v): self._player5_leader = v; self.data_changed.emit()

    @property
    def player5_color(self): return self._player5_color
    @player5_color.setter
    def player5_color(self, v): self._player5_color = v; self.data_changed.emit()

    @property
    def player5_country(self): return self._player5_country
    @player5_country.setter
    def player5_country(self, v): self._player5_country = v; self.data_changed.emit()

    @property
    def player6_name(self): return self._player6_name
    @player6_name.setter
    def player6_name(self, v): self._player6_name = v; self.data_changed.emit()
    
    @property
    def player6_leader(self): return self._player6_leader
    @player6_leader.setter
    def player6_leader(self, v): self._player6_leader = v; self.data_changed.emit()

    @property
    def player6_color(self): return self._player6_color
    @player6_color.setter
    def player6_color(self, v): self._player6_color = v; self.data_changed.emit()

    @property
    def player6_country(self): return self._player6_country
    @player6_country.setter
    def player6_country(self, v): self._player6_country = v; self.data_changed.emit()

    # Player 1
    @property
    def player1_name(self): return self._player1_name
    @player1_name.setter
    def player1_name(self, value):
        self._player1_name = value
        self.data_changed.emit()

    @property
    def player1_team(self): return self._player1_team
    @player1_team.setter
    def player1_team(self, value):
        self._player1_team = value
        self.data_changed.emit()

    @property
    def player1_leader(self): return self._player1_leader
    @player1_leader.setter
    def player1_leader(self, value):
        self._player1_leader = value
        self.data_changed.emit()

    @property
    def player1_color(self): return self._player1_color
    @player1_color.setter
    def player1_color(self, value):
        self._player1_color = value
        self.data_changed.emit()

    @property
    def player1_score(self): return self._player1_score

    @property
    def player1_country(self): return self._player1_country
    @player1_country.setter
    def player1_country(self, value):
        self._player1_country = value
        self.data_changed.emit()

    # Player 2
    @property
    def player2_name(self): return self._player2_name
    @player2_name.setter
    def player2_name(self, value):
        self._player2_name = value
        self.data_changed.emit()

    @property
    def player2_team(self): return self._player2_team
    @player2_team.setter
    def player2_team(self, value):
        self._player2_team = value
        self.data_changed.emit()

    @property
    def player2_leader(self): return self._player2_leader
    @player2_leader.setter
    def player2_leader(self, value):
        self._player2_leader = value
        self.data_changed.emit()

    @property
    def player2_color(self): return self._player2_color
    @player2_color.setter
    def player2_color(self, value):
        self._player2_color = value
        self.data_changed.emit()

    @property
    def player2_score(self): return self._player2_score

    @property
    def player2_country(self): return self._player2_country
    @player2_country.setter
    def player2_country(self, value):
        self._player2_country = value
        self.data_changed.emit()

    # Match Config
    @property
    def best_of(self): return self._best_of
    @best_of.setter
    def best_of(self, value):
        self._best_of = int(value)
        self.init_matches()
        self.data_changed.emit()

    @property
    def game_type(self): return self._game_type
    @game_type.setter
    def game_type(self, value):
        self._game_type = value
        self.data_changed.emit()

    @property
    def current_map(self): return self._current_map
    @current_map.setter
    def current_map(self, value):
        self._current_map = value
        self.data_changed.emit()

    # Match Logic
    def init_matches(self):
        # Keep existing data if resizing or create new
        old_matches = getattr(self, 'matches', [])
        self.matches = []
        
        # Use match #1 leaders as template for new matches (if it exists)
        leader_template = {
            'p1_leader': 'Atriox', 'p2_leader': 'Captain Cutter',
            'p3_leader': 'Professor Anders', 'p4_leader': 'Decimus',
            'p5_leader': 'Sergeant Forge', 'p6_leader': 'Pavium',
        }
        if old_matches:
            for key in leader_template:
                if key in old_matches[0]:
                    leader_template[key] = old_matches[0][key]
        
        for i in range(self._best_of):
            if i < len(old_matches):
                m = old_matches[i]
                if 'p3_leader' not in m: m.update({'p3_leader': 'Anders', 'p4_leader': 'Decimus', 'p5_leader': 'Forge', 'p6_leader': 'Pavium'})
                self.matches.append(m)
            else:
                self.matches.append({
                    'p1_leader': leader_template['p1_leader'], 
                    'p2_leader': leader_template['p2_leader'], 
                    'p3_leader': leader_template['p3_leader'], 
                    'p4_leader': leader_template['p4_leader'], 
                    'p5_leader': leader_template['p5_leader'], 
                    'p6_leader': leader_template['p6_leader'], 
                    'winner': 0 
                })
        self.calculate_score()

    def set_match_winner(self, index, winner):
        if 0 <= index < len(self.matches):
            self.matches[index]['winner'] = winner
            self.calculate_score()
            self.data_changed.emit()

    def set_match_leader(self, index, player_key, leader_name):
        # player_key: 'p1_leader', 'p2_leader', etc.
        if 0 <= index < len(self.matches):
            self.matches[index][player_key] = leader_name
            self.data_changed.emit()

    def calculate_score(self):
        self._player1_score = sum(1 for m in self.matches if m['winner'] == 1)
        self._player2_score = sum(1 for m in self.matches if m['winner'] == 2)

    def get_current_match(self):
        # Return the first match without a winner or the last one
        for i, match in enumerate(self.matches):
            if match['winner'] == 0:
                return match, i + 1
        return self.matches[-1], len(self.matches)

    def reset_scores(self):
        """Reset all match winners to 0, keeping names, teams, and settings."""
        for match in self.matches:
            match['winner'] = 0
        self.calculate_score()
        self.data_changed.emit()
