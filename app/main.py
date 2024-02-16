from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def root():
    return { "app": "Welcome ..." }

@app.get("/token/")
async def auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
