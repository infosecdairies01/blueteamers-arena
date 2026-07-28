import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { EVENTS, saveSelectedEvent } from "@/lib/mock-events";

export const Route = createFileRoute("/arena")({
  component: Arena,
  head: () => ({
    meta: [
      { title: "Enter Event Code — Blueteamers Arena" },
      { name: "description", content: "Enter your event code to join the Blueteamers Arena workshop." },
      { property: "og:title", content: "Enter Event Code — Blueteamers Arena" },
      { property: "og:description", content: "Enter your event code to join the Blueteamers Arena workshop." },
    ],
  }),
});

function Shell({ children }: { children: React.ReactNode }) {
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
          <Link to="/" className="text-sm font-medium text-muted-foreground hover:text-foreground">
            Back to Home
          </Link>
        </nav>
      </header>
      <div className="mx-auto flex max-w-7xl items-center justify-center px-6 py-16">
        {children}
      </div>
    </main>
  );
}

function Arena() {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const key = code.trim().toUpperCase();
    if (EVENTS[key]) {
      saveSelectedEvent(key);
      navigate({ to: "/event" });
    } else {
      setError("Invalid Event Code");
    }
  };

  return (
    <Shell>
      <div className="w-full max-w-md rounded-xl border border-border bg-card p-8 shadow-2xl shadow-black/40">
        <h1 className="text-center text-2xl font-bold">Enter Event Code</h1>
        <p className="mt-2 text-center text-sm text-muted-foreground">
          Enter the event code provided by your college
        </p>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <input
            value={code}
            onChange={(e) => {
              setCode(e.target.value);
              setError("");
            }}
            placeholder="Event Code"
            className="w-full rounded-lg border border-border bg-[var(--surface)] px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none"
          />
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button
            type="submit"
            className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-[var(--primary-hover)]"
          >
            Continue <ArrowRight className="h-4 w-4" />
          </button>
        </form>
        <p className="mt-6 text-center text-xs text-muted-foreground">
          Don't have a code? Contact your college coordinator.
        </p>
      </div>
    </Shell>
  );
}
