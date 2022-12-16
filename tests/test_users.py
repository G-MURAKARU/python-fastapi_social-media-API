import pytest
from jose import jwt

from app import models
from app.config import config_settings


def test_root(client):
    res = client.get("/")  # GET request
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, name, password",
    [
        ("peacewas@neveranoption.com", "Goose", "password123"),
        ("peace@wasneveranoption.com", "Goose", "password123"),
        ("peacewasnever@anoption.com", "Goose", "password123"),
    ],
)
def test_create_user(client, email, name, password):
    """Tests the create user functionality of the API"""
    res = client.post(
        "/users/",
        json={
            "email": email,
            "name": name,
            "password": password,
        },
    )

    new_user = models.UserRead(**res.json())
    assert new_user.email == email
    assert res.status_code == 201


def test_login_user(client, test_dummy_user):
    """Tests the login functionality of the API"""
    res = client.post(
        "/login",
        data={
            "username": test_dummy_user["email"],
            "password": test_dummy_user["password"],
        },
    )

    login_res = models.Token(**res.json())

    secret_key = config_settings.fastapi_jwt_secret_key
    algorithm = config_settings.fastapi_jwt_algorithm
    payload = jwt.decode(login_res.access_token, secret_key, algorithm)

    name = payload.get("username")
    assert name == test_dummy_user["name"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("peacewas@neveranoption.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("peacewas@neveranoption.com", None, 422),
    ],
)
def test_incorrect_login(client, test_dummy_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    """Tests the API login functionality with incorrect credentials"""

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials."
