import { useCallback, useEffect, useState, type FormEvent } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { api, ApiError } from "@/lib/api"
import type { TrainingDirection, TrainingQuestion, TrainingResult } from "@/types"
import { toast } from "sonner"
import { Check, X, ArrowRight, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

export function TrainingPage() {
  const [direction, setDirection] = useState<TrainingDirection>("en_ru")
  const [question, setQuestion] = useState<TrainingQuestion | null>(null)
  const [answer, setAnswer] = useState("")
  const [result, setResult] = useState<TrainingResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [checking, setChecking] = useState(false)
  const [noWords, setNoWords] = useState(false)

  const loadNext = useCallback(async (dir: TrainingDirection) => {
    setLoading(true)
    setResult(null)
    setAnswer("")
    setNoWords(false)
    try {
      setQuestion(await api.trainingNext(dir))
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setNoWords(true)
        setQuestion(null)
      } else {
        toast.error(err instanceof ApiError ? err.message : "Ошибка загрузки")
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadNext(direction)
  }, [direction, loadNext])

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    if (!question || !answer.trim()) return
    setChecking(true)
    try {
      setResult(
        await api.trainingAnswer({ word_id: question.word_id, direction, answer }),
      )
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Ошибка проверки")
    } finally {
      setChecking(false)
    }
  }

  const promptLabel =
    direction === "en_ru" ? "Переведите на русский" : "Переведите на английский"

  return (
    <div className="flex flex-col gap-6">
      <div>
        <p className="text-xs font-medium uppercase tracking-wider text-brand">
          Ежедневная практика
        </p>
        <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">Тренировка</h1>
        <p className="mt-1 text-muted-foreground">
          Выберите направление и переведите слово.
        </p>
      </div>

      <Tabs value={direction} onValueChange={(v) => setDirection(v as TrainingDirection)}>
        <TabsList className="h-11 w-full rounded-xl p-1">
          <TabsTrigger value="en_ru" className="flex-1 rounded-lg">
            EN → RU
          </TabsTrigger>
          <TabsTrigger value="ru_en" className="flex-1 rounded-lg">
            RU → EN
          </TabsTrigger>
        </TabsList>
      </Tabs>

      {loading ? (
        <div className="flex justify-center py-20 text-muted-foreground">
          <Loader2 className="size-6 animate-spin" />
        </div>
      ) : noWords ? (
        <Card className="rounded-3xl py-16 text-center text-muted-foreground">
          Нет слов для тренировки.
          <br />
          Добавьте слова или смените статус с «Выучено».
        </Card>
      ) : question ? (
        <Card className="rounded-3xl p-8 sm:p-12">
          <div className="flex flex-col items-center gap-8">
            <div className="text-center">
              <p className="text-xs uppercase tracking-wider text-muted-foreground">
                {promptLabel}
              </p>
              <p className="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">
                {question.question}
              </p>
            </div>

            {result ? (
              <div className="flex w-full max-w-sm flex-col items-center gap-4">
                <div
                  className={cn(
                    "flex w-full items-center justify-center gap-2 rounded-2xl py-3 text-lg font-semibold",
                    result.correct
                      ? "bg-mint text-emerald-700 dark:text-emerald-200"
                      : "bg-coral/15 text-[#9a3b2a] dark:text-coral",
                  )}
                >
                  {result.correct ? (
                    <>
                      <Check className="size-5" /> Верно!
                    </>
                  ) : (
                    <>
                      <X className="size-5" /> Неверно
                    </>
                  )}
                </div>
                {!result.correct && (
                  <p className="text-center text-muted-foreground">
                    Правильный ответ:{" "}
                    <span className="font-medium text-foreground">{result.correct_answer}</span>
                  </p>
                )}
                <Button className="h-11 w-full" onClick={() => loadNext(direction)} autoFocus>
                  Следующее слово <ArrowRight className="size-4" />
                </Button>
              </div>
            ) : (
              <form onSubmit={submit} className="flex w-full max-w-sm flex-col gap-3">
                <Input
                  autoFocus
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  placeholder="Ваш ответ"
                  className="h-12 rounded-xl text-center text-lg"
                />
                <Button type="submit" className="h-11" disabled={checking || !answer.trim()}>
                  {checking ? <Loader2 className="size-4 animate-spin" /> : "Проверить"}
                </Button>
              </form>
            )}
          </div>
        </Card>
      ) : null}
    </div>
  )
}
