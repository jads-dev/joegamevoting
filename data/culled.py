import json
import requests


with open("round1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

games = data["votes"]

files = ["round2p1.json", "round2p2.json", "round3p1.json", "round3p1.json", "round3p2.json", "round3p3.json", "round4p1.json", "round4p2.json"]
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
veldt_games = []
specials_games = []

outer_heaven_ids = [
    807294358520725585,
    807308420104323103,
    807297766970753044,
    807296278668115978,
    807293645057163285,
    807297543825653801,
    807303944002994186,
    807304931588964362,
    807293508821844019,
    807302499831775244,
    807298868194050068,
    807308502921904158,
]

ascended_ids = [
    807296785231118376,
    807290323952599080,
    807307475535396904,
    807289635243032597,
    807296983286415411,
    807297421604421640,
    807307725754597408,
    809131123099041832,
    809131104320618546,
    807296037965266975,
    807307201949204520,
    807299662301626389,
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

veldt_ids = [
    807295814442418176,
    807295814442418176,
    807297867923718186,
    809131141776015472,
    807304581843386458,
    807292471842570311,
    807296202739286066,
    807299830787080222,
    809131166321213471,
    807294093943111710,
    807294650033242173,
    807291135633522789,
    807297742178615306,
    807290290658082826,
    807296503378346004,
    807306157294223392,
    807295787854987314,
    807298319528493146,
    807294804731887656,
    807295712504315974,
    807306017939259433,
    807297524762935347,
]

specials_games_ids = [
    809130993507237919,
    809410955880562701,
    809535003406893082,
    810207947661508608,
]

outer_heaven_ids = [str(id_) for id_ in outer_heaven_ids]
ascended_ids = [str(id_) for id_ in ascended_ids]
double_hell_ids = [str(id_) for id_ in double_hell_ids]
veldt_ids = [str(id_) for id_ in veldt_ids]
specials_games_ids = [str(id_) for id_ in specials_games_ids]


outer_heaven_games.append(
    {
        "message_id": "69",
        "name": "A Glowing Light",
        "emote": "🔆",
        "emote_unicode": True,
        "votes": 29.1,
        "downvotes": 0,
        "absolute": 29.1,
        "extra_emotes": [],
    },
)

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
                "emote2": game_data.get("emote2", None),
                "emote2_unicode": game_data.get("emote2_unicode", None),
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
                "emote2": game_data.get("emote2", None),
                "emote2_unicode": game_data.get("emote2_unicode", None),
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
                "emote2": game_data.get("emote2", None),
                "emote2_unicode": game_data.get("emote2_unicode", None),
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
            },
        )
    elif game in veldt_ids:
        veldt_games.append(
            {
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "emote2": game_data.get("emote2", None),
                "emote2_unicode": game_data.get("emote2_unicode", None),
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
            }
        )
    elif game in specials_games_ids:
        specials_games.append(
            {
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "emote2": game_data.get("emote2", None),
                "emote2_unicode": game_data.get("emote2_unicode", None),
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
            }
        )

    elif game not in new_game_ids:
        culled_games.append(
            {
                "message_id": game,
                "name": game_data["game"],
                "emote": game_data["emote"],
                "emote_unicode": game_data["emote_unicode"],
                "emote2": game_data.get("emote2", None),
                "emote2_unicode": game_data.get("emote2_unicode", None),
                "votes": game_data["yay"],
                "downvotes": game_data.get("nay", 0),
                "absolute": game_data["yay"] - game_data.get("nay", 0),
                "extra_emotes": [],
                "rank": "-",
            },
        )
    else:
        print(game)

    #   emote2: this.votes[key].emote2,
    #   emote2_unicode: this.votes[key].emote2_unicode,
    #   weeb_status: this.votes[key].weeb_status,

data = {
    "outer_heaven": sorted(outer_heaven_games, key=lambda k: k["absolute"], reverse=True),
    "ascended_games": sorted(ascended_games, key=lambda k: k["absolute"], reverse=True),
    "double_hell_games": sorted(double_hell_games, key=lambda k: k["absolute"], reverse=True),
    "culled_games": sorted(culled_games, key=lambda k: k["absolute"], reverse=True),
    "veldt_games": sorted(veldt_games, key=lambda k: k["absolute"], reverse=True),
    "specials_games": sorted(specials_games, key=lambda k: k["absolute"], reverse=True),
}


with open("culled.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

with open("culled_old.json", "r", encoding="utf-8") as f:
    data = json.load(f)

old_culled_ids = [culled["message_id"] for culled in data["culled_games"]]

# for culled in culled_games:
#     if culled["message_id"] not in old_culled_ids:
#         print(culled["message_id"])

# for culled in culled_games:
#     if culled["message_id"] not in old_culled_ids:
#         print(culled["name"])
