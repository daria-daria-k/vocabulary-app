from pydantic import BaseModel, ConfigDict, Field

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
    translations: list[TranslationCreate] = Field(min_length=1)
    examples: list[ExampleCreate] = Field(default_factory=list)

class WordUpdate(BaseModel):
    word_en: str
    translations: list[TranslationCreate] = Field(min_length=1)
    examples: list[ExampleCreate] = Field(default_factory=list)


class WordStatusUpdate(BaseModel):
    status: WordStatus


class WordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word_en: str
    translations: list[TranslationResponse]
    examples: list[ExampleResponse]
    progress: WordProgressResponse
