from pydantic import BaseModel, ConfigDict

from app.models.word_progress import WordStatus


class TranslationCreate(BaseModel):
    translation_ru: str

class ExampleCreate(BaseModel):
    sentence: str


class TranslationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    translation_ru: str
    id: int

class ExampleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    sentence: str
    id: int

class WordProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: WordStatus

class WordCreate(BaseModel):
    word_en: str
    translations: list[TranslationCreate]
    examples: list[ExampleCreate]

class WordUpdate(BaseModel):
    word_en: str
    translations: list[TranslationCreate]
    examples: list[ExampleCreate]


class WordStatusUpdate(BaseModel):
    status: WordStatus


class WordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word_en: str
    translations: list[TranslationResponse]
    examples: list[ExampleResponse]
    progress: WordProgressResponse
