from fastapi import FastAPI
from app.routers import auth, words, training

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(words.router, prefix="/words")
app.include_router(training.router, prefix="/training")

@app.get("/")
def root():
    return {"status": "ok"}
