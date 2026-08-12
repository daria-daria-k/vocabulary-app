import { useState, type FormEvent } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useAuth } from "@/lib/auth"
import { ApiError } from "@/lib/api"
import { toast } from "sonner"
import { Eye, EyeOff, ArrowRight } from "lucide-react"
import { cn } from "@/lib/utils"

export function LoginPage() {
  const { login, register } = useAuth()
  const navigate = useNavigate()
  const [mode, setMode] = useState<"login" | "register">("login")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      if (mode === "login") await login(email, password)
      else await register(email, password)
      navigate("/")
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Что-то пошло не так")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-svh items-center justify-center bg-background p-4">
      <div className="w-full max-w-md overflow-hidden rounded-3xl border bg-card shadow-xl">
        {/* Баннер */}
        <div className="relative overflow-hidden bg-[linear-gradient(135deg,#40329e,#6554d9_60%,#8e70e7)] px-7 pb-9 pt-7 text-white">
          <div
            className="pointer-events-none absolute -right-16 -top-10 size-52 rounded-full border-[30px]"
            style={{ borderColor: "color-mix(in srgb, var(--coral) 70%, transparent)", transform: "rotate(-12deg)" }}
          />
          <div
            className="pointer-events-none absolute -bottom-10 -left-8 size-28 rounded-3xl"
            style={{ background: "color-mix(in srgb, var(--lime) 65%, transparent)", transform: "rotate(18deg)" }}
          />
          <div className="relative flex items-center gap-2.5 font-medium">
            <img src="/app-icon.png" alt="" className="size-9 rounded-xl object-cover" />
            Vocab
          </div>
          <h1 className="relative mt-6 text-3xl font-semibold leading-tight">
            Новые слова становятся частью вашей речи.
          </h1>
          <p className="relative mt-3 text-white/75">
            Сохраняйте, повторяйте и наблюдайте за прогрессом каждый день.
          </p>
        </div>

        {/* Форма */}
        <div className="p-7">
          <div className="mb-6 grid grid-cols-2 gap-1 rounded-xl bg-brand-soft/60 p-1">
            {(["login", "register"] as const).map((m) => (
              <button
                key={m}
                type="button"
                onClick={() => setMode(m)}
                className={cn(
                  "rounded-lg py-2 text-sm font-medium transition-colors",
                  mode === m
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "text-brand-dark hover:bg-brand-soft",
                )}
              >
                {m === "login" ? "Вход" : "Регистрация"}
              </button>
            ))}
          </div>

          <p className="text-xs font-medium uppercase tracking-wider text-brand">
            {mode === "login" ? "С возвращением" : "Приятно познакомиться"}
          </p>
          <h2 className="mt-1 text-2xl font-semibold tracking-tight">
            {mode === "login" ? "Продолжим обучение?" : "Создадим аккаунт?"}
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            {mode === "login"
              ? "Войдите, чтобы открыть свой словарь."
              : "Зарегистрируйтесь, чтобы начать."}
          </p>

          <form onSubmit={submit} className="mt-6 flex flex-col gap-4">
            <div className="flex flex-col gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="h-11"
              />
            </div>
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Пароль</Label>
                {mode === "login" && (
                  <button
                    type="button"
                    onClick={() => toast("Восстановление пароля — скоро")}
                    className="text-sm font-medium text-brand hover:underline"
                  >
                    Забыли пароль?
                  </button>
                )}
              </div>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Введите пароль"
                  className="h-11 pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((s) => !s)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  title={showPassword ? "Скрыть" : "Показать"}
                >
                  {showPassword ? <EyeOff className="size-4" /> : <Eye className="size-4" />}
                </button>
              </div>
            </div>
            <Button type="submit" className="mt-1 h-11" disabled={loading}>
              {loading ? "Подождите…" : mode === "login" ? "Войти" : "Зарегистрироваться"}
              {!loading && <ArrowRight className="size-4" />}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
