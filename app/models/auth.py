from pydantic import BaseModel

from app.models import dbc, row_to_dictionary


class TokenData(BaseModel):
    user_id: int = None


class User(BaseModel):
    user_id: int
    username: str = None
    avatar_url: str = None
    can_vote: bool = False


def get_user(user_id: int):
    cursor = dbc.cursor()
    cursor.execute("select * from users where user_id = ? LIMIT 1", (user_id,))
    user = cursor.fetchone()

    if user:
        return row_to_dictionary(cursor, user)


def register_user(user_id, username, avatar_url):
    cursor = dbc.cursor()
    sql = """
        insert into users (user_id, username, avatar_url) 
        values (?,?,?) 
        ON CONFLICT(user_id) DO 
        UPDATE SET username = ?, avatar_url = ?
        where user_id = ?
    """
    cursor.execute(sql, (user_id, username, avatar_url, username, avatar_url, user_id))
    dbc.commit()


def set_can_vote(user_id, can_vote):
    cursor = dbc.cursor()
    sql = """
        update users 
        set can_vote = ?
        where user_id = ?
    """
    cursor.execute(sql, (can_vote, user_id))
    dbc.commit()