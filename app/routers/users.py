from sqlmodel import Session

# to 'access the app object' from main, FastAPI uses routers
from fastapi import APIRouter, Depends, HTTPException, status

from .. import models, utils
from ..database import start_session

# app is not imported from main, use APIRouter
# refactoring, to avoid repeated "/users"
router = APIRouter(prefix="/users", tags=["Users"])

# REMEMBER: FastAPI will execute the first matched path operation (i.e. request + endpoint)

# API endpoint to create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.UserRead)
def create_user(user: models.UserCreate, session: Session = Depends(start_session)):
    # create password hash for password encryption
    hashed_password = utils.hash(user.password)

    # creating the user
    user.password = hashed_password
    new_user = models.User.from_orm(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# API endpoint to retrieve user info based on ID
@router.get("/{user_id}", response_model=models.UserReadWithPosts)
def get_user(user_id: int, session: Session = Depends(start_session)):
    if queried_user := session.get(models.User, user_id):
        return queried_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User (id: {user_id}) Not Found.",
        )
