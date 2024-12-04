from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import menu, user
from database.connection import create_tables

app = FastAPI()

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(user.router, prefix="/user", tags=["User"])
