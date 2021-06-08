from typing import List

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from bolo.auth.user_sqlalchemy import UserTable, User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# @app.get("/alternative_users", response_model=List[User])
# async def read_users():
#     query = UserTable.__table__.select()
#     return await database.fetch_all(query)
