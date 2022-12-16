from pydantic import BaseSettings


# the BaseSettings class from Pydantic helps us ensure that all environment variables
# needed by the application have been imported from the machine's OS,
# akin to using the OS module and getenv() function
# helps in keeping track of environment variables, that change in different environments
# (e.g. development vis-a-vis production)
# it scans the env variable (like running env/printenv in terminal) for case insensitive matches
# and assigns them
class ConfigSettings(BaseSettings):
    fastapi_postgresql_db_username: str
    fastapi_postgresql_db_password: str
    fastapi_postgresql_db_hostname: str
    fastapi_postgresql_db_name: str
    fastapi_postgresql_db_port: str
    fastapi_jwt_secret_key: str
    fastapi_jwt_algorithm: str
    fastapi_jwt_access_token_expire_minutes: int

    # telling Pydantic where to look for the environment variables
    class Config:
        # env_file = "/Users/not-gich/.zshrc"
        env_file = ".env"


# instantiating the above class (to run it an extract the values)
config_settings = ConfigSettings()
