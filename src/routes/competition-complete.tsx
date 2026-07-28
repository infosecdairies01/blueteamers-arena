import { createFileRoute, Link } from "@tanstack/react-router";
import {
  CheckCircle2,
  Trophy,
  Target,
  Clock,
  Medal,
  ArrowLeft,
} from "lucide-react";

export const Route = createFileRoute("/competition-complete")({
  component: CompetitionComplete,
  head: () => ({
    meta: [
      { title: "Competition Complete — Blueteamers Arena" },
      {
        name: "description",
        content: "You have successfully completed all investigation challenges.",
      },
      {
        property: "og:title",
        content: "Competition Complete — Blueteamers Arena",
      },
      {
        property: "og:description",
        content: "You have successfully completed all investigation challenges.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
});

function CompetitionComplete() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-6 py-12">
      <div className="w-full max-w-3xl">
        <div className="text-center">
          <div className="mx-auto grid h-20 w-20 place-items-center rounded-2xl border border-emerald-500/30 bg-emerald-500/10">
            <CheckCircle2 className="h-10 w-10 text-emerald-400" />
          </div>
          <h1 className="mt-8 text-3xl font-extrabold tracking-tight">
            Competition Complete
          </h1>
          <p className="mx-auto mt-3 max-w-md text-sm text-muted-foreground">
            You have successfully completed all five investigation challenges.
          </p>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <SummaryCard
            icon={<Trophy className="h-4 w-4 text-emerald-400" />}
            label="Final Score"
            value="850 / 1000"
          />
          <SummaryCard
            icon={<Target className="h-4 w-4 text-emerald-400" />}
            label="Challenges Completed"
            value="5 / 5"
          />
          <SummaryCard
            icon={<Clock className="h-4 w-4 text-emerald-400" />}
            label="Time Taken"
            value="1h 47m"
          />
          <SummaryCard
            icon={<Medal className="h-4 w-4 text-emerald-400" />}
            label="Final Rank"
            value="#5"
          />
        </div>

        <div className="mt-8 rounded-xl border border-border bg-card p-6 text-center">
          <h2 className="text-lg font-semibold">Performance Summary</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            Excellent work! You completed all practical investigations and
            submitted every challenge before the timer expired.
          </p>
        </div>

        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link
            to="/leaderboard"
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-500 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-emerald-600"
          >
            <Trophy className="h-4 w-4" />
            View Leaderboard
          </Link>
          <Link
            to="/review"
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-border bg-[var(--surface)] px-5 py-2.5 text-sm font-semibold text-foreground transition-colors hover:bg-card"
          >
            Review My Answers
          </Link>
        </div>

        <div className="mt-8 text-center">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            <ArrowLeft className="h-4 w-4" /> Return to Dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}

function SummaryCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-border bg-card p-6">
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        {icon}
        {label}
      </div>
      <div className="mt-2 text-2xl font-bold">{value}</div>
    </div>
  );
}
