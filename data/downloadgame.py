import requests
import sqlite3
import sys

params = {"client_id": "***REMOVED***", "client_secret": "***REMOVED***", "grant_type": "client_credentials"}


base_url = "https://id.twitch.tv/oauth2/token"


s = requests.Session()
r = s.post(base_url, params=params)
token = r.json()["access_token"]
s.headers.update({"Client-ID": params["client_id"]})
s.headers.update({"Authorization": f"Bearer {token}"})


dbc = sqlite3.connect("gamevotes.db")
c = dbc.cursor()


game_id = sys.argv[1]

query = f"""
fields name, first_release_date, platforms, summary, cover.url;
where id = {game_id};
sort id asc;
limit 500;
"""
print(query)

r = s.post("https://api.igdb.com/v4/games", data=query)

games = r.json()

for game in games:
    print(game)
    game_id = game["id"]
    name = game["name"]
    cover_url = game.get("cover", {"url": ""})["url"]
    cover_url_big = cover_url.replace("/t_thumb/", "/t_cover_big/")
    release_date = game.get("first_release_date", None)
    summary = game.get("summary", "")

    sql_game = """
        INSERT INTO igdb_game (id, name, cover_url, cover_url_big, release_date, summary)
        VALUES (?,?,?,?,?,?)
    """

    c.execute(sql_game, (game_id, name, cover_url, cover_url_big, release_date, summary))

    sql_platforms = """
        INSERT INTO igdb_game_platforms (game_id, platform_id)
        VALUES (?,?)
    """

    if "platforms" in game:
        platforms = [(game_id, platform) for platform in game["platforms"]]
        c.executemany(sql_platforms, platforms)

dbc.commit()