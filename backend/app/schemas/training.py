from pydantic import BaseModel, field_validator
import enum

class TrainingDirection(str, enum.Enum):
    en_ru = "en_ru"
    ru_en = "ru_en"


class TrainingQuestion(BaseModel):
    word_id: int
    direction: TrainingDirection
    question: str


class TrainingAnswer(BaseModel):
    word_id: int
    direction: TrainingDirection
    answer: str

    @field_validator("answer")
    @classmethod
    def answer_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Ответ не может быть пустым")
        return v


class TrainingResult(BaseModel):
    correct: bool
    correct_answer: str