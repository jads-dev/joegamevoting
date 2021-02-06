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

    return bot.voters[str(message_id)]


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