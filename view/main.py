from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from bolo.auth.user_sqlalchemy import setup_users
from bolo.db.connection import get_database
from .user import router as user_router

database = get_database()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)


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
