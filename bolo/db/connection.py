from sqlalchemy import create_engine

from bolo.config import Config


config = Config()


def get_engine(connect_args=None):
    return create_engine(config.get("DB_CONNECT"), connect_args=connect_args or dict())


def get_connection():
    return get_engine().connect()


def get_database():
    return databases.Database(config.get("DB_CONNECT_ASYNC"))


class Q:
    def __init__(self, sql, connection=None):
        self.sql = sql
        self.connection = connection or get_connection()

    def do(self):
        result = self.connection.execute(self.sql)
        return result.fetchall()
