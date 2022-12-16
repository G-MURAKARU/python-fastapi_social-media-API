# special file used by pytest that can be accessed globally within the test suite
# commonly-used code should be stored here
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.config import config_settings
from app.database import start_session
from app.main import app

### TESTING DATABASE SETUP ###
# to define the network connection credentials for the SQL ORM engine
# engine - object that handles communication with the database

### USING ENV VARIABLES INSTEAD OF HARD CODING VALUES FOR SAFETY REASONS ###
postgresql_username = config_settings.fastapi_postgresql_db_username
postgresql_password = config_settings.fastapi_postgresql_db_password
postgresql_hostname = config_settings.fastapi_postgresql_db_hostname
postgresql_port = config_settings.fastapi_postgresql_db_port

# URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLMODEL_DATABASE_URL = f"postgresql://{postgresql_username}:{postgresql_password}@localhost:{postgresql_port}/FastAPI_TestingDB"

# to create the engine
test_engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

# SCOPE OF FIXTURES, see pytest docs
@pytest.fixture(scope="function")
def session():
    """(Re)creates a fresh, empty database for each test. Returns the Session object"""
    # using SQLModel
    SQLModel.metadata.drop_all(bind=test_engine)
    SQLModel.metadata.create_all(bind=test_engine)

    # using Alembic
    # alembic.command.downgrade("base")
    # alembic.command.upgrade("head")

    with Session(test_engine) as test_session:
        yield test_session


@pytest.fixture(scope="function")
def client(session):
    """Overrides the default app session dependency. Returns the TestClient object"""

    def override_start_session():
        with session as test_session:
            yield test_session

    # FastAPI can allow for dependency overrides as shown below
    app.dependency_overrides[start_session] = override_start_session

    yield TestClient(app)


@pytest.fixture
def test_dummy_user(client):
    """Creates a dummy user that's used to test the login functionality"""
    user_data = {
        "email": "peacewas@neveranoption.com",
        "name": "Goose",
        "password": "password123",
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    # to return the new user (details)
    new_user = res.json()
    new_user["password"] = user_data.get("password")
    return new_user
