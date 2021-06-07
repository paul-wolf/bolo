import sqlalchemy as db

from bolo.auth.user_sqlalchemy import UserTable
from bolo.db.connection import get_engine, get_connection, Q

user_table = UserTable.__table__

connection = get_connection()
user_query = db.select([user_table])

result = connection.execute(user_query)
users = result.fetchall()
users
