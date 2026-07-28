import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import { useState } from "react";
import { ArrowRight, ShieldCheck } from "lucide-react";

export const Route = createFileRoute("/admin/login")({
  component: AdminLogin,
  head: () => ({
    meta: [
      { title: "Admin Login — Blueteamers Arena" },
      { name: "description", content: "Secure admin portal for Blueteamers Arena event administrators." },
      { property: "og:title", content: "Admin Login — Blueteamers Arena" },
      { property: "og:description", content: "Secure admin portal for Blueteamers Arena event administrators." },
    ],
  }),
});

function AdminLogin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate({ to: "/admin/dashboard" });
  };

  return (
    <main className="min-h-screen bg-background">
      <header className="border-b border-border/60">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <Link to="/" className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg border border-border bg-card">
              <span className="text-lg font-bold text-primary">B</span>
            </div>
            <div className="leading-tight">
              <div className="text-sm font-bold tracking-wide">BLUETEAMERS</div>
              <div className="text-xs font-semibold tracking-widest text-primary">ARENA</div>
            </div>
          </Link>
          <div className="flex items-center gap-4">
            <Link to="/" className="text-xs font-medium text-muted-foreground hover:text-foreground">
              Back to Home
            </Link>
            <span className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3 py-1.5 text-xs font-medium text-muted-foreground">
              <ShieldCheck className="h-3.5 w-3.5 text-primary" />
              Admin Portal
            </span>
          </div>
        </nav>
      </header>

      <div className="mx-auto flex max-w-7xl items-center justify-center px-6 py-16">
        <div className="w-full max-w-md rounded-xl border border-border bg-card p-8 shadow-2xl shadow-black/40">
          <div className="flex flex-col items-center">
            <div className="grid h-12 w-12 place-items-center rounded-lg border border-border bg-[var(--surface)]">
              <ShieldCheck className="h-6 w-6 text-primary" />
            </div>
            <h1 className="mt-4 text-center text-2xl font-bold">Blueteamers Arena</h1>
            <p className="mt-1 text-center text-sm text-muted-foreground">Admin Portal</p>
          </div>

          <form onSubmit={submit} className="mt-8 space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-muted-foreground">Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@blueteamers.io"
                required
                className="w-full rounded-lg border border-border bg-[var(--surface)] px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none"
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-muted-foreground">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full rounded-lg border border-border bg-[var(--surface)] px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none"
              />
            </div>

            <button
              type="submit"
              className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-[var(--primary-hover)]"
            >
              Login <ArrowRight className="h-4 w-4" />
            </button>

            <button
              type="button"
              className="w-full text-center text-xs font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              Forgot Password?
            </button>
          </form>

          <p className="mt-8 border-t border-border/60 pt-4 text-center text-xs text-muted-foreground">
            Only authorized event administrators can access this portal.
          </p>
        </div>
      </div>
    </main>
  );
}
