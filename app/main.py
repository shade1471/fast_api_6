import os
from contextlib import asynccontextmanager

import dotenv

dotenv.load_dotenv()

from app.database.users import create_user
from app.database.data import users_data

dotenv.load_dotenv()
from urllib.parse import urlparse
import uvicorn

from app.database.engine import create_db_and_tables

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import status, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    for user in users_data.values():
        create_user(user)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)

if __name__ == "__main__":
    parsed_app_url = urlparse(os.getenv('APP_URL'))
    uvicorn.run(app, host=parsed_app_url.hostname, port=parsed_app_url.port)
