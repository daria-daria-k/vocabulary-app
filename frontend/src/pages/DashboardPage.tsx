import { useEffect, useMemo, useState } from "react"
import { Link } from "react-router-dom"
import { Card } from "@/components/ui/card"
import { api, ApiError } from "@/lib/api"
import type { Word } from "@/types"
import { toast } from "sonner"
import { Plus, Play, ArrowRight, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

function greeting() {
  const h = new Date().getHours()
  if (h < 6) return "Доброй ночи"
  if (h < 12) return "Доброе утро"
  if (h < 18) return "Добрый день"
  return "Добрый вечер"
}

const dateLabel = new Intl.DateTimeFormat("ru-RU", {
  weekday: "long",
  day: "numeric",
  month: "long",
}).format(new Date())

export function DashboardPage() {
  const [words, setWords] = useState<Word[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .getWords()
      .then(setWords)
      .catch((err) =>
        toast.error(err instanceof ApiError ? err.message : "Ошибка загрузки"),
      )
      .finally(() => setLoading(false))
  }, [])

  const stats = useMemo(() => {
    const total = words.length
    const learned = words.filter((w) => w.progress.status === "learned").length
    const learning = words.filter((w) => w.progress.status === "learning").length
    const fresh = words.filter((w) => w.progress.status === "new").length
    const toPractice = total - learned
    const pct = total ? Math.round((learned / total) * 100) : 0
    return { total, learned, learning, fresh, toPractice, pct }
  }, [words])

  const continueWords = words
    .filter((w) => w.progress.status !== "learned")
    .slice(0, 4)

  if (loading) {
    return (
      <div className="flex justify-center py-24 text-muted-foreground">
        <Loader2 className="size-6 animate-spin" />
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Заголовок + быстрые действия */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-brand">
            {dateLabel}
          </p>
          <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">
            {greeting()}
          </h1>
          <p className="mt-1 text-muted-foreground">
            {stats.toPractice > 0
              ? "Немного практики — и слова закрепятся."
              : "Всё повторено. Можно добавить новые слова."}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            to="/words"
            className="inline-flex items-center gap-2 rounded-xl border bg-card px-3.5 py-2.5 text-sm font-medium transition-all hover:-translate-y-0.5 hover:border-brand hover:bg-brand-soft"
          >
            <span className="grid size-5 place-items-center rounded-md bg-brand-soft text-brand-dark">
              <Plus className="size-3.5" />
            </span>
            Добавить слово
          </Link>
          <Link
            to="/training"
            className="inline-flex items-center gap-2 rounded-xl bg-primary px-3.5 py-2.5 text-sm font-medium text-primary-foreground transition-all hover:-translate-y-0.5 hover:bg-brand-dark"
          >
            <span className="grid size-5 place-items-center rounded-md bg-white text-brand-dark">
              <Play className="size-3 fill-current" />
            </span>
            Начать тренировку
          </Link>
        </div>
      </div>

      {/* Герой: план + прогресс */}
      <div className="grid gap-4 lg:grid-cols-[1.35fr_0.85fr]">
        <div className="relative flex min-h-56 flex-col justify-between overflow-hidden rounded-3xl bg-[linear-gradient(135deg,#40329e,#6554d9_58%,#8e70e7)] p-6 text-white">
          <div
            className="pointer-events-none absolute -right-14 -top-16 size-44 rounded-full border-[34px]"
            style={{ borderColor: "color-mix(in srgb, var(--coral) 76%, transparent)", transform: "rotate(-18deg)" }}
          />
          <div>
            <p className="text-xs uppercase tracking-wider text-white/70">
              План на сегодня
            </p>
            <h2 className="mt-2 text-2xl font-semibold">
              {stats.toPractice > 0
                ? `Повторить ${stats.toPractice} ${plural(stats.toPractice)}`
                : "Слова на сегодня закрыты"}
            </h2>
            {stats.toPractice > 0 && (
              <p className="mt-1 text-white/80">
                Около {Math.max(1, Math.round(stats.toPractice * 0.4))} мин · EN → RU
              </p>
            )}
          </div>
          <Link
            to="/training"
            className="z-10 inline-flex w-fit items-center gap-1.5 rounded-xl bg-lime px-3.5 py-2.5 text-sm font-semibold text-[#292d13] transition-transform hover:-translate-y-0.5"
          >
            {stats.toPractice > 0 ? "Начать сейчас" : "Повторить всё"} <ArrowRight className="size-4" />
          </Link>
        </div>

        <Card className="grid content-center gap-4 rounded-3xl p-6">
          <div className="flex items-center gap-4">
            <div
              className="relative grid size-20 shrink-0 place-items-center rounded-full"
              style={{
                background: `conic-gradient(var(--coral) 0 ${stats.pct}%, var(--brand-soft) ${stats.pct}% 100%)`,
              }}
            >
              <div className="absolute inset-[9px] rounded-full bg-card" />
              <strong className="relative text-lg">{stats.pct}%</strong>
            </div>
            <div>
              <h3 className="font-semibold">Общий прогресс</h3>
              <p className="text-sm text-muted-foreground">
                {stats.learned} из {stats.total} слов выучено
              </p>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-1.5">
            <Stat n={stats.fresh} label="новых" className="bg-brand-soft" />
            <Stat
              n={stats.learning}
              label="учу"
              style={{ background: "color-mix(in srgb, var(--coral) 18%, var(--card))" }}
            />
            <Stat n={stats.learned} label="знаю" className="bg-mint" />
          </div>
        </Card>
      </div>

      {/* Продолжить изучение */}
      <Card className="rounded-2xl p-5">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="font-semibold">Продолжить изучение</h3>
          <Link
            to="/words"
            className="rounded-full bg-brand-soft px-3 py-1.5 text-xs font-medium text-brand-dark transition-colors hover:bg-brand hover:text-white"
          >
            Все слова →
          </Link>
        </div>
        {continueWords.length === 0 ? (
          <p className="py-4 text-center text-sm text-muted-foreground">
            {stats.total === 0
              ? "Пока нет слов — добавьте первое на странице «Слова»."
              : "Все слова выучены 🎉"}
          </p>
        ) : (
          <div className="flex flex-col">
            {continueWords.map((w) => (
              <Link
                key={w.id}
                to="/training"
                className="flex items-center justify-between rounded-lg border-b px-2 py-2.5 transition-all last:border-0 hover:translate-x-0.5 hover:bg-brand-soft"
              >
                <span>
                  <strong>{w.word_en}</strong>
                  <br />
                  <small className="text-muted-foreground">
                    {w.translations.map((t) => t.translation_ru).join(", ")}
                  </small>
                </span>
                <span className="rounded-full bg-brand-soft px-2.5 py-1 text-xs text-brand-dark">
                  {w.progress.status === "new" ? "новое" : "учу"}
                </span>
              </Link>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}

function Stat({
  n,
  label,
  className,
  style,
}: {
  n: number
  label: string
  className?: string
  style?: React.CSSProperties
}) {
  return (
    <div className={cn("rounded-xl px-2 py-2.5 text-center", className)} style={style}>
      <strong className="block">{n}</strong>
      <span className="text-[11px] text-muted-foreground">{label}</span>
    </div>
  )
}

function plural(n: number) {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return "слово"
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return "слова"
  return "слов"
}
