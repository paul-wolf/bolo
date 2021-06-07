from typing import List

import databases
import sqlalchemy
from fastapi import Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    event,
)
from pydantic import BaseModel

from bolo.config import Config

config = Config()

DATABASE_URL = config.get("DB_CONNECT_ASYNC")
SECRET = config.get("SECRET")


class User(models.BaseUser):
    pass


class UserList(BaseModel):
    __root__: List[User]


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    # crikey, by default they try to use "user" as table name; but that's a reserved word in pg
    __tablename__ = "auth_user"
    comment = Column(String(length=320), unique=True, index=True, nullable=False)


# engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = sqlalchemy.create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")


def setup_users(app):
    fastapi_users = FastAPIUsers(
        user_db,
        [jwt_authentication],
        User,
        UserCreate,
        UserUpdate,
        UserDB,
    )
    app.include_router(fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"])
    app.include_router(fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"])
    app.include_router(
        fastapi_users.get_reset_password_router(SECRET, after_forgot_password=on_after_forgot_password),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(SECRET, after_verification_request=after_verification_request),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
