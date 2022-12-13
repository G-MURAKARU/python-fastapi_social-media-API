# some necessary imports
from sqlmodel import Session, create_engine

from .config import config_settings
from .models import SQLModel

# to define the network connection credentials for the SQL ORM engine
# engine - object that handles communication with the database

### USING ENV VARIABLES INSTEAD OF HARD CODING VALUES FOR SAFETY REASONS ###
postgresql_username = config_settings.fastapi_postgresql_db_username
postgresql_password = config_settings.fastapi_postgresql_db_password
postgresql_hostname = config_settings.fastapi_postgresql_db_hostname
postgreql_db_name = config_settings.fastapi_postgresql_db_name
postgresql_port = config_settings.fastapi_postgresql_db_port

# URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLMODEL_DATABASE_URL = f"postgresql://{postgresql_username}:{postgresql_password}@{postgresql_hostname}:{postgresql_port}/{postgreql_db_name}"

# to create the engine
# connect_args = {"check_same_thread": False}
engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

# not needed anymore, DB migrations handled by alembic
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# getting DB sessions as a dependency, to eliminate 'with' and make life easier
def start_session():
    with Session(engine) as session:
        yield session
