from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from starlette import status
from app import models, schemas
from . import database
from sqlalchemy.orm import Session
from .config import settings


# SECRET_KEY
# ALGORITHM = HS256
# EXPIRY = 30 min



oauth_scheme = OAuth2PasswordBearer(tokenUrl="login");

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception=credentials_exception)

    user = db.query(models.User).filter(models.User.email == token.id).first()

    return user