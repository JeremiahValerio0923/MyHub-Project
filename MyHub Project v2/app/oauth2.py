from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from sqlalchemy.orm import Session

from . import schemas, database, models
from .config import settings

SECRET_KEY = settings.jwt_encode_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")

def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire_in = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    jwt_str = jwt.encode(to_encode, key=SECRET_KEY, algorithm = ALGORITHM)
    return jwt_str


def verify_access_token(token: str, credential_exception: Exception):
    """Verify JWT

    :param token: JWT to verify
    :param credential_exception: invalid credentials exception
    :return: token scheme
    """

    try: 
        payload = jwt.decode(token, key = SECRET_KEY, algorithms = [ALGORITHM])
    except JWTError: 
        raise credential_exception
    user_id = payload.get("user_id")
    if user_id is None: 
        raise credential_exception
    return schemas.TokenData(user_id=user_id) 



def verify_current_user(token: str = Depends(oauth2_scheme),
                        db: Session = Depends(database.get_db)) -> models.User:

    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
    detail = "Could not verify credentials",
    headers = {"WWW-Authenticate": " Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter_by(id=token_data.user_id).first()
    return user