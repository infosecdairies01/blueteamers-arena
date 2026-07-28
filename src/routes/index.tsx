import { createFileRoute, useNavigate, Link } from "@tanstack/react-router";
import {
  ArrowRight,
  ShieldCheck,
  Brain,
  Trophy,
  Target,
  Siren,
  FileText,
  Mail,
  LineChart,
  Linkedin,
  Instagram,
  Youtube,
} from "lucide-react";

export const Route = createFileRoute("/")({
  component: Landing,
});

const navLinks = [
  { label: "Challenges", to: "/challenges" as const },
  { label: "Leaderboard", to: "/leaderboard" as const },
  { label: "Events", to: "/admin/events" as const },
  { label: "About Us", to: "/" as const, hash: "about" },
];

const features = [
  {
    icon: ShieldCheck,
    title: "Real Challenges",
    description: "Solve practical SOC scenarios based on real incidents.",
    tint: "bg-blue-500/10 text-blue-400",
  },
  {
    icon: Brain,
    title: "AI Assisted",
    description: "Use AI tools the way professionals do in SOC.",
    tint: "bg-emerald-500/10 text-emerald-400",
  },
  {
    icon: Trophy,
    title: "Live Competition",
    description: "Compete with students across multiple colleges.",
    tint: "bg-amber-500/10 text-amber-400",
  },
];

const categories = [
  { icon: ShieldCheck, label: "AI with SOC", tint: "text-blue-400" },
  { icon: Target, label: "Threat Hunting", tint: "text-emerald-400" },
  { icon: Siren, label: "Incident Response", tint: "text-red-400" },
  { icon: FileText, label: "Log Analysis", tint: "text-orange-400" },
  { icon: Mail, label: "Phishing Analysis", tint: "text-violet-400" },
  { icon: LineChart, label: "SIEM & Tools", tint: "text-sky-400" },
];

function Logo() {
  return (
    <div className="flex items-center gap-3">
      <div className="grid h-10 w-10 shrink-0 place-items-center rounded-lg border border-border bg-card">
        <span className="text-lg font-bold text-primary">B</span>
      </div>
      <div className="leading-tight">
        <div className="text-sm font-bold tracking-wide">BLUETEAMERS</div>
        <div className="text-xs font-semibold tracking-widest text-primary">ARENA</div>
      </div>
    </div>
  );
}

function PrimaryButton({
  children,
  className = "",
  onClick,
}: {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}) {
  const navigate = useNavigate();
  return (
    <button
      onClick={onClick ?? (() => navigate({ to: "/arena" }))}
      className={`inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground shadow-sm transition-colors hover:bg-[var(--primary-hover)] focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/60 ${className}`}
    >
      {children}
    </button>
  );
}

function GhostButton({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-lg border border-border bg-transparent px-5 py-2.5 text-sm font-semibold text-foreground transition-colors hover:bg-card ${className}`}
    >
      {children}
    </button>
  );
}

function Nav() {
  return (
    <header className="border-b border-border/60">
      <nav className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-5">
        <Logo />
        <ul className="hidden items-center gap-10 md:flex">
          {navLinks.map((l) => (
            <li key={l.label}>
              <Link
                to={l.to}
                hash={l.hash}
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>
        <div className="flex items-center gap-4">
          <a
            href="/admin/login"
            className="hidden text-sm font-medium text-foreground transition-colors hover:text-muted-foreground sm:inline"
          >
            Log in
          </a>
          <PrimaryButton>Enter Arena</PrimaryButton>
        </div>
      </nav>
    </header>
  );
}

function AppPreview() {
  return (
    <div className="overflow-hidden rounded-xl border border-border bg-card shadow-2xl shadow-black/40">
      {/* Title bar */}
      <div className="flex items-center gap-2 border-b border-border px-4 py-3">
        <span className="h-3 w-3 rounded-full bg-red-500" />
        <span className="h-3 w-3 rounded-full bg-yellow-500" />
        <span className="h-3 w-3 rounded-full bg-green-500" />
      </div>
      <div className="grid grid-cols-[180px_1fr]">
        {/* Sidebar */}
        <aside className="border-r border-border p-4">
          <div className="mb-4 text-xs font-semibold tracking-widest text-muted-foreground">
            ARENA
          </div>
          <ul className="space-y-1 text-sm">
            {[
              { label: "Dashboard", active: false },
              { label: "Challenges", active: true },
              { label: "Leaderboard", active: false },
              { label: "Events", active: false },
              { label: "Profile", active: false },
            ].map((item) => (
              <li
                key={item.label}
                className={`flex items-center gap-2 rounded-md px-2 py-1.5 ${
                  item.active
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground"
                }`}
              >
                <span
                  className={`h-1.5 w-1.5 rounded-full ${
                    item.active ? "bg-primary" : "bg-muted-foreground/50"
                  }`}
                />
                {item.label}
              </li>
            ))}
          </ul>
        </aside>

        {/* Content */}
        <div className="p-5">
          <div className="mb-3 flex items-center justify-between">
            <div className="text-sm font-semibold">Question 8 / 25</div>
            <span className="rounded-md bg-emerald-500/10 px-2 py-0.5 text-xs font-medium text-emerald-400">
              Medium
            </span>
          </div>
          <div className="mb-1 h-1.5 w-full overflow-hidden rounded-full bg-border">
            <div className="h-full w-[32%] rounded-full bg-primary" />
          </div>
          <div className="mb-5 flex items-center justify-between text-xs text-muted-foreground">
            <span>32%</span>
            <span>20 Points</span>
          </div>

          <div className="rounded-lg border border-border bg-[var(--surface)] p-4">
            <p className="text-sm text-foreground">
              Multiple failed logins detected from 192.168.1.22.
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              What should a SOC analyst do first?
            </p>
            <div className="mt-4 space-y-2.5 text-sm">
              {[
                { label: "Block the IP address", checked: false },
                { label: "Investigate the logs", checked: true },
                { label: "Ignore the alert", checked: false },
                { label: "Reset the user password", checked: false },
              ].map((opt) => (
                <label
                  key={opt.label}
                  className="flex cursor-pointer items-center gap-3"
                >
                  <span
                    className={`grid h-4 w-4 place-items-center rounded-full border ${
                      opt.checked
                        ? "border-primary"
                        : "border-muted-foreground/60"
                    }`}
                  >
                    {opt.checked && (
                      <span className="h-2 w-2 rounded-full bg-primary" />
                    )}
                  </span>
                  <span
                    className={
                      opt.checked ? "text-foreground" : "text-muted-foreground"
                    }
                  >
                    {opt.label}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <div className="mt-5 flex items-center justify-between">
            <button className="rounded-md border border-border px-3.5 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground">
              Skip
            </button>
            <button className="rounded-md bg-primary px-4 py-1.5 text-xs font-semibold text-primary-foreground hover:bg-[var(--primary-hover)]">
              Submit Answer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function Hero() {
  return (
    <section className="mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-6 py-20 lg:grid-cols-2 lg:py-28">
      <div>
        <h1 className="text-5xl font-extrabold leading-[1.05] tracking-tight sm:text-6xl">
          <span className="block">Train Like a</span>
          <span className="block">SOC Analyst.</span>
          <span className="mt-2 block text-primary">Compete Like a Defender.</span>
        </h1>
        <p className="mt-6 max-w-md text-base leading-relaxed text-muted-foreground">
          Practice real-world cybersecurity challenges using AI-powered SOC scenarios
          for the next generation of blue teams.
        </p>
        <div className="mt-8 flex flex-wrap items-center gap-3">
          <PrimaryButton>
            Enter Arena <ArrowRight className="h-4 w-4" />
          </PrimaryButton>
          <GhostButton>View Challenges</GhostButton>
        </div>
      </div>
      <div className="lg:pl-4">
        <AppPreview />
      </div>
    </section>
  );
}

function Features() {
  return (
    <section className="border-y border-border bg-[var(--surface)]/40">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-10 px-6 py-16 md:grid-cols-3">
        {features.map((f) => (
          <div key={f.title} className="flex items-start gap-4">
            <div className={`grid h-12 w-12 shrink-0 place-items-center rounded-xl ${f.tint}`}>
              <f.icon className="h-5 w-5" />
            </div>
            <div className="min-w-0">
              <h3 className="text-base font-semibold">{f.title}</h3>
              <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
                {f.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function Categories() {
  return (
    <section id="challenges" className="mx-auto max-w-7xl px-6 py-20">
      <h2 className="text-center text-2xl font-bold tracking-tight sm:text-3xl">
        Challenge Categories
      </h2>
      <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
        {categories.map((c) => (
          <div
            key={c.label}
            className="flex items-center gap-3 rounded-xl border border-border bg-card px-4 py-5 transition-colors hover:border-primary/40"
          >
            <c.icon className={`h-5 w-5 shrink-0 ${c.tint}`} />
            <span className="text-sm font-medium">{c.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function FinalCTA() {
  return (
    <section className="mx-auto max-w-7xl px-6 pb-20">
      <div className="flex flex-col items-center justify-center gap-6 rounded-xl border border-border bg-card px-6 py-10 sm:flex-row sm:justify-between sm:px-12">
        <h3 className="text-xl font-semibold sm:text-2xl">Ready to test your skills?</h3>
        <PrimaryButton>Enter Arena</PrimaryButton>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 py-8 sm:flex-row">
        <div className="text-sm font-bold tracking-widest">BLUETEAMERS ARENA</div>
        <div className="text-sm text-muted-foreground">© 2026 All rights reserved.</div>
        <div className="flex items-center gap-4 text-muted-foreground">
          <span className="text-sm">Follow us</span>
          <a href="#" aria-label="LinkedIn" className="hover:text-foreground">
            <Linkedin className="h-4 w-4" />
          </a>
          <a href="#" aria-label="Instagram" className="hover:text-foreground">
            <Instagram className="h-4 w-4" />
          </a>
          <a href="#" aria-label="YouTube" className="hover:text-foreground">
            <Youtube className="h-4 w-4" />
          </a>
        </div>
      </div>
    </footer>
  );
}

function Landing() {
  return (
    <main className="min-h-screen bg-background">
      <Nav />
      <Hero />
      <Features />
      <Categories />
      <FinalCTA />
      <Footer />
    </main>
  );
}
