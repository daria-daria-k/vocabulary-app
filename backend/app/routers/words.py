from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

from app.schemas.word import WordCreate, WordUpdate, WordResponse
from app.models.word import Word
from app.models.translation import Translation
from app.models.example import Example

from app.utils.security import get_current_user

router = APIRouter()


@router.post("", response_model=WordResponse)
def add(word_data: WordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_word = Word(
        user_id=current_user.id,
        word_en=word_data.word_en,
        translations=[Translation(translation_ru=t.translation_ru) for t in word_data.translations],
        examples=[Example(sentence=ex.sentence) for ex in word_data.examples],
    )

    db.add(new_word)
    db.commit()
    db.refresh(new_word)

    return new_word


@router.get("", response_model=list[WordResponse])
def get(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    words = db.query(Word).filter(Word.user_id == current_user.id).all()

    return words


@router.get("/{word_id}", response_model=WordResponse)
def get_one(word_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = db.query(Word).filter(Word.id == word_id, Word.user_id == current_user.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Слово не найдено")

    return word


@router.put("/{word_id}", response_model=WordResponse)
def update(word_id: int, word_data: WordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = db.query(Word).filter(Word.id == word_id, Word.user_id == current_user.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Слово не найдено")

    word.word_en = word_data.word_en
    word.translations = [Translation(translation_ru=t.translation_ru) for t in word_data.translations]
    word.examples = [Example(sentence=ex.sentence) for ex in word_data.examples]

    db.commit()
    db.refresh(word)

    return word


@router.delete("/{word_id}", status_code=204)
def delete(word_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = db.query(Word).filter(Word.id == word_id, Word.user_id == current_user.id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Слово не найдено")

    db.delete(word)
    db.commit()



