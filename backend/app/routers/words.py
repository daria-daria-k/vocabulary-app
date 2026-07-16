from fastapi import APIRouter, Depends
import json

from redis import Redis
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, WordProgress
from app.models.word_progress import WordStatus

from app.schemas.word import WordCreate, WordUpdate, WordResponse, WordStatusUpdate
from app.models.word import Word
from app.models.translation import Translation
from app.models.example import Example

from app.utils.security import get_current_user
from app.utils.words import get_owned_word_or_404, words_cache_key

from app.redis_client import get_redis

router = APIRouter()


@router.post("", response_model=WordResponse)
def add(word_data: WordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), redis: Redis = Depends(get_redis)):
    new_word = Word(
        user_id=current_user.id,
        word_en=word_data.word_en,
        translations=[Translation(translation_ru=t.translation_ru) for t in word_data.translations],
        examples=[Example(sentence=ex.sentence) for ex in word_data.examples],
        progress=WordProgress(status=WordStatus.new)
    )

    db.add(new_word)
    db.commit()
    redis.delete(words_cache_key(current_user.id))
    db.refresh(new_word)

    return new_word


@router.get("", response_model=list[WordResponse])
def get(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), redis: Redis = Depends(get_redis)):

    cached = redis.get(words_cache_key(current_user.id))
    if cached is not None:
        return json.loads(cached)

    words = db.query(Word).filter(Word.user_id == current_user.id).all()

    data = [WordResponse.model_validate(w).model_dump(mode="json") for w in words]
    redis.set(words_cache_key(current_user.id), json.dumps(data, ensure_ascii=False), ex=60 * 90)

    return data


@router.get("/{word_id}", response_model=WordResponse)
def get_one(word_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    word = get_owned_word_or_404(word_id, db, current_user)

    return word


@router.put("/{word_id}", response_model=WordResponse)
def update(word_id: int, word_data: WordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), redis: Redis = Depends(get_redis)):
    word = get_owned_word_or_404(word_id, db, current_user)

    word.word_en = word_data.word_en
    word.translations = [Translation(translation_ru=t.translation_ru) for t in word_data.translations]
    word.examples = [Example(sentence=ex.sentence) for ex in word_data.examples]

    db.commit()
    redis.delete(words_cache_key(current_user.id))
    db.refresh(word)

    return word

@router.patch("/{word_id}/status", response_model=WordResponse)
def update_status(word_id: int, status_data: WordStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), redis: Redis = Depends(get_redis)):
    word = get_owned_word_or_404(word_id, db, current_user)

    word.progress.status = status_data.status
    db.commit()
    redis.delete(words_cache_key(current_user.id))
    db.refresh(word)

    return word


@router.delete("/{word_id}", status_code=204)
def delete(word_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), redis: Redis = Depends(get_redis)):
    word = get_owned_word_or_404(word_id, db, current_user)

    db.delete(word)
    db.commit()
    redis.delete(words_cache_key(current_user.id))



