from typing import Dict

import bcrypt
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.async_db import get_db
from src.database.models.Users import Users

router = APIRouter()


class UserInfo(BaseModel):
    username: str
    password: str
    email: str


@router.post("/signup", name="signup")
async def create_user( new_user_info: UserInfo, db_session: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    same_email = await db_session.execute(select(Users).where(Users.email == new_user_info.email))
    is_unique = True if same_email.one_or_none() is not None else False
    if is_unique:
        return {"status": "409"} # deal with non unique email.
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_user_info.password.encode(), salt).decode()
    new_user: Users = Users(
        username=new_user_info.username,
        password=hashed_password,
        salt=salt.decode(),
        email=new_user_info.email,
        )
    db_session.add(new_user)
    await db_session.commit()
    return {"status": "201"}
