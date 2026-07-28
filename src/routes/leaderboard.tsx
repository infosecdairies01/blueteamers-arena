import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { ArrowLeft, Search } from "lucide-react";

export const Route = createFileRoute("/leaderboard")({
  component: Leaderboard,
  head: () => ({
    meta: [
      { title: "Leaderboard — Blueteamers Arena" },
      { name: "description", content: "Competition leaderboard." },
      { property: "og:title", content: "Leaderboard — Blueteamers Arena" },
      { property: "og:description", content: "Competition leaderboard." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
});

const podium = [
  { rank: 1, medal: "🥇", name: "Rahul", score: 950, time: "1:42:18", color: "#F59E0B" },
  { rank: 2, medal: "🥈", name: "Akhil", score: 910, time: "1:45:07", color: "#9CA3AF" },
  { rank: 3, medal: "🥉", name: "Sanjay", score: 890, time: "1:48:12", color: "#B45309" },
];

const tableRows = [
  { rank: 4, student: "Anjali", challenges: "5/5", score: 870, time: "1:49:52", status: "Completed" },
  { rank: 5, student: "Kiran", challenges: "5/5", score: 850, time: "1:52:41", status: "Completed" },
  { rank: 6, student: "Priya", challenges: "4/5", score: 720, time: "—", status: "Running" },
  { rank: 7, student: "Rohith", challenges: "3/5", score: 610, time: "—", status: "Running" },
];

type Filter = "All" | "Completed" | "Running";

function Leaderboard() {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<Filter>("All");

  const filteredRows = tableRows.filter((row) => {
    const matchesSearch = row.student.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === "All" || row.status === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <main className="min-h-screen bg-background px-6 py-12">
      <div className="mx-auto max-w-5xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Leaderboard</h1>
            <p className="mt-1 text-sm text-muted-foreground">CBIT • AI with SOC Workshop</p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search student"
                className="h-9 rounded-lg border border-border bg-card pl-9 pr-3 text-sm text-foreground placeholder:text-muted-foreground outline-none focus:border-primary"
              />
            </div>
            <FilterButton active={filter === "All"} onClick={() => setFilter("All")}>
              All
            </FilterButton>
            <FilterButton active={filter === "Completed"} onClick={() => setFilter("Completed")}>
              Completed
            </FilterButton>
            <FilterButton active={filter === "Running"} onClick={() => setFilter("Running")}>
              Running
            </FilterButton>
          </div>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
          {podium.map((p) => (
            <div
              key={p.rank}
              className="rounded-xl border border-border bg-card p-6 text-center"
            >
              <div
                className="mx-auto flex h-12 w-12 items-center justify-center rounded-full text-xl"
                style={{ backgroundColor: `${p.color}20`, color: p.color }}
              >
                {p.medal}
              </div>
              <div className="mt-4 text-lg font-semibold">{p.name}</div>
              <div className="mt-1 text-2xl font-bold">{p.score} Points</div>
              <div className="mt-1 text-sm text-muted-foreground">Time {p.time}</div>
            </div>
          ))}
        </div>

        <div className="mt-8 overflow-hidden rounded-xl border border-border bg-card">
          <table className="w-full text-sm">
            <thead className="border-b border-border bg-[var(--surface)] text-xs uppercase text-muted-foreground">
              <tr>
                <th className="px-4 py-3 text-left font-medium">Rank</th>
                <th className="px-4 py-3 text-left font-medium">Student</th>
                <th className="px-4 py-3 text-left font-medium">Challenges</th>
                <th className="px-4 py-3 text-right font-medium">Score</th>
                <th className="px-4 py-3 text-right font-medium">Time</th>
                <th className="px-4 py-3 text-left font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredRows.map((row) => (
                <tr key={row.rank} className="border-b border-border/50 last:border-0">
                  <td className="px-4 py-3 font-medium text-muted-foreground">{row.rank}</td>
                  <td className="px-4 py-3 font-medium">{row.student}</td>
                  <td className="px-4 py-3 text-muted-foreground">{row.challenges}</td>
                  <td className="px-4 py-3 text-right font-medium">{row.score}</td>
                  <td className="px-4 py-3 text-right text-muted-foreground">{row.time}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        row.status === "Completed"
                          ? "bg-emerald-500/10 text-emerald-400"
                          : "bg-primary/10 text-primary"
                      }`}
                    >
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
              {filteredRows.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-sm text-muted-foreground">
                    No students match your search.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="mt-8">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            <ArrowLeft className="h-4 w-4" /> Back to Dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}

function FilterButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`h-9 rounded-lg px-3 text-sm font-medium transition-colors ${
        active
          ? "bg-primary text-primary-foreground"
          : "border border-border bg-card text-foreground hover:bg-[var(--surface)]"
      }`}
    >
      {children}
    </button>
  );
}
