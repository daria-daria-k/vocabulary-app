from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth")

@app.get("/")
def root():
    return {"status": "ok"}
