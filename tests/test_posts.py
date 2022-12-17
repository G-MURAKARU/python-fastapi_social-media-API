import pytest

from app import models

### TESTS FOR GETTING POSTS ###


def test_get_all_posts(authenticated_client, test_posts):
    """
    Tests the API endpoint for getting all posts
    Requires an authenticated user to work
    """

    res = authenticated_client.get("/posts/")

    def validate(post):
        """Validates returned data with Pydantic"""

        return models.PostOut(**post)  # expects a 'mapping' i.e. dictionary

    dummy_data = list(map(validate, res.json()))

    assert res.status_code == 200
    assert len(dummy_data) == len(res.json())
    for index, value in enumerate(dummy_data):
        # because only using one dummy user
        assert value.Post.owner.id == test_posts[index].owner_id


def test_get_one_post(authenticated_client, test_posts):
    """
    Tests the API endpoint for getting a single, existent post
    Requires an authenticated user to work
    """

    res = authenticated_client.get(f"/posts/{test_posts[0].id}")
    dummy_data = models.PostOut(**res.json())

    assert res.status_code == 200
    assert dummy_data.Post.owner.id == 1
    assert dummy_data.Post.id == test_posts[0].id
    assert dummy_data.Post.content == test_posts[0].content


def test_unauthenticated_user_reject_all_posts(client, test_posts):
    """
    Tests if an unauthenticated user is denied access to all posts
    """

    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthenticated_user_reject_one_post(client, test_posts):
    """
    Tests if an unauthenticated user is denied access to one post
    """

    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_reject_nonexistent_post(authenticated_client):
    """
    Tests if a 404 is thrown if a user tries to request for a nonexistent post
    """

    res = authenticated_client.get("/posts/21345678")
    assert res.status_code == 404


### TESTS FOR CREATING POSTS ###


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "burj khalifa", None),
    ],
)
def test_create_post(
    authenticated_client, test_dummy_user, test_posts, title, content, published
):
    """Tests API create post functionality"""

    res = authenticated_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = models.PostRead(**res.json())

    assert res.status_code == 201
    assert created_post.owner.id == test_dummy_user["id"]
    assert created_post.title == title
    assert created_post.published == published if published is not None else True


def test_unauthenticated_user_reject_create_post(client, test_dummy_user, test_posts):
    """
    Tests if an unauthenticated user is prevented from creating a post
    """

    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"}
    )

    assert res.status_code == 401


### TESTS FOR DELETING POST ###


def test_unauthenticated_user_reject_delete_post(client, test_dummy_user, test_posts):
    """
    Tests if an unauthenticated user is prevented from deleting a post
    """

    res = client.delete(f"posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authenticated_client, test_dummy_user, test_posts):
    """Tests API delete post functionality"""

    res = authenticated_client.delete(f"posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_reject_delete_nonexistent_post(
    authenticated_client, test_dummy_user, test_posts
):
    """
    Tests if a 404 is thrown if a user tries to delete a nonexistent post
    """

    res = authenticated_client.delete("posts/2345678987")
    assert res.status_code == 404


def test_reject_delete_other_user_post(
    authenticated_client, test_dummy_user, test_posts
):
    """
    Tests if a user us prevented from deleting a post that is not their own
    """

    res = authenticated_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authenticated_client, test_dummy_user, test_posts):
    """Tests API update post functionality"""

    res = authenticated_client.patch(
        f"/posts/{test_posts[0].id}", json={"content": "updated content"}
    )

    print(res.json())
    updated_post = models.PostRead(**res.json())

    assert res.status_code == 200
    assert updated_post.content == "updated content"
    assert updated_post.owner.id == test_dummy_user["id"]
    assert updated_post.title == "first title"


def test_reject_update_other_user_post(
    authenticated_client, test_dummy_user, test_posts
):
    """
    Tests if a user is prevented from updating a post that is not their own
    """

    res = authenticated_client.patch(
        f"/posts/{test_posts[3].id}", json={"content": "updated content"}
    )
    assert res.status_code == 403


def test_reject_update_nonexistent_post(
    authenticated_client, test_dummy_user, test_posts
):
    """
    Tests inability to update a nonexistent post
    """

    res = authenticated_client.patch(
        "/posts/3454345353", json={"content": "updated content"}
    )

    assert res.status_code == 404


def test_unauthenticated_user_reject_update_post(client, test_dummy_user, test_posts):
    """
    Tests if an unauthenticated user is prevented from updating a post
    """

    res = client.patch(
        f"/posts/{test_posts[0].id}", json={"content": "updated content"}
    )

    assert res.status_code == 401
