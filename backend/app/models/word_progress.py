from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base

import enum

class WordStatus(str, enum.Enum):
    new = "new"
    learning = "learning"
    learned = "learned"


class WordProgress(Base):
    __tablename__ = "word_progress"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, unique=True)
    interval = Column(Integer, nullable=False, default=0)
    ease_factor = Column(Float, nullable=False, default=2.5)
    correct_count = Column(Integer, nullable=False, default=0)
    wrong_count = Column(Integer, nullable=False, default=0)
    word = relationship("Word", back_populates="progress")
    next_review_at = Column(DateTime, nullable=True)
    status = Column(Enum(WordStatus), nullable=False, default=WordStatus.new)


