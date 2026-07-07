from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base

class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    translation_ru = Column(String, nullable=False)
    word = relationship("Word", back_populates="translations")
