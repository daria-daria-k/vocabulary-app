import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from app.database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    word_en = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    translations = relationship("Translation", back_populates="word", cascade="all, delete-orphan")
    examples = relationship("Example", back_populates="word", cascade="all, delete-orphan")
    progress = relationship("WordProgress", back_populates="word", uselist=False, cascade="all, delete-orphan")
