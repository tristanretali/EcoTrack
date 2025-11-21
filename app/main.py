from fastapi import FastAPI
from database import init_db

app = FastAPI(title="Ecotrack API")


@app.on_event("startup")
def on_startup():
    init_db()
