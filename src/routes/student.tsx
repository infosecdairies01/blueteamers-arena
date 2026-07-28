import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { User, Mail, Lock } from "lucide-react";
import { ACCENT_CLASSES, getSelectedEvent, saveStudentName, type Accent } from "@/lib/mock-events";

export const Route = createFileRoute("/student")({
  component: Student,
  head: () => ({
    meta: [
      { title: "Student Details — Blueteamers Arena" },
      { name: "description", content: "Enter your details to enter the arena." },
      { property: "og:title", content: "Student Details — Blueteamers Arena" },
      { property: "og:description", content: "Enter your details to enter the arena." },
    ],
  }),
});

function Student() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [accentKey, setAccentKey] = useState<Accent>("blue");
  useEffect(() => setAccentKey(getSelectedEvent().accent), []);
  const accent = ACCENT_CLASSES[accentKey];

  return (
    <main className="min-h-screen bg-background">
      <header className="border-b border-border/60">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <Link to="/" className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg border border-border bg-card">
              <span className={`text-lg font-bold ${accent.text}`}>B</span>
            </div>
            <div className="leading-tight">
              <div className="text-sm font-bold tracking-wide">BLUETEAMERS</div>
              <div className={`text-xs font-semibold tracking-widest ${accent.text}`}>ARENA</div>
            </div>
          </Link>
          <div className="flex items-center gap-6">
            <Link to="/" className="text-sm font-medium text-muted-foreground hover:text-foreground">Back to Home</Link>
            <Link to="/about" className="text-sm font-medium text-muted-foreground hover:text-foreground">About Us</Link>
          </div>
        </nav>
      </header>

      <div className="mx-auto flex max-w-md flex-col px-6 py-16">
        <div className="rounded-xl border border-border bg-card p-8 shadow-2xl shadow-black/40">
          <h1 className="text-center text-2xl font-bold">Almost There!</h1>
          <p className="mt-2 text-center text-sm text-muted-foreground">
            Enter your details to enter the arena.
          </p>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (name.trim()) saveStudentName(name.trim().split(/\s+/)[0]);
              navigate({ to: "/dashboard" });
            }}
            className="mt-6 space-y-4"
          >
            <div className="relative">
              <User className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Full Name"
                className="w-full rounded-lg border border-border bg-[var(--surface)] py-3 pl-10 pr-3 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none"
              />
            </div>
            <div className="relative">
              <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="College Email ID"
                className="w-full rounded-lg border border-border bg-[var(--surface)] py-3 pl-10 pr-3 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none"
              />
            </div>
            <button
              type="submit"
              className={`w-full rounded-lg ${accent.bg} ${accent.hover} px-5 py-3 text-sm font-semibold text-white transition-colors`}
            >
              Enter Arena
            </button>
          </form>
          <p className="mt-6 flex items-center justify-center gap-2 text-xs text-muted-foreground">
            <Lock className="h-3 w-3" />
            Your details are secure and will only be used for this event.
          </p>
        </div>
      </div>
    </main>
  );
}
