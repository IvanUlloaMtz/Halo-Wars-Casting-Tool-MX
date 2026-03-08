import asyncio
import websockets
import json

async def send_msg():
    uri = "ws://localhost:7305"
    async with websockets.connect(uri) as websocket:
        data1 = {
            "type": "update_score",
            "data": {
                "p1": {"score": "0", "name": "Player 1", "leader": "anders", "color": "#ff0000", "country": "us"},
                "p2": {"score": "0", "name": "Player 2", "leader": "cutter", "color": "#0000ff", "country": "uk"},
                "game_type": "DEATHMATCH",
                "best_of": 3,
                "matches": [],
                "team_size": 1,
                "show_team_names": False,
                "show_flags": True
            }
        }
        await websocket.send(json.dumps(data1))
        print("Sent init data")
        await asyncio.sleep(5)
        
        data1["data"]["p1"]["score"] = "10"
        data1["data"]["p2"]["score"] = "20"
        await websocket.send(json.dumps(data1))
        print("Sent 10-20 score data")
        await asyncio.sleep(5)

asyncio.run(send_msg())
