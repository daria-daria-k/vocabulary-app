import type {
  Word,
  WordStatus,
  WordCreateInput,
  TrainingDirection,
  TrainingQuestion,
  TrainingResult,
} from "@/types"

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

let onUnauthorized: (() => void) | null = null
export function setUnauthorizedHandler(handler: () => void) {
  onUnauthorized = handler
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem("token")
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  }
  if (token) headers["Authorization"] = `Bearer ${token}`

  const res = await fetch(`${API_URL}${path}`, { ...options, headers })

  if (res.status === 401 && onUnauthorized) {
    onUnauthorized()
  }

  if (!res.ok) {
    let detail = "Что-то пошло не так"
    try {
      const data = await res.json()
      if (typeof data.detail === "string") detail = data.detail
      else if (Array.isArray(data.detail)) detail = "Проверьте правильность данных"
    } catch {
      /* тело не JSON — оставляем дефолт */
    }
    throw new ApiError(res.status, detail)
  }

  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  register: (email: string, password: string) =>
    request<{ id: number; email: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  login: (email: string, password: string) =>
    request<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  getWords: () => request<Word[]>("/words"),

  createWord: (data: WordCreateInput) =>
    request<Word>("/words", { method: "POST", body: JSON.stringify(data) }),

  deleteWord: (id: number) =>
    request<void>(`/words/${id}`, { method: "DELETE" }),

  setStatus: (id: number, status: WordStatus) =>
    request<Word>(`/words/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),

  trainingNext: (direction: TrainingDirection) =>
    request<TrainingQuestion>(`/training/next?direction=${direction}`),

  trainingAnswer: (data: {
    word_id: number
    direction: TrainingDirection
    answer: string
  }) =>
    request<TrainingResult>("/training/answer", {
      method: "POST",
      body: JSON.stringify(data),
    }),
}
