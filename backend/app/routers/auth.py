from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse, UserLogin
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_is_exist = db.query(User).filter(User.email == user_data.email).first()
    if user_is_exist:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        streak=0,
        daily_goal=10
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    access_token = create_access_token(data={"sub": str(user.id)})

    return{"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user