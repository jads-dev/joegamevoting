from app.models import dbc, row_to_dictionary, votes
from app.routers.socketio import send_votes


def get_game_search(search_terms):
    cursor = dbc.cursor()

    search_terms = search_terms.replace(" ", "%")
    search_terms = f"%{search_terms}%"

    sql = """
        select id, name, cover_url, release_date
        from igdb_game
        where name_normal like ?
        LIMIT 50
    """

    cursor.execute(sql, (search_terms,))
    games = cursor.fetchall()
    games = [row_to_dictionary(cursor, row) for row in games]
    return games


def get_game(game_id, user_id=0, poll=0):
    cursor = dbc.cursor()

    sql = """
        select id, name, cover_url_big, release_date, summary, v.vote, u.can_vote, b.block_level, b.reason,
            case when gp.user_id is null then 1 else 0 end as can_pitch
        from igdb_game as ig
        left join users as u on u.user_id = ?
        left join votes as v on v.game_id = ig.id and v.poll = ? and v.user_id = u.user_id
        left join blocked_games as b on b.game_id = ig.id and b.poll = ?
        left join game_pitches as gp on gp.game_id = ig.id and gp.user_id = u.user_id
        where ig.id = ?
    """

    cursor.execute(sql, (user_id, poll, poll, game_id))
    game = cursor.fetchone()
    return row_to_dictionary(cursor, game)


def get_game_platforms(id):
    cursor = dbc.cursor()

    sql = """
        select p.name
        from igdb_game_platforms as gp
        left join igdb_platforms as p on gp.platform_id = p.id
        where game_id = ?
    """

    cursor.execute(sql, (id,))
    games = cursor.fetchall()
    games = [row_to_dictionary(cursor, row) for row in games]
    return games


def vote_game(poll, game_id, user_id, upvote):
    cursor = dbc.cursor()

    sql = """
        insert into votes(poll, game_id, user_id, vote)
        values (?, ?, ?, ?)
        ON CONFLICT(poll, game_id, user_id) DO 
        UPDATE SET vote = ?
        where poll = ? and game_id = ? and user_id = ?

    """
    cursor.execute(sql, (poll, game_id, user_id, upvote, upvote, poll, game_id, user_id))
    dbc.commit()


async def calc_votes():
    cursor = dbc.cursor()

    sql = """
        select v.game_id, sum(vote) as votes, g.name
        from votes as v
        left join igdb_game as g on g.id = v.game_id
        left join blocked_games as b on b.game_id = g.id and b.poll = 0
        where v.poll = 0
        and b.block_level is null
        group by v.game_id
        having sum(vote) > 0
        order by sum(vote) desc
    """

    cursor.execute(sql)
    _votes = cursor.fetchall()
    _votes = [row_to_dictionary(cursor, row) for row in _votes]

    votes.data = _votes

    await send_votes()


def get_game_voters(poll, game_id):
    cursor = dbc.cursor()

    sql = """
        select u.user_id, u.username, u.avatar_url
        from votes as v
        left join users as u on u.user_id = v.user_id
        where poll = ?
        and v.vote = 1
        and v.game_id = ?
        order by v.rowid
    """

    cursor.execute(sql, (poll, game_id))
    voters = cursor.fetchall()
    voters = [row_to_dictionary(cursor, row) for row in voters]
    return voters


def pitch_game(game_id, user_id, pitch):
    cursor = dbc.cursor()

    sql = """
        insert into game_pitches(game_id, user_id, pitch)
        values (?, ?, ?)
    """
    cursor.execute(sql, (game_id, user_id, pitch))
    dbc.commit()


def get_game_pitches(game_id):
    cursor = dbc.cursor()

    sql = """
        select gp.*, u.username, u.avatar_url
        from game_pitches as gp
        left join users as u on u.user_id = gp.user_id
        where gp.game_id = ?
        order by gp.rowid
    """

    cursor.execute(sql, (game_id,))
    pitches = cursor.fetchall()
    pitches = [row_to_dictionary(cursor, row) for row in pitches]
    return pitches