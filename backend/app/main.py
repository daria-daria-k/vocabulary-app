from fastapi import FastAPI
from app.routers import auth, words

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(words.router, prefix="/words")

@app.get("/")
def root():
    return {"status": "ok"}
