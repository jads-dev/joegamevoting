import requests
import sqlite3

params = {"client_id": "***REMOVED***", "client_secret": "***REMOVED***", "grant_type": "client_credentials"}


base_url = "https://id.twitch.tv/oauth2/token"


s = requests.Session()
r = s.post(base_url, params=params)
token = r.json()["access_token"]
s.headers.update({"Client-ID": params["client_id"]})
s.headers.update({"Authorization": f"Bearer {token}"})


dbc = sqlite3.connect("gamevotes.db")
c = dbc.cursor()

c.execute("select max(id) as lastid from igdb_game;")
row = c.fetchone()

lastid = row[0] or 0

offset = 0


while True:
    query = f"""
    fields name, first_release_date, platforms, summary, cover.url;
    where version_parent = null & id > {lastid};
    sort id asc;
    limit 500;
    offset {offset};
    """
    print(query)

    r = s.post("https://api.igdb.com/v4/games", data=query)

    games = r.json()
    if not games:
        break

    for game in games:
        game_id = game["id"]
        name = game["name"]
        cover_url = game.get("cover", {"url": ""})["url"]
        release_date = game.get("first_release_date", None)
        summary = game.get("summary", "")

        sql_game = """
            INSERT INTO igdb_game (id, name, cover_url, release_date, summary)
            VALUES (?,?,?,?,?)
        """

        c.execute(sql_game, (game_id, name, cover_url, release_date, summary))

        sql_platforms = """
            INSERT INTO igdb_game_platforms (game_id, platform_id)
            VALUES (?,?)
        """

        if "platforms" in game:
            platforms = [(game_id, platform) for platform in game["platforms"]]
            c.executemany(sql_platforms, platforms)

    dbc.commit()
    offset += 500


query = f"""
fields name;
limit 500;
"""
print(query)

r = s.post("https://api.igdb.com/v4/platforms", data=query)

for platform in r.json():
    print(platform)