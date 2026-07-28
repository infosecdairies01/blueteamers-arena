import { createFileRoute, Link } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import {
  LayoutDashboard,
  Calendar,
  HelpCircle,
  Users,
  Trophy,
  Settings,
  ArrowLeft,
  Search,
  Plus,
  Upload,
  Eye,
  Pencil,
  Trash2,
  Copy,
  X,
} from "lucide-react";

export const Route = createFileRoute("/admin/questions")({
  component: AdminQuestions,
  head: () => ({
    meta: [
      { title: "Question Bank — Blueteamers Arena Admin" },
      { name: "description", content: "Manage the question bank across phishing, SIEM, AI, incident response, and digital forensics." },
      { property: "og:title", content: "Question Bank — Blueteamers Arena Admin" },
      { property: "og:description", content: "Manage the question bank across phishing, SIEM, AI, incident response, and digital forensics." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary" },
    ],
  }),
});

const navItems = [
  { title: "Dashboard", icon: LayoutDashboard, href: "/admin/dashboard" },
  { title: "Events", icon: Calendar, href: "/admin/events" },
  { title: "Questions", icon: HelpCircle, href: "/admin/questions" },
  { title: "Participants", icon: Users, href: "#" },
  { title: "Leaderboard", icon: Trophy, href: "/leaderboard" },
  { title: "Settings", icon: Settings, href: "#" },
];

type Category = "Phishing" | "SIEM" | "AI" | "Incident Response" | "Digital Forensics";
type Difficulty = "Easy" | "Medium" | "Hard";
type Status = "Published" | "Draft";

type Question = {
  id: string;
  question: string;
  evidence?: string;
  category: Category;
  difficulty: Difficulty;
  marks: number;
  status: Status;
  options: string[];
  correct: number;
  explanation?: string;
};

const CATEGORIES: Category[] = ["Phishing", "SIEM", "AI", "Incident Response", "Digital Forensics"];

const seed: Question[] = [
  {
    id: "1",
    question: "Which header field is most useful to verify the true sender of an email?",
    category: "Phishing",
    difficulty: "Easy",
    marks: 10,
    status: "Published",
    options: ["From", "Reply-To", "Return-Path", "Subject"],
    correct: 2,
    explanation: "Return-Path shows the actual envelope sender used for bounces.",
  },
  {
    id: "2",
    question: "In Wazuh, which rule level typically indicates a critical security alert?",
    category: "SIEM",
    difficulty: "Medium",
    marks: 15,
    status: "Published",
    options: ["Level 3", "Level 7", "Level 12", "Level 15"],
    correct: 3,
  },
  {
    id: "3",
    question: "What is the primary risk of blindly trusting an AI-generated incident summary?",
    category: "AI",
    difficulty: "Medium",
    marks: 15,
    status: "Draft",
    options: ["Slower triage", "Hallucinated indicators", "Higher CPU usage", "Lower cost"],
    correct: 1,
  },
  {
    id: "4",
    question: "Which NIST IR phase includes evidence preservation and root cause analysis?",
    category: "Incident Response",
    difficulty: "Hard",
    marks: 25,
    status: "Published",
    options: ["Preparation", "Detection", "Containment, Eradication & Recovery", "Post-Incident Activity"],
    correct: 2,
  },
  {
    id: "5",
    question: "Which artifact best proves execution of a binary on a Windows host?",
    category: "Digital Forensics",
    difficulty: "Hard",
    marks: 20,
    status: "Published",
    options: ["Prefetch", "MFT", "Recycle Bin", "Event ID 4624"],
    correct: 0,
  },
  {
    id: "6",
    question: "A URL uses punycode 'xn--pple-43d.com'. What technique is this?",
    category: "Phishing",
    difficulty: "Medium",
    marks: 15,
    status: "Published",
    options: ["Typosquatting", "Homograph attack", "Open redirect", "Clickjacking"],
    correct: 1,
  },
];

const CATEGORY_FILTERS: ("All" | Category)[] = ["All", ...CATEGORIES];

function AdminQuestions() {
  const [questions, setQuestions] = useState<Question[]>(seed);
  const [query, setQuery] = useState("");
  const [catFilter, setCatFilter] = useState<"All" | Category>("All");
  const [showAdd, setShowAdd] = useState(false);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return questions.filter((row) => {
      const matchQ = !q || row.question.toLowerCase().includes(q);
      const matchC = catFilter === "All" || row.category === catFilter;
      return matchQ && matchC;
    });
  }, [questions, query, catFilter]);

  const handleDelete = (id: string) => setQuestions((prev) => prev.filter((q) => q.id !== id));
  const handleDuplicate = (id: string) => {
    setQuestions((prev) => {
      const src = prev.find((q) => q.id === id);
      if (!src) return prev;
      return [{ ...src, id: `${Date.now()}`, question: `${src.question} (Copy)`, status: "Draft" }, ...prev];
    });
  };
  const handleAdd = (q: Question) => setQuestions((prev) => [q, ...prev]);

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
          <Link to="/admin/login" className="text-sm font-medium text-muted-foreground hover:text-foreground">
            Sign Out
          </Link>
        </nav>
      </header>

      <div className="mx-auto flex max-w-7xl items-start gap-6 px-6 py-10">
        <aside className="sticky top-6 hidden w-60 shrink-0 rounded-xl border border-border bg-card p-4 lg:block">
          <div className="mb-4 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Menu</div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const active = item.href === "/admin/questions";
              return (
                <Link
                  key={item.title}
                  to={item.href}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                    active
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-[var(--surface)] hover:text-foreground"
                  }`}
                >
                  <item.icon className="h-4 w-4" />
                  {item.title}
                </Link>
              );
            })}
          </nav>
        </aside>

        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Question Bank</h1>
              <p className="mt-1 text-sm text-muted-foreground">
                Author, categorize, and publish questions across blue team domains.
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <button className="inline-flex items-center gap-2 rounded-lg border border-border bg-card px-3.5 py-2.5 text-sm font-medium text-foreground hover:border-primary">
                <Upload className="h-4 w-4" /> Import
              </button>
              <button
                onClick={() => setShowAdd(true)}
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground transition-colors hover:bg-[var(--primary-hover)]"
              >
                <Plus className="h-4 w-4" /> Add Question
              </button>
            </div>
          </div>

          <div className="mt-6 flex flex-wrap items-center gap-3">
            <div className="relative min-w-[240px] flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search questions..."
                className="w-full rounded-lg border border-border bg-card py-2.5 pl-9 pr-3 text-sm outline-none placeholder:text-muted-foreground focus:border-primary"
              />
            </div>
            <div className="flex flex-wrap items-center gap-1 rounded-lg border border-border bg-card p-1">
              {CATEGORY_FILTERS.map((c) => (
                <button
                  key={c}
                  onClick={() => setCatFilter(c)}
                  className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
                    catFilter === c
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {c}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-6 overflow-hidden rounded-xl border border-border bg-card">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b border-border bg-[var(--surface)] text-xs uppercase text-muted-foreground">
                  <tr>
                    <th className="px-4 py-3 text-left font-medium">Question</th>
                    <th className="px-4 py-3 text-left font-medium">Category</th>
                    <th className="px-4 py-3 text-left font-medium">Difficulty</th>
                    <th className="px-4 py-3 text-right font-medium">Marks</th>
                    <th className="px-4 py-3 text-left font-medium">Status</th>
                    <th className="px-4 py-3 text-right font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((row) => (
                    <tr key={row.id} className="border-b border-border/50 last:border-0">
                      <td className="max-w-[420px] px-4 py-3 font-medium">
                        <div className="truncate">{row.question}</div>
                      </td>
                      <td className="px-4 py-3">
                        <span className="inline-flex items-center rounded-md border border-border bg-[var(--surface)] px-2 py-0.5 text-xs text-muted-foreground">
                          {row.category}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <DifficultyBadge difficulty={row.difficulty} />
                      </td>
                      <td className="px-4 py-3 text-right">{row.marks}</td>
                      <td className="px-4 py-3">
                        <StatusBadge status={row.status} />
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center justify-end gap-1">
                          <IconBtn label="View"><Eye className="h-4 w-4" /></IconBtn>
                          <IconBtn label="Edit"><Pencil className="h-4 w-4" /></IconBtn>
                          <IconBtn label="Duplicate" onClick={() => handleDuplicate(row.id)}>
                            <Copy className="h-4 w-4" />
                          </IconBtn>
                          <IconBtn label="Delete" danger onClick={() => handleDelete(row.id)}>
                            <Trash2 className="h-4 w-4" />
                          </IconBtn>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {filtered.length === 0 && (
                    <tr>
                      <td colSpan={6} className="px-4 py-10 text-center text-sm text-muted-foreground">
                        No questions match your filters.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="mt-8">
            <Link
              to="/admin/dashboard"
              className="inline-flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              <ArrowLeft className="h-4 w-4" /> Back to Dashboard
            </Link>
          </div>
        </div>
      </div>

      {showAdd && (
        <AddQuestionModal
          onClose={() => setShowAdd(false)}
          onSave={(q) => {
            handleAdd(q);
            setShowAdd(false);
          }}
        />
      )}
    </main>
  );
}

function IconBtn({
  children,
  label,
  onClick,
  danger,
}: {
  children: React.ReactNode;
  label: string;
  onClick?: () => void;
  danger?: boolean;
}) {
  return (
    <button
      title={label}
      onClick={onClick}
      className={`grid h-8 w-8 place-items-center rounded-md text-muted-foreground transition-colors hover:bg-[var(--surface)] ${
        danger ? "hover:text-red-400" : "hover:text-foreground"
      }`}
    >
      {children}
    </button>
  );
}

function StatusBadge({ status }: { status: Status }) {
  const styles =
    status === "Published"
      ? "bg-emerald-500/10 text-emerald-400"
      : "bg-amber-500/10 text-amber-400";
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${styles}`}>
      {status}
    </span>
  );
}

function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  const styles =
    difficulty === "Easy"
      ? "bg-emerald-500/10 text-emerald-400"
      : difficulty === "Medium"
      ? "bg-primary/10 text-primary"
      : "bg-red-500/10 text-red-400";
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${styles}`}>
      {difficulty}
    </span>
  );
}

function AddQuestionModal({
  onClose,
  onSave,
}: {
  onClose: () => void;
  onSave: (q: Question) => void;
}) {
  const [question, setQuestion] = useState("");
  const [evidence, setEvidence] = useState("");
  const [options, setOptions] = useState(["", "", "", ""]);
  const [correct, setCorrect] = useState(0);
  const [explanation, setExplanation] = useState("");
  const [category, setCategory] = useState<Category>("Phishing");
  const [difficulty, setDifficulty] = useState<Difficulty>("Easy");
  const [marks, setMarks] = useState("10");

  const save = (e: React.FormEvent) => {
    e.preventDefault();
    onSave({
      id: `${Date.now()}`,
      question: question || "Untitled Question",
      evidence: evidence || undefined,
      options: options.map((o) => o.trim()).filter(Boolean),
      correct,
      explanation: explanation || undefined,
      category,
      difficulty,
      marks: Number(marks) || 0,
      status: "Draft",
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4" onClick={onClose}>
      <form
        onSubmit={save}
        onClick={(e) => e.stopPropagation()}
        className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-xl border border-border bg-card p-6 shadow-2xl"
      >
        <div className="mb-5 flex items-start justify-between">
          <div>
            <h2 className="text-lg font-bold">Add Question</h2>
            <p className="mt-1 text-xs text-muted-foreground">Author a new question for the bank.</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-md p-1 text-muted-foreground hover:bg-[var(--surface)] hover:text-foreground"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="grid gap-4">
          <Field label="Question">
            <textarea
              required
              rows={2}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className={inputCls}
              placeholder="What did the attacker exfiltrate first?"
            />
          </Field>

          <Field label="Evidence (optional)">
            <textarea
              rows={2}
              value={evidence}
              onChange={(e) => setEvidence(e.target.value)}
              className={`${inputCls} font-mono text-xs`}
              placeholder="Paste log snippet, header, or artifact reference..."
            />
          </Field>

          <div>
            <label className="mb-1.5 block text-xs font-medium text-muted-foreground">Options</label>
            <div className="space-y-2">
              {options.map((opt, i) => (
                <div key={i} className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setCorrect(i)}
                    className={`grid h-8 w-8 shrink-0 place-items-center rounded-full border text-xs font-semibold transition-colors ${
                      correct === i
                        ? "border-emerald-400 bg-emerald-500/10 text-emerald-400"
                        : "border-border text-muted-foreground hover:border-primary"
                    }`}
                    title="Mark as correct answer"
                  >
                    {String.fromCharCode(65 + i)}
                  </button>
                  <input
                    value={opt}
                    onChange={(e) => {
                      const next = [...options];
                      next[i] = e.target.value;
                      setOptions(next);
                    }}
                    placeholder={`Option ${String.fromCharCode(65 + i)}`}
                    className={inputCls}
                  />
                </div>
              ))}
            </div>
            <p className="mt-2 text-xs text-muted-foreground">
              Click a letter to mark the correct answer.
            </p>
          </div>

          <Field label="Explanation">
            <textarea
              rows={2}
              value={explanation}
              onChange={(e) => setExplanation(e.target.value)}
              className={inputCls}
              placeholder="Why is this the correct answer?"
            />
          </Field>

          <div className="grid gap-4 sm:grid-cols-3">
            <Field label="Category">
              <select value={category} onChange={(e) => setCategory(e.target.value as Category)} className={inputCls}>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </Field>
            <Field label="Difficulty">
              <select value={difficulty} onChange={(e) => setDifficulty(e.target.value as Difficulty)} className={inputCls}>
                {(["Easy", "Medium", "Hard"] as Difficulty[]).map((d) => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </Field>
            <Field label="Marks">
              <input type="number" min={0} value={marks} onChange={(e) => setMarks(e.target.value)} className={inputCls} />
            </Field>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg border border-border px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-[var(--primary-hover)]"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  );
}

const inputCls =
  "w-full rounded-lg border border-border bg-background px-3 py-2 text-sm outline-none placeholder:text-muted-foreground focus:border-primary";

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-medium text-muted-foreground">{label}</label>
      {children}
    </div>
  );
}
