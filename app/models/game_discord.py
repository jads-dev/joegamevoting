import datetime
import json
import os
import statistics

from app.models import dbc, row_to_dictionary


def get_game(message_id, user_id=0):
    cursor = dbc.cursor()

    sql = """
        select gm.message_id as id, g.name, g.release_date, ifnull(g.summary,'') as summary , g.cover_url_big, u.can_vote
                ,case when gp.user_id is null then 1 else 0 end as can_pitch
        from discord_game_map as gm
        left join users as u on u.user_id = ?
        left join igdb_game as g on g.id = gm.game_id
        left join game_pitches_discord as gp on gp.message_id = ? and gp.user_id = u.user_id
        where gm.message_id = ?
    """

    cursor.execute(sql, (user_id, message_id, message_id))
    game = cursor.fetchone()
    return row_to_dictionary(cursor, game)


def get_game_voters(message_id):
    from app.discordbot import bot

    try:
        return bot.voters[str(message_id)]
    except KeyError:
        return {}


def get_all_game_voters(message_id):
    from app.discordbot import bot

    _voters = {}
    key = str(message_id)
    if key in bot.voters:
        _voters.update(bot.voters[key])
    if key in bot.downvoters:
        _voters.update(bot.downvoters[key])
    return _voters


def get_game_platforms(id):
    cursor = dbc.cursor()

    sql = """
        select p.name
        from igdb_game_platforms as gp
        left join igdb_platforms as p on gp.platform_id = p.id
        left join discord_game_map as gm on gm.game_id = gp.game_id
        where gm.message_id = ?
    """

    cursor.execute(sql, (id,))
    games = cursor.fetchall()
    games = [row_to_dictionary(cursor, row) for row in games]
    return games


def pitch_game(message_id, user_id, pitch):
    cursor = dbc.cursor()

    sql = """
        insert into game_pitches_discord(message_id, user_id, pitch)
        values (?, ?, ?)
    """
    cursor.execute(sql, (message_id, user_id, pitch))
    dbc.commit()


def get_game_pitches(message_id):
    cursor = dbc.cursor()

    sql = """
        select gp.*, u.username, u.avatar_url
        from game_pitches_discord as gp
        left join users as u on u.user_id = gp.user_id
        where gp.message_id = ?
        order by gp.pinned desc, gp.rowid
    """

    cursor.execute(sql, (message_id,))
    pitches = cursor.fetchall()
    pitches = [row_to_dictionary(cursor, row) for row in pitches]
    return pitches


def get_latest_pitches():
    cursor = dbc.cursor()

    sql = """
        select cast(gp.message_id as text) as message_id, u.user_id,  gp.pitch, u.username, u.avatar_url, dm.game_name, ig.cover_url_big
        from game_pitches_discord as gp
        left join users as u on u.user_id = gp.user_id
        left join discord_game_map as dm on dm.message_id = gp.message_id
        left join igdb_game as ig on ig.id = dm.game_id
        where u.user_id <> 141021676040224768
        and gp.pinned <> 1
        order by gp.created_at desc
        limit 10
    """

    cursor.execute(sql)
    pitches = cursor.fetchall()
    pitches = [row_to_dictionary(cursor, row) for row in pitches]
    return pitches


def get_random_pitches():
    cursor = dbc.cursor()
    from app.discordbot import bot

    valid_message_ids = (str(id_) for id_ in bot.valid_message_ids)
    valid_message_ids = ",".join(valid_message_ids)

    sql = f"""
        select cast(gp.message_id as text) as message_id, u.user_id, gp.pitch, u.username, u.avatar_url, dm.game_name, ig.cover_url_big
        from game_pitches_discord as gp
        left join users as u on u.user_id = gp.user_id
        left join discord_game_map as dm on dm.message_id = gp.message_id
        left join igdb_game as ig on ig.id = dm.game_id
        where gp.message_id in ({valid_message_ids})
        and gp.pinned <> 1
        and ig.id < 690000
        order by random()
        limit 10
    """

    cursor.execute(sql)
    pitches = cursor.fetchall()
    pitches = [row_to_dictionary(cursor, row) for row in pitches]
    return pitches


def get_votes():
    from app.discordbot import bot

    return bot.votes


def get_voters():
    from app.discordbot import bot

    return bot.voters


def get_stats():
    from app.discordbot import bot

    _votes = bot.votes

    extra_messages = [
        "809130993507237919",  # votos
        "809410955880562701",  # kill purple chan
        "809535003406893082",  # hug purple chan
        "810207947661508608",  # davina cage
    ]

    voters_games = [list(bot.voters[game].keys()) for game in bot.voters]
    downvoters_games = [list(bot.downvoters[game].keys()) for game in bot.downvoters]

    unique_voters = set()
    for voters in voters_games:
        for voter in voters:
            if type(voter) is str and voter not in extra_messages:
                unique_voters.add(voter)

    for voters in downvoters_games:
        for voter in voters:
            if type(voter) is str and voter not in extra_messages:
                unique_voters.add(voter)

    nr_voters = len(unique_voters)

    votes = [_votes[vote]["yay"] - _votes[vote].get("nay", 0) for vote in _votes if vote != "partial" and vote not in extra_messages]

    try:
        votes_avg = statistics.mean(votes)
        votes_median = statistics.median(votes)
    except statistics.StatisticsError:
        votes_avg = 0
        votes_median = 0

    nr_games = len(votes)
    return {"nr_games": nr_games, "nr_voters": nr_voters, "votes_average": votes_avg, "votes_median": votes_median}


def get_vote_files():
    base_dir = "./data/votes"

    return sorted([file for file in os.listdir(base_dir) if file.endswith(".json")], reverse=True)


def get_vote_file(file):
    base_dir = "./data/votes"
    with open(f"{base_dir}/{file}", "r") as f:
        data = json.load(f)
    return data["votes"]


def get_weeb_games():
    cursor = dbc.cursor()

    sql = """
        select message_id, weeb_status
        from joes_weeblist
    """

    cursor.execute(sql)
    games = cursor.fetchall()
    games = [row_to_dictionary(cursor, row) for row in games]
    return games