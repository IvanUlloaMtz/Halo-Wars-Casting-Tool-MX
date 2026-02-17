import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hwctool.player_db import PlayerDB

db = PlayerDB()

# create initial
print("Creating 'TestPlayer'")
db.add_update_player("TestPlayer", {"rank_1v1": "Gold"})

# Verify
p = db.get_player("TestPlayer")
print(f"Player exists: {p is not None}")

# Now try to 'update' by changing case?
print("Updating 'testplayer' (lowercase)")
db.add_update_player("testplayer", {"rank_1v1": "Platinum"})

# Should still be one player?
print(f"Total players: {len(db.players)}")
print(f"Keys: {list(db.players.keys())}")

# Now try to 'rename' effectively by saving as new name
# This simulates what happens in UI if user changes name field
print("Saving as 'TestPlayerNew'")
db.add_update_player("TestPlayerNew", {"rank_1v1": "Diamond"})

print(f"Total players: {len(db.players)}")
print(f"Keys: {list(db.players.keys())}")
