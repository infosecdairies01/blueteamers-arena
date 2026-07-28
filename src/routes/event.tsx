import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Calendar, Clock, Target, Users } from "lucide-react";
import { ACCENT_CLASSES, getSelectedEvent, type MockEvent } from "@/lib/mock-events";

export const Route = createFileRoute("/event")({
  component: Event,
  head: () => ({
    meta: [
      { title: "Event Welcome — Blueteamers Arena" },
      { name: "description", content: "Event details for your Blueteamers Arena workshop." },
      { property: "og:title", content: "Event Welcome — Blueteamers Arena" },
      { property: "og:description", content: "Event details for your Blueteamers Arena workshop." },
    ],
  }),
});

function Event() {
  const navigate = useNavigate();
  const [ev, setEv] = useState<MockEvent | null>(null);

  useEffect(() => {
    setEv(getSelectedEvent());
  }, []);

  if (!ev) return null;
  const accent = ACCENT_CLASSES[ev.accent];

  const stats = [
    { icon: Calendar, value: ev.date, label: "Event Date" },
    { icon: Clock, value: ev.duration, label: "Duration" },
    { icon: Target, value: `${ev.challenges} Challenges`, label: "Total Challenges" },
    { icon: Users, value: String(ev.participants), label: "Participants" },
  ];

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
          <a href="#about" className="text-sm font-medium text-muted-foreground hover:text-foreground">About</a>
        </nav>
      </header>
      <div className="mx-auto flex max-w-3xl flex-col px-6 py-16">
        <div className="rounded-xl border border-border bg-card p-8 shadow-2xl shadow-black/40">
          <div className="flex items-center gap-6">
            <div className={`grid h-20 w-20 shrink-0 place-items-center rounded-xl border ${accent.border} ${accent.bgSoft}`}>
              <span className={`text-2xl font-bold ${accent.text}`}>{ev.college.charAt(0)}</span>
            </div>
            <div>
              <h1 className="text-4xl font-extrabold tracking-tight">{ev.college}</h1>
              <p className={`mt-1 text-lg ${accent.text}`}>{ev.workshop}</p>
            </div>
          </div>

          <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4">
            {stats.map((s) => (
              <div key={s.label} className="rounded-lg border border-border bg-[var(--surface)] p-4 text-center">
                <s.icon className={`mx-auto h-5 w-5 ${accent.text}`} />
                <div className="mt-2 text-sm font-semibold">{s.value}</div>
                <div className="mt-0.5 text-xs text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>

          <button
            onClick={() => navigate({ to: "/student" })}
            className={`mt-8 w-full rounded-lg ${accent.bg} ${accent.hover} px-5 py-3 text-sm font-semibold text-white transition-colors`}
          >
            Continue
          </button>
        </div>
      </div>
    </main>
  );
}
