import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from bolo.auth.user_sqlalchemy import UserTable, UserList
from bolo.db.connection import get_engine, get_connection, Q

# put all users in a variable
user_table = UserTable.__table__
connection = get_connection()
user_query = db.select([user_table])
users = list(UserList.parse_obj(connection.execute(user_query).fetchall()))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
db = SessionLocal()

# create query object
q = Q()
