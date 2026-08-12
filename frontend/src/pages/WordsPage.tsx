import { useEffect, useMemo, useState, type FormEvent } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card } from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { api, ApiError } from "@/lib/api"
import type { Word, WordStatus } from "@/types"
import { toast } from "sonner"
import { Plus, Trash2, Loader2, Search, Upload, Languages } from "lucide-react"
import { cn } from "@/lib/utils"

type Filter = "all" | WordStatus

const STATUS_TAG: Record<WordStatus, { label: string; className: string }> = {
  new: { label: "новое", className: "bg-brand-soft text-brand-dark" },
  learning: {
    label: "учу",
    className: "bg-coral/15 text-[#9a3b2a] dark:text-coral",
  },
  learned: { label: "знаю", className: "bg-mint text-emerald-800 dark:text-emerald-200" },
}

export function WordsPage() {
  const [words, setWords] = useState<Word[]>([])
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)
  const [showForm, setShowForm] = useState(false)

  const [wordEn, setWordEn] = useState("")
  const [translations, setTranslations] = useState("")
  const [example, setExample] = useState("")

  const [query, setQuery] = useState("")
  const [filter, setFilter] = useState<Filter>("all")

  const load = async () => {
    try {
      setWords(await api.getWords())
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Не удалось загрузить слова")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const stats = useMemo(
    () => ({
      total: words.length,
      new: words.filter((w) => w.progress.status === "new").length,
      learning: words.filter((w) => w.progress.status === "learning").length,
      learned: words.filter((w) => w.progress.status === "learned").length,
    }),
    [words],
  )

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase()
    return words.filter((w) => {
      if (filter !== "all" && w.progress.status !== filter) return false
      if (!q) return true
      return (
        w.word_en.toLowerCase().includes(q) ||
        w.translations.some((t) => t.translation_ru.toLowerCase().includes(q))
      )
    })
  }, [words, query, filter])

  const addWord = async (e: FormEvent) => {
    e.preventDefault()
    const parsed = translations
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean)
    if (parsed.length === 0) {
      toast.error("Добавьте хотя бы один перевод")
      return
    }
    setAdding(true)
    try {
      await api.createWord({
        word_en: wordEn.trim(),
        translations: parsed.map((t) => ({ translation_ru: t })),
        examples: example.trim() ? [{ sentence: example.trim() }] : [],
      })
      setWordEn("")
      setTranslations("")
      setExample("")
      setShowForm(false)
      toast.success("Слово добавлено")
      load()
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Не удалось добавить")
    } finally {
      setAdding(false)
    }
  }

  const remove = async (id: number) => {
    try {
      await api.deleteWord(id)
      setWords((prev) => prev.filter((w) => w.id !== id))
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Не удалось удалить")
    }
  }

  const changeStatus = async (id: number, status: WordStatus) => {
    try {
      const updated = await api.setStatus(id, status)
      setWords((prev) => prev.map((w) => (w.id === id ? updated : w)))
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Не удалось обновить статус")
    }
  }

  const filters: { key: Filter; label: string }[] = [
    { key: "all", label: "Все" },
    { key: "new", label: "Новые" },
    { key: "learning", label: "Учу" },
    { key: "learned", label: "Выучено" },
  ]

  return (
    <div className="flex flex-col gap-6">
      {/* Заголовок + действия */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-brand">
            Моя коллекция
          </p>
          <h1 className="mt-1.5 text-3xl font-semibold tracking-tight">Словарь</h1>
          <p className="mt-1 max-w-sm text-muted-foreground">
            Сохраняйте слова и наблюдайте, как они становятся знакомыми.
          </p>
        </div>
        <div className="flex flex-col gap-2">
          <Button className="h-11" onClick={() => setShowForm((s) => !s)}>
            <Plus className="size-4" /> Добавить слово
          </Button>
          <Button
            variant="outline"
            className="h-11"
            onClick={() => toast("Импорт из файла — скоро")}
          >
            <Upload className="size-4" /> Загрузить из файла
          </Button>
        </div>
      </div>

      {/* Статистика */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <StatCard n={stats.total} label="всего слов" />
        <StatCard n={stats.new} label="новых" />
        <StatCard n={stats.learning} label="в изучении" className="bg-brand-soft" />
        <StatCard n={stats.learned} label="выучено" className="bg-mint" />
      </div>

      {/* Форма добавления (по кнопке) */}
      {showForm && (
        <Card className="rounded-2xl p-5">
          <form onSubmit={addWord} className="flex flex-col gap-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="flex flex-col gap-2">
                <Label htmlFor="word_en">Слово (EN)</Label>
                <Input id="word_en" required value={wordEn} onChange={(e) => setWordEn(e.target.value)} placeholder="apple" />
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="translations">Переводы (через запятую)</Label>
                <Input id="translations" required value={translations} onChange={(e) => setTranslations(e.target.value)} placeholder="яблоко, яблоня" />
              </div>
            </div>
            <div className="flex flex-col gap-2">
              <Label htmlFor="example">Пример (необязательно)</Label>
              <Input id="example" value={example} onChange={(e) => setExample(e.target.value)} placeholder="I ate an apple." />
            </div>
            <Button type="submit" className="self-start" disabled={adding}>
              {adding ? <Loader2 className="size-4 animate-spin" /> : <Plus className="size-4" />}
              Сохранить
            </Button>
          </form>
        </Card>
      )}

      {/* Поиск + фильтры */}
      <div className="flex flex-col gap-3">
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Найти слово или перевод"
            className="h-12 rounded-2xl pl-10"
          />
        </div>
        <div className="flex flex-wrap gap-2">
          {filters.map((f) => (
            <button
              key={f.key}
              onClick={() => setFilter(f.key)}
              className={cn(
                "rounded-full px-4 py-2 text-sm font-medium transition-colors",
                filter === f.key
                  ? "bg-brand-soft text-brand-dark"
                  : "border bg-card text-muted-foreground hover:bg-brand-soft/50",
              )}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Список */}
      {loading ? (
        <div className="flex justify-center py-12 text-muted-foreground">
          <Loader2 className="size-6 animate-spin" />
        </div>
      ) : visible.length === 0 ? (
        <p className="py-10 text-center text-sm text-muted-foreground">
          {words.length === 0 ? "Пока нет слов — добавьте первое." : "Ничего не найдено."}
        </p>
      ) : (
        <div className="flex flex-col gap-3">
          {visible.map((word) => {
            const tag = STATUS_TAG[word.progress.status]
            return (
              <Card key={word.id} className="rounded-2xl p-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="grid size-7 shrink-0 place-items-center rounded-lg bg-brand-soft text-brand-dark">
                        <Languages className="size-4" />
                      </span>
                      <span className="text-lg font-semibold">{word.word_en}</span>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {word.translations.map((t) => (
                        <span key={t.id} className="rounded-lg bg-brand-soft px-2.5 py-1 text-sm text-brand-dark">
                          {t.translation_ru}
                        </span>
                      ))}
                    </div>
                    {word.examples.length > 0 && (
                      <p className="mt-2 text-sm italic text-muted-foreground">
                        {word.examples[0].sentence}
                      </p>
                    )}
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    <span className={cn("rounded-full px-2.5 py-1 text-xs font-medium", tag.className)}>
                      {tag.label}
                    </span>
                    <Select value={word.progress.status} onValueChange={(v) => changeStatus(word.id, v as WordStatus)}>
                      <SelectTrigger size="sm" className="w-[116px]">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="new">Новое</SelectItem>
                        <SelectItem value="learning">Учу</SelectItem>
                        <SelectItem value="learned">Выучено</SelectItem>
                      </SelectContent>
                    </Select>
                    <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-destructive" onClick={() => remove(word.id)}>
                      <Trash2 className="size-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}

function StatCard({ n, label, className }: { n: number; label: string; className?: string }) {
  return (
    <Card className={cn("rounded-2xl p-4", className)}>
      <div className="text-2xl font-semibold">{n}</div>
      <div className="text-sm text-muted-foreground">{label}</div>
    </Card>
  )
}
