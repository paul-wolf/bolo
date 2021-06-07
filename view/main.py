from typing import List

from fastapi import FastAPI

from bolo.auth.user_sqlalchemy import setup_users, UserTable, User
from bolo.db.connection import get_database

database = get_database()


app = FastAPI()

setup_users(app)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = UserTable.__table__.select()
    return await database.fetch_all(query)
