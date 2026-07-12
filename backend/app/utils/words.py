from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User, Word


def get_owned_word_or_404(word_id: int, db: Session, current_user: User) -> Word:
    """Получить слово, если не найдено отдать 404"""
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id,
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Слово не найдено")
    return word