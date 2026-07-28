import { useMemo, useRef, useState } from "react";
import {
  Copy,
  Check,
  Download,
  Maximize2,
  Minimize2,
  Search,
  WrapText,
  X,
} from "lucide-react";
import type { EvidenceFormat } from "@/lib/evidence-text";

type Props = {
  filename: string;
  format: EvidenceFormat;
  content: string;
};

function escapeHtml(s: string) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// Very small JSON tokenizer -> HTML with Tailwind classes.
function highlightJson(line: string) {
  const escaped = escapeHtml(line);
  // strings (keys vs values differentiated by trailing colon)
  return escaped
    .replace(
      /("(?:\\.|[^"\\])*")(\s*:)/g,
      '<span class="text-sky-300">$1</span><span class="text-slate-400">$2</span>',
    )
    .replace(
      /(:\s*)("(?:\\.|[^"\\])*")/g,
      '$1<span class="text-emerald-300">$2</span>',
    )
    .replace(
      /\b(true|false|null)\b/g,
      '<span class="text-purple-300">$1</span>',
    )
    .replace(
      /(^|[\s,\[])(-?\d+(?:\.\d+)?)/g,
      '$1<span class="text-amber-300">$2</span>',
    )
    .replace(/([{}\[\],])/g, '<span class="text-slate-500">$1</span>');
}

// Log highlighter: URLs, IPs, hashes, filenames, PowerShell/suspicious keywords.
function highlightLog(line: string) {
  const esc = escapeHtml(line);
  const patterns: { re: RegExp; cls: string }[] = [
    { re: /(https?:\/\/[^\s'"<>]+)/g, cls: "text-sky-300 underline decoration-sky-500/40" },
    { re: /\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?\b/g, cls: "text-rose-300" },
    { re: /\b[a-fA-F0-9]{32,64}\b/g, cls: "text-amber-300" },
    {
      re: /\b[\w.\-]+\.(?:exe|ps1|dll|zip|dmp|log|bat|vbs|xlsx|pdf|txt|php)\b/gi,
      cls: "text-emerald-300",
    },
    {
      re: /\b(IEX|Invoke-Expression|New-Object|DownloadString|Set-MpPreference|Add-MpPreference|powershell|Net\.WebClient|wevtutil|rundll32)\b/g,
      cls: "text-purple-300",
    },
    {
      re: /\b(mimikatz|sekurlsa|lsass|vssadmin|netsh|whoami|logonpasswords|RDPClip|AnyDesk|support_admin)\b/gi,
      cls: "text-rose-400 font-semibold",
    },
    {
      re: /(delete shadows|net user|net localgroup|net use)/gi,
      cls: "text-rose-400 font-semibold",
    },
  ];
  let result = esc;
  const placeholders: string[] = [];
  for (const { re, cls } of patterns) {
    result = result.replace(re, (m) => {
      const idx = placeholders.length;
      placeholders.push(`<span class="${cls}">${m}</span>`);
      return `\u0000${idx}\u0000`;
    });
  }
  return result.replace(/\u0000(\d+)\u0000/g, (_, i) => placeholders[+i]);
}

function applySearch(html: string, query: string) {
  if (!query) return html;
  try {
    const re = new RegExp(
      query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
      "gi",
    );
    return html.replace(
      re,
      (m) =>
        `<mark class="bg-amber-400/30 text-amber-100 rounded-sm px-0.5">${m}</mark>`,
    );
  } catch {
    return html;
  }
}

export function EvidenceCodeViewer({ filename, format, content }: Props) {
  const [wrap, setWrap] = useState(false);
  const [query, setQuery] = useState("");
  const [showSearch, setShowSearch] = useState(false);
  const [copied, setCopied] = useState(false);
  const [full, setFull] = useState(false);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  const lines = useMemo(() => content.replace(/\r\n/g, "\n").split("\n"), [
    content,
  ]);

  // Parse CSV once per content change.
  const csv = useMemo(() => {
    if (format !== "csv") return null;
    // simple parser (no quoted commas in this dataset)
    const rows = lines
      .filter((l, i) => !(i === lines.length - 1 && l === ""))
      .map((l) => l.split(","));
    return rows;
  }, [format, lines]);

  const matchCount = useMemo(() => {
    if (!query) return 0;
    try {
      const re = new RegExp(
        query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
        "gi",
      );
      return (content.match(re) ?? []).length;
    } catch {
      return 0;
    }
  }, [content, query]);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    } catch {
      /* ignore */
    }
  };

  const download = () => {
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  };

  const IconBtn = ({
    title,
    onClick,
    active,
    children,
  }: {
    title: string;
    onClick: () => void;
    active?: boolean;
    children: React.ReactNode;
  }) => (
    <button
      type="button"
      title={title}
      aria-label={title}
      onClick={onClick}
      className={`inline-flex h-7 w-7 items-center justify-center rounded-md border border-border text-muted-foreground transition-colors hover:text-foreground ${
        active
          ? "bg-blue-500/15 text-blue-300 border-blue-500/40"
          : "bg-[var(--surface)]"
      }`}
    >
      {children}
    </button>
  );

  const body = (
    <div
      className={`flex flex-col overflow-hidden rounded-lg border border-border bg-[#0b1220] ${
        full ? "h-full" : "h-[520px]"
      }`}
    >
      {/* Sticky filename header */}
      <div className="sticky top-0 z-10 flex items-center justify-between gap-2 border-b border-border bg-[#0d1526] px-3 py-2">
        <div className="flex min-w-0 items-center gap-2 text-xs">
          <span className="inline-block h-2 w-2 rounded-full bg-emerald-400/80" />
          <span className="truncate font-mono text-slate-200">{filename}</span>
          <span className="rounded border border-border px-1.5 py-0.5 text-[10px] uppercase tracking-wider text-muted-foreground">
            {format}
          </span>
          <span className="text-[10px] text-muted-foreground">
            {lines.length} lines
          </span>
        </div>
        <div className="flex items-center gap-1">
          <IconBtn
            title="Search"
            onClick={() => setShowSearch((v) => !v)}
            active={showSearch}
          >
            <Search className="h-3.5 w-3.5" />
          </IconBtn>
          <IconBtn
            title="Toggle word wrap"
            onClick={() => setWrap((v) => !v)}
            active={wrap}
          >
            <WrapText className="h-3.5 w-3.5" />
          </IconBtn>
          <IconBtn title={copied ? "Copied!" : "Copy"} onClick={copy}>
            {copied ? (
              <Check className="h-3.5 w-3.5 text-emerald-400" />
            ) : (
              <Copy className="h-3.5 w-3.5" />
            )}
          </IconBtn>
          <IconBtn title="Download" onClick={download}>
            <Download className="h-3.5 w-3.5" />
          </IconBtn>
          <IconBtn
            title={full ? "Exit fullscreen" : "Fullscreen"}
            onClick={() => setFull((v) => !v)}
          >
            {full ? (
              <Minimize2 className="h-3.5 w-3.5" />
            ) : (
              <Maximize2 className="h-3.5 w-3.5" />
            )}
          </IconBtn>
        </div>
      </div>

      {showSearch && (
        <div className="flex items-center gap-2 border-b border-border bg-[#0d1526] px-3 py-2">
          <Search className="h-3.5 w-3.5 text-muted-foreground" />
          <input
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search in file..."
            className="flex-1 rounded-md border border-border bg-[#0b1220] px-2 py-1 font-mono text-xs text-slate-200 outline-none placeholder:text-muted-foreground focus:border-blue-500/60"
          />
          <span className="font-mono text-[11px] text-muted-foreground">
            {query ? `${matchCount} match${matchCount === 1 ? "" : "es"}` : ""}
          </span>
          <button
            type="button"
            onClick={() => {
              setQuery("");
              setShowSearch(false);
            }}
            className="text-muted-foreground hover:text-foreground"
            aria-label="Close search"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      )}

      {/* Body */}
      <div ref={scrollRef} className="flex-1 overflow-auto">
        {format === "csv" && csv ? (
          <table className="w-full min-w-full border-collapse font-mono text-[12px]">
            <thead className="sticky top-0 bg-[#0d1526]">
              <tr>
                <th className="w-12 border-b border-border px-2 py-1.5 text-right text-[10px] font-normal text-muted-foreground">
                  #
                </th>
                {csv[0]?.map((h, i) => (
                  <th
                    key={i}
                    className="border-b border-border px-3 py-1.5 text-left text-[11px] font-semibold uppercase tracking-wider text-sky-300"
                  >
                    <span
                      dangerouslySetInnerHTML={{
                        __html: applySearch(escapeHtml(h), query),
                      }}
                    />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {csv.slice(1).map((row, ri) => (
                <tr key={ri} className="hover:bg-white/[0.02]">
                  <td className="w-12 select-none border-b border-border/50 px-2 py-1 text-right text-[10px] text-muted-foreground">
                    {ri + 1}
                  </td>
                  {row.map((cell, ci) => (
                    <td
                      key={ci}
                      className="whitespace-nowrap border-b border-border/50 px-3 py-1 text-slate-200"
                    >
                      <span
                        dangerouslySetInnerHTML={{
                          __html: applySearch(escapeHtml(cell), query),
                        }}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <pre
            className={`m-0 font-mono text-[12.5px] leading-5 text-slate-200 ${
              wrap ? "whitespace-pre-wrap break-words" : "whitespace-pre"
            }`}
          >
            {lines.map((line, i) => {
              const rendered =
                format === "json"
                  ? highlightJson(line)
                  : format === "log"
                    ? highlightLog(line)
                    : escapeHtml(line);
              const withSearch = applySearch(rendered, query);
              return (
                <div key={i} className="flex hover:bg-white/[0.02]">
                  <span className="sticky left-0 w-12 flex-none select-none border-r border-border/60 bg-[#0b1220] px-2 py-0 text-right text-[11px] text-muted-foreground">
                    {i + 1}
                  </span>
                  <span
                    className="flex-1 px-3"
                    dangerouslySetInnerHTML={{ __html: withSearch || "&nbsp;" }}
                  />
                </div>
              );
            })}
          </pre>
        )}
      </div>
    </div>
  );

  if (full) {
    return (
      <div className="fixed inset-0 z-50 flex flex-col bg-background/95 p-4 backdrop-blur">
        {body}
      </div>
    );
  }
  return body;
}
