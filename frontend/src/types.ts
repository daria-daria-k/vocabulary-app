export type WordStatus = "new" | "learning" | "learned"

export interface Translation {
  id: number
  translation_ru: string
}

export interface Example {
  id: number
  sentence: string
}

export interface Word {
  id: number
  word_en: string
  translations: Translation[]
  examples: Example[]
  progress: { status: WordStatus }
}

export type TrainingDirection = "en_ru" | "ru_en"

export interface TrainingQuestion {
  word_id: number
  direction: TrainingDirection
  question: string
}

export interface TrainingResult {
  correct: boolean
  correct_answer: string
}

export interface WordCreateInput {
  word_en: string
  translations: { translation_ru: string }[]
  examples: { sentence: string }[]
}
