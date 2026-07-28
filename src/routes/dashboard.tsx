import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  Target,
  Trophy,
  BookOpen,
  Award,
  Clock,
  ArrowRight,
  CheckCircle2,
  X,
} from "lucide-react";
import {
  ACCENT_CLASSES,
  getSelectedEvent,
  getStudentName,
  type MockEvent,
} from "@/lib/mock-events";

export const Route = createFileRoute("/dashboard")({
  component: Dashboard,
  head: () => ({
    meta: [
      { title: "Dashboard — Blueteamers Arena" },
      { name: "description", content: "Your arena dashboard." },
      { property: "og:title", content: "Dashboard — Blueteamers Arena" },
      { property: "og:description", content: "Your arena dashboard." },
    ],
  }),
});

const sidebar = [
  { label: "Dashboard", icon: LayoutDashboard, active: true },
  { label: "Challenges", icon: Target, active: false },
  { label: "Leaderboard", icon: Trophy, active: false },
  { label: "Rules", icon: BookOpen, active: false },
  { label: "Certificate", icon: Award, active: false, locked: true },
];

const rules = [
  "20 Challenges",
  "60 Minutes Duration",
  "One Attempt Only",
  "No Page Refresh / Back",
  "Auto Submit on Timeout",
];

function Dashboard() {
  const [open, setOpen] = useState(false);
  const [ev, setEv] = useState<MockEvent | null>(null);
  const [name, setName] = useState("Rahul");

  useEffect(() => {
    setEv(getSelectedEvent());
    setName(getStudentName());
  }, []);

  if (!ev) return null;
  const accent = ACCENT_CLASSES[ev.accent];

  const stats = [
    { label: "Progress", value: "0%" },
    { label: "Score", value: "0", sub: "Points" },
    { label: "Rank", value: "--", sub: `/ ${ev.participants}` },
    { label: "Challenges", value: `0 / ${ev.challenges}`, sub: "Completed" },
  ];

  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-6 py-8 lg:grid-cols-[220px_1fr]">
        <aside className="rounded-xl border border-border bg-card p-4">
          <Link to="/" className="mb-6 flex items-center gap-3 px-2">
            <div className="grid h-9 w-9 place-items-center rounded-lg border border-border bg-[var(--surface)]">
              <span className={`text-base font-bold ${accent.text}`}>B</span>
            </div>
            <div className="leading-tight">
              <div className="text-xs font-bold tracking-wide">BLUETEAMERS</div>
              <div className={`text-[10px] font-semibold tracking-widest ${accent.text}`}>ARENA</div>
            </div>
          </Link>
          <ul className="space-y-1 text-sm">
            {sidebar.map((item) => (
              <li
                key={item.label}
                className={`flex items-center gap-3 rounded-md px-3 py-2 ${
                  item.active
                    ? `${accent.bgSoft} ${accent.text}`
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <item.icon className="h-4 w-4" />
                <span className="flex-1">{item.label}</span>
                {item.locked && <span className="text-[10px]">🔒</span>}
              </li>
            ))}
          </ul>
        </aside>

        <div className="space-y-6">
          <div className="flex flex-wrap items-start justify-between gap-4 rounded-xl border border-border bg-card p-6">
            <div>
              <div className="text-sm text-muted-foreground">Welcome back,</div>
              <h1 className="mt-1 text-3xl font-extrabold tracking-tight">
                {name} <span>👋</span>
              </h1>
              <p className="mt-1 text-sm text-muted-foreground">
                {ev.college} • {ev.workshop}
              </p>
            </div>
            <div className="rounded-lg border border-border bg-[var(--surface)] px-5 py-3 text-center">
              <div className="text-xs text-muted-foreground">Time Left</div>
              <div className="mt-1 flex items-center gap-2 text-2xl font-bold">
                <Clock className={`h-5 w-5 ${accent.text}`} /> 60:00
              </div>
              <div className="text-xs text-muted-foreground">Minutes</div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            {stats.map((s) => (
              <div key={s.label} className="rounded-xl border border-border bg-card p-5">
                <div className="text-xs text-muted-foreground">{s.label}</div>
                <div className="mt-2 text-2xl font-bold">{s.value}</div>
                {s.sub && <div className="mt-0.5 text-xs text-muted-foreground">{s.sub}</div>}
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="rounded-xl border border-border bg-card p-6">
              <h3 className="text-lg font-semibold">Start Your Journey</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Click the button below to start the first challenge.
              </p>
              <button
                onClick={() => setOpen(true)}
                className={`mt-6 inline-flex items-center gap-2 rounded-lg ${accent.bg} ${accent.hover} px-5 py-2.5 text-sm font-semibold text-white transition-colors`}
              >
                Start Challenge <ArrowRight className="h-4 w-4" />
              </button>
            </div>

            <div className="rounded-xl border border-border bg-card p-6">
              <h3 className="text-lg font-semibold">Event Info</h3>
              <dl className="mt-4 space-y-2 text-sm">
                {[
                  ["Event", ev.workshop],
                  ["College", ev.college],
                  ["Date", ev.date],
                  ["Duration", ev.duration],
                ].map(([k, v]) => (
                  <div key={k} className="flex justify-between border-b border-border/60 py-2 last:border-0">
                    <dt className="text-muted-foreground">{k}</dt>
                    <dd className="font-medium">{v}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      </div>

      {open && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
          onClick={() => setOpen(false)}
        >
          <div
            className="w-full max-w-md rounded-xl border border-border bg-card p-8 shadow-2xl shadow-black/60"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold">Rules of the Arena</h2>
              <button
                onClick={() => setOpen(false)}
                className="text-muted-foreground hover:text-foreground"
                aria-label="Close"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <ul className="mt-6 space-y-3">
              {rules.map((r) => (
                <li key={r} className="flex items-center gap-3 text-sm">
                  <CheckCircle2 className={`h-5 w-5 ${accent.text}`} />
                  {r}
                </li>
              ))}
            </ul>
            <Link
              to="/challenges"
              className={`mt-8 block w-full rounded-lg ${accent.bg} ${accent.hover} px-5 py-3 text-center text-sm font-semibold text-white transition-colors`}
            >
              Start Competition
            </Link>
          </div>
        </div>
      )}
    </main>
  );
}
