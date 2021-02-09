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

    nr_games = len(_votes) - 1
    voters_games = [list(bot.voters[game].keys()) for game in bot.voters]

    unique_voters = set()
    for voters in voters_games:
        unique_voters |= set(voters)

    nr_voters = len(unique_voters)

    votes = [_votes[vote]["yay"] for vote in _votes if vote != "partial"]

    try:
        votes_avg = statistics.mean(votes)
        votes_median = statistics.median(votes)
    except statistics.StatisticsError:
        votes_avg = 0
        votes_median = 0

    return {"nr_games": nr_games, "nr_voters": nr_voters, "votes_average": votes_avg, "votes_median": votes_median}
