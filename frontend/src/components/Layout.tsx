import { NavLink, Outlet, useNavigate } from "react-router-dom"
import { useAuth } from "@/lib/auth"
import { cn } from "@/lib/utils"

export function Layout() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate("/login")
  }

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    cn(
      "px-3 py-2 rounded-lg text-sm font-medium transition-colors",
      isActive
        ? "bg-brand-soft text-brand-dark"
        : "text-muted-foreground hover:text-brand-dark hover:bg-brand-soft/60",
    )

  return (
    <div className="min-h-svh bg-background">
      <header className="sticky top-0 z-10 border-b bg-card/90 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6">
          <NavLink to="/" className="flex items-center gap-2.5 font-medium">
            <img
              src="/app-icon.png"
              alt=""
              className="size-9 rounded-xl object-cover shadow-[0_8px_20px_rgba(101,84,217,0.25)]"
            />
            Vocab
          </NavLink>

          <nav className="flex items-center gap-1">
            <NavLink to="/" className={linkClass} end>
              Обзор
            </NavLink>
            <NavLink to="/words" className={linkClass}>
              Слова
            </NavLink>
            <NavLink to="/training" className={linkClass}>
              Тренировка
            </NavLink>
          </nav>

          <button
            onClick={handleLogout}
            title="Выйти из аккаунта"
            className="grid size-9 place-items-center rounded-full bg-lime font-medium text-[#353b18] transition-transform hover:scale-105"
          >
            Д
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
        <Outlet />
      </main>
    </div>
  )
}
