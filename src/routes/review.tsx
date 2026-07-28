import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowLeft, CheckCircle2, Home } from "lucide-react";

export const Route = createFileRoute("/review")({
  component: Review,
  head: () => ({
    meta: [
      { title: "Review My Answers — Blueteamers Arena" },
      { name: "description", content: "Review your submitted answers." },
      { property: "og:title", content: "Review My Answers — Blueteamers Arena" },
      { property: "og:description", content: "Review your submitted answers." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
});

function Review() {
  return (
    <main className="min-h-screen bg-background px-6 py-12">
      <div className="mx-auto max-w-3xl">
        <div className="flex items-center gap-4">
          <Link
            to="/competition-complete"
            className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            <ArrowLeft className="h-4 w-4" /> Back
          </Link>
          <span className="text-muted-foreground/40">•</span>
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
          >
            <Home className="h-4 w-4" /> Back to Home
          </Link>
        </div>
        <h1 className="mt-6 text-2xl font-bold tracking-tight">
          Review My Answers
        </h1>
        <div className="mt-6 flex items-center gap-3 rounded-xl border border-border bg-card p-6">
          <CheckCircle2 className="h-5 w-5 flex-none text-emerald-400" />
          <p className="text-sm text-muted-foreground">
            All answers have been submitted and saved. A detailed review panel
            will be available here soon.
          </p>
        </div>
      </div>
    </main>
  );
}
