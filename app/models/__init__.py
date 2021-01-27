import sqlite3

dbc = sqlite3.connect("gamevotes.db")


def row_to_dictionary(cursor, row):
    if row:
        return dict(zip([column[0] for column in cursor.description], row))


class Votes:
    def __init__(self):
        self.data = []


votes = Votes()