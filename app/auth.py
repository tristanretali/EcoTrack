from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from database import get_db
from crud import get_user_by_id

SECRET_KEY = "treali"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1200

oauth2_scheme = HTTPBearer()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Impossible de valider les identifiants",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    data = {**data, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        if not subject:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, int(subject))
    if not user:
        raise credentials_exception

    return user
