from fastapi import FastAPI

from bolo.auth.user_sqlalchemy import setup_users


app = FastAPI()

setup_users(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
