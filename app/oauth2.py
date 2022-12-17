# handles authentication - JWT tokens

from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from fastapi import Depends, HTTPException, status

from . import models
from .config import config_settings
from .database import start_session

### USING ENV VARIABLES INSTEAD OF HARD CODING VALUES FOR SAFETY REASONS ###
# obtain secret key
SECRET_KEY = config_settings.fastapi_jwt_secret_key
# signing algorithm
ALGORITHM = config_settings.fastapi_jwt_algorithm
# token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = config_settings.fastapi_jwt_access_token_expire_minutes

# this makes FastAPI know that it is a security scheme, so it is added that way to OpenAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    # sourcery skip: inline-immediately-returned-variable
    """Generates a JWT token for a logged-in user"""
    # initialising the payload to populate the JWT token
    jwt_payload = data.copy()

    # setting the token's lifetime (30 minutes)
    jwt_lifetime = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # update the payload to carry the token's lifetime (it's a dict)
    jwt_payload["exp"] = jwt_lifetime

    # creating the JWT token
    # 1. payload
    # 2. secret key
    # 3. algorithm
    jwt_token = jwt.encode(jwt_payload, SECRET_KEY, ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):
    """Validates a provided JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        _id = payload.get("user_id")
        name = payload.get("username")

        if not _id:
            raise credentials_exception

        token_data = models.TokenPayload(id=_id, name=name)
    except JWTError as error:
        raise credentials_exception from error

    return token_data


# passed as a dependency in any endpoint to extract user's id
# "get" - actually fetches the current user from the database
def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(start_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_token = verify_access_token(token, credentials_exception)

    if logged_in_user := session.get(models.User, int(user_token.id)):
        return logged_in_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User (id: {user_token.id}) Not Found.",
        )
