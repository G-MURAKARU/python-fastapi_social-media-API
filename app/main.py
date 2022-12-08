# API -> SCHEMA

# import psycopg2 <- database driver, used when not using an ORM
# from psycopg2.extras import RealDictCursor -> to extract the column names

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

# to import our app routes
from .routers import auth, posts, users, vote

# below imports not required because of alembic
# from .database import SQLModel, create_db_and_tables


# to enforce a schema
# import pydantic <- SQLModel ORM & FastAPI use Pydantic models in the background
# for data validation and sanitation


# to create an instance of FastApi
app = FastAPI()

# CORS and Middleware
origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# to create our database tables (does not need a session)
# commented out because DB will be created with alemmbic
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# REMEMBER: FastAPI will execute the first matched path operation (i.e. request + endpoint)

# imports our routes
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# path operation/route/endpoint
@app.get("/")
# FastApi leverages asynchronous processing
def root():
    return {
        "message": "Hello World"
    }  # FastAPI will automatically convert this to JSON before sending it back to the client
