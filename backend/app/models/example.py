from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base

class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)
    sentence = Column(String, nullable=False)
    word = relationship("Word", back_populates="examples")