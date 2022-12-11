# handles user authentication

# for authentication purposes
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models, oauth2, utils
from ..database import start_session

router = APIRouter(tags=["Authentication"])

# REMEMBER: FastAPI will execute the first matched path operation (i.e. request + endpoint)


@router.post("/login")
# using OAuth2PasswordRequestForm instead of models.UserLogin, as a dependency
# note: it is sent as form data, not as json body
def login_user(
    user_form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(start_session),
):
    """Authenticates an existing user"""
    # obtain user by email (note use of exec(), select() and one())

    # oauth2 password request form returns 2 fields: username and password
    # therefore, email will be under the key 'username'
    try:
        authenticated_user = session.exec(
            select(models.User).where(models.User.email == user_form_data.username)
        ).one()
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
        ) from e

    # check if the user exists based on email

    # if found, verify if input password is correct
    if not utils.verify(user_form_data.password, authenticated_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
        )

    # create a JWT token for security
    # where payload = id, email
    user_jwt_token = oauth2.create_access_token(
        data={"user_id": authenticated_user.id, "username": authenticated_user.name}
    )

    # return the token
    return {"access_token": user_jwt_token, "token_type": "bearer"}
