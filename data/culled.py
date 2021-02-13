import json
import requests


with open("round1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

games = data["votes"]

files = ["round2p1.json", "round2p2.json", "round3p1.json", "round3p1.json", "round3p2.json"]
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    games.update(data["votes"])

# print(game_ids)

resp = requests.get(f"https://joegames.nodja.com/api/game_discord/votes/")
new_games = resp.json()

new_game_ids = [game_id for game_id in new_games]

outer_heaven_games = []
ascended_games = []
culled_games = []
double_hell_games = []

outer_heaven_ids = [
    807294358520725585,
    807308420104323103,
    807297766970753044,
    807296278668115978,
    807293645057163285,
    807297543825653801,
    807303944002994186,
    807304931588964362,
]

ascended_ids = [
    807298868194050068,
]

double_hell_ids = [
    807295004484960276,
    807303838037311548,
    807303892542160947,
    807297271385423903,
    807303868806856784,
    807303813899091968,
    807303919440756786,
    807293807593783307,
    807289797005279263,
    807298026132996116,
    807301920464044153,
    807301973019852880,
    807306639421997056,
    807307291144618064,
    807308048426991626,
    807294093943111710,  # dogs life
    807299830787080222,  # no one can stop
]

outer_heaven_ids = [str(id_) for id_ in outer_heaven_ids]
ascended_ids = [str(id_) for id_ in ascended_ids]
double_hell_ids = [str(id_) for id_ in double_hell_ids]


for game in games:
    game_data = games[game]
    if game == "partial":
        continue
    # print(game, ascended_ids[0], type(game), type(ascended_ids[0]))

    if game in outer_heaven_ids:
        outer_heaven_games.append(
            {
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
            },
        )
    elif game in ascended_ids:
        ascended_games.append(
            {
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
            },
        )
    elif game in double_hell_ids:
        double_hell_games.append(
            {
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
            },
        )
    elif game not in new_game_ids:
        culled_games.append(
            {
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
                "rank": "-",
            },
        )

        #   emote2: this.votes[key].emote2,
        #   emote2_unicode: this.votes[key].emote2_unicode,
        #   weeb_status: this.votes[key].weeb_status,

data = {
    "outer_heaven": sorted(outer_heaven_games, key=lambda k: k["votes"], reverse=True),
    "ascended_games": sorted(ascended_games, key=lambda k: k["votes"], reverse=True),
    "double_hell_games": sorted(double_hell_games, key=lambda k: k["votes"], reverse=True),
    "culled_games": sorted(culled_games, key=lambda k: k["votes"], reverse=True),
}


with open("culled.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

with open("culled_old.json", "r", encoding="utf-8") as f:
    data = json.load(f)

old_culled_ids = [culled["message_id"] for culled in data["culled_games"]]
for culled in culled_games:
    if culled["message_id"] not in old_culled_ids:
        print(culled["message_id"])

for culled in culled_games:
    if culled["message_id"] not in old_culled_ids:
        print(culled["name"])
