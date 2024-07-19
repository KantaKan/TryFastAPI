from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "30b458570519c58538c06630779f4c3c85f92b3d6a7ccdb6dc94e34a19030c87"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30


app = FastAPI()

class Data(BaseModel):
    name : str
    image : str



@app.post("/create/")
async def creat(data:Data):
    return {"data": data}


@app.get("/test/{item_id}")
async def test(item_id: str , query: int):
    return {"hello": item_id}

