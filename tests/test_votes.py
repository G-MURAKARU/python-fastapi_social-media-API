import pytest

from app import models


@pytest.fixture
def add_dummy_vote(session, test_dummy_user, test_posts):
    """
    Adds dummy likes to a post for testing purposes
    """
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_dummy_user["id"])
    session.add(new_vote)
    session.commit()


def test_votes_on_post(authenticated_client, test_dummy_user, test_posts):
    """
    Tests API functionality for voting on/liking a post
    Requires an authenticated user to work, otherwise API throws 401
    """
    res = authenticated_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "vote_dir": 1}
    )

    assert res.status_code == 201


def test_reject_duplicate_vote(
    add_dummy_vote, authenticated_client, test_dummy_user, test_posts
):
    """
    Tests that a single user cannot like a post more than once
    """
    res = authenticated_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "vote_dir": 1}
    )

    assert res.status_code == 409


def test_reject_delete_nonexistent_vote(
    authenticated_client, test_dummy_user, test_posts
):
    """
    Tests that a user cannot downvote/un-like a post they previously had not liked/upvoted
    """
    res = authenticated_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "vote_dir": 0}
    )

    assert res.status_code == 404


def test_reject_unauthenticated_vote(client, test_dummy_user, test_posts):
    """
    Tests that an unauthenticated user is denied permission to vote on posts
    """
    res = client.post("/votes/", json={"post_id": test_posts[3].id, "vote_dir": 1})

    assert res.status_code == 401


def test_reject_vote_nonexistent_post(authenticated_client, test_dummy_user):
    """
    Tests that a user cannot like a post that does not exist
    """
    res = authenticated_client.post("/votes/", json={"post_id": 234567, "vote_dir": 0})

    assert res.status_code == 404
