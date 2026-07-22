from fastapi import FastAPI
from contextlib import asynccontextmanager

from expenses.routes import router as expenses_routes
from users.routes import router as users_routes
from super_admin.routes import router as super_admin_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting the application")
    yield
    print("shuting down the application")


app = FastAPI(lifespan=lifespan)

app.include_router(expenses_routes)
app.include_router(users_routes)
app.include_router(super_admin_routes)
