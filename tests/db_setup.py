import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.database import start_session
from app.main import app

### TESTING DATABASE SETUP ###
# to define the network connection credentials for the SQL ORM engine
# engine - object that handles communication with the database

# URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLMODEL_DATABASE_URL = (
    "postgresql://postgres:lifegoeson@localhost:5432/FastAPI_TestingDB"
)

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
