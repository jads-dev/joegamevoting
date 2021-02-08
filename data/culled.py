import json
import requests


with open("round1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

games = data["votes"]


# print(game_ids)

resp = requests.get(f"https://joegames.nodja.com/api/game_discord/votes/")
new_games = resp.json()

new_game_ids = [game_id for game_id in new_games]

culled_games = []

ascended_ids = [
    807308420104323103,
]

for game in games:
    if game not in new_game_ids and game not in ascended_ids:
        game_data = games[game]
        culled_games.append(
            {
                "plane": "The Hell of Culled Things",
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "votes": game_data["yay"],
                "extra_emotes": [],
            },
        )


culled_games = sorted(culled_games, key=lambda k: k["votes"], reverse=True)

with open("round1_culled.json", "w", encoding="utf-8") as f:
    json.dump(culled_games, f)
