from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "30b458570519c58538c06630779f4c3c85f92b3d6a7ccdb6dc94e34a19030c87"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30



fake_db = {
    "Kan": {
        "username": "kan",
        "full_name": "Kan Kanta",
        "email": "kan@mail.com",
        "hashed_password": "",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username:str
    email:str or None = None
    full_name:str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password:str



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

app = FastAPI()

def verify_password(password , hashed_password):
    return pwd_context.verify(password,hashed_password)

def get_password(password):
    return pwd_context.hashed(password)

def get_user(db, username : str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    

def authenticate_user(db, username : str,password:str):
    user = get_user(db, username)
    if not user :
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta 
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    try: 
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
    except:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user


async def get_current_active_user(current: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


