from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, words, training

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(words.router, prefix="/words")
app.include_router(training.router, prefix="/training")

@app.get("/")
def root():
    return {"status": "ok"}
