from fastapi import FastAPI
from .router import router
from .database import init_db


app = FastAPI(title="Tron Wallet Info")

init_db()
app.include_router(router)
