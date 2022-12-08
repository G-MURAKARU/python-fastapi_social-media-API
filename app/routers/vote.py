from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models, oauth2
from ..database import start_session

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_vote(
    vote: models.UserVote,
    session: Session = Depends(start_session),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = session.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post (id: {vote.post_id}) Not Found.",
        )

    vote_query = select(models.Vote).where(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )

    try:
        voted_post = session.exec(vote_query).one()
        if vote.vote_dir == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"You ({current_user.name}) have already voted on post {vote.post_id}",
            )

        session.delete(voted_post)
        session.commit()
        return {"message": "vote deleted."}

    except NoResultFound:
        if vote.vote_dir == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote on post {vote.post_id} not found.",
            )

        new_vote = models.Vote.from_orm(
            vote, update={"user_id": current_user.id, "post_id": vote.post_id}
        )
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return {"message": "post liked successfully."}
