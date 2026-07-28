from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.user import UserCreate, UserResponse, UserLogin
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    too_many_attempts,
    register_attempt
)

from redis import Redis
from app.redis_client import get_redis

import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

MAX_ATTEMPTS_EMAIL = int(os.getenv("MAX_ATTEMPTS_EMAIL", 5))
MAX_ATTEMPTS_IP = int(os.getenv("MAX_ATTEMPTS_IP", 20))
WINDOW_SECONDS = int(os.getenv("WINDOW_SECONDS", 900))


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_is_exist = db.query(User).filter(User.email == user_data.email).first()
    if user_is_exist:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(
        email=user_data.email.lower().strip(),
        password_hash=hash_password(user_data.password),
        streak=0,
        daily_goal=10
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user_data: UserLogin, request: Request, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    ip = request.client.host
    email = user_data.email.lower().strip()

    ip_key = f"login_attempts:ip:{ip}"
    email_key = f"login_attempts:email:{email}"

    if too_many_attempts(redis, ip_key, MAX_ATTEMPTS_IP) or too_many_attempts(redis, email_key, MAX_ATTEMPTS_EMAIL):
        raise HTTPException(status_code=429, detail="Слишком много попыток. Попробуйте позже")

    user = db.query(User).filter(User.email == user_data.email.lower().strip()).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        register_attempt(redis, ip_key, WINDOW_SECONDS)
        register_attempt(redis, email_key, WINDOW_SECONDS)
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    redis.delete(ip_key, email_key)

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
