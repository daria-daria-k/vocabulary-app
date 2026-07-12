from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Word, WordProgress
from app.models.word_progress import WordStatus
from app.schemas.training import TrainingQuestion, TrainingDirection, TrainingResult, TrainingAnswer

from app.utils.security import get_current_user
from app.utils.text import normalize
from app.utils.words import get_owned_word_or_404

router = APIRouter()


@router.get("/next", response_model=TrainingQuestion)
def get_next(
        direction: TrainingDirection,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    word = (
        db.query(Word)
        .join(WordProgress)
        .filter(
            Word.user_id == current_user.id,
            WordProgress.status != WordStatus.learned
        )
        .order_by(func.random())
        .first()
    )

    if not word:
        raise HTTPException(status_code=404, detail="Нет слов для тренировки")

    if direction == TrainingDirection.en_ru:
        question = word.word_en
    else:
        question = word.translations[0].translation_ru

    return TrainingQuestion(word_id=word.id, direction=direction, question=question)


@router.post("/answer", response_model=TrainingResult)
def check_answer(
        answer_data: TrainingAnswer,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    word = get_owned_word_or_404(answer_data.word_id, db, current_user)

    if answer_data.direction == TrainingDirection.ru_en:
        correct_answer = word.word_en
        is_correct = normalize(answer_data.answer) == normalize(correct_answer)
    else:
        correct_answer = ", ".join(t.translation_ru for t in word.translations)
        is_correct = any(
            normalize(answer_data.answer) == normalize(t.translation_ru)
            for t in word.translations
        )

    if is_correct:
        word.progress.correct_count += 1
    else:
        word.progress.wrong_count += 1

    db.commit()

    return TrainingResult(
        correct=is_correct,
        correct_answer=correct_answer
    )
