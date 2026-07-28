# BlueTeamers Arena — API Versioning & Changelog

This document tracks API version changes, deprecation schedules, and backwards compatibility guarantees across `/api/v1/` and `/api/v2/`.

---

## 📌 API Versioning Policy

- **Current Stable Version**: `v1` (`/api/v1/`)
- **Experimental / Extended Version**: `v2` (`/api/v2/`)
- **Deprecation Notice**: APIs in `v1` will receive a minimum 12-month deprecation notice before sunsetting.

---

## 🚀 Version History

### Version 1.0.0 (Stable) — July 2026
- **Auth**: Admin JWT Authentication (`/api/v1/auth/login/`, `/token/refresh/`, `/logout/`, `/me/`).
- **Events**: Event management & code verification (`/api/v1/events/verify-code/`).
- **Participants**: Student registration & profile management (`/api/v1/participants/register-student/`).
- **Questions**: Question Bank CRUD with MCQ & Text prompt validation (`/api/v1/questions/`).
- **Challenges**: CTF scenario workspace, multi-format evidence files (`TXT`, `LOG`, `JSON`, `CSV`, `PNG`), and stripped public questions (`/api/v1/challenges/`).
- **Submissions & Auto-Grading**: Automatic answer grading, regex pattern matching, keyword checks, score calculation (`/api/v1/challenges/{slug}/submit/`).
- **Leaderboard**: Real-time ranking (`score` DESC, `time` ASC), top 3 podium, student rank lookup (`/api/v1/leaderboard/`).
- **Dashboard & Progress**: Dashboard metrics (`/api/v1/dashboard/`) and draft answer autosaving (`/api/v1/progress/{slug}/save-draft/`).
- **Admin & Audit**: Platform analytics dashboard, CSV report exports, and security audit logging (`/api/v1/admin/dashboard/`, `/audit-logs/`).

### Version 2.0.0 (Experimental) — July 2026
- Namespace `/api/v2/` added for future extended microservice integrations and webhooks.
