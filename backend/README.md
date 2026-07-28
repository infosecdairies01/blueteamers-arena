# BlueTeamers Arena — Backend API Service

Production-ready Django 5 REST Framework backend powering **BlueTeamers Arena**, a gamified cybersecurity SOC training platform.

---

## 🎯 Architecture & Features

- **Service Layer Architecture**: Clean separation between Viewsets, Serializers, Services, Selectors, and Validators.
- **Custom User Model**: UUID primary keys and Role-Based Access Control (`ADMIN`, `SUPER_ADMIN`).
- **Student Platform APIs**: Event code verification, student registration, signed participant token auth (`X-Participant-Token`), and dashboard metrics.
- **Backend-Controlled Timer Engine**: Computes elapsed and remaining time strictly from database records to prevent browser refresh resets.
- **CTF Challenge Workspace**: Supports 5 CTF scenarios with multi-format evidence files (`TXT`, `LOG`, `JSON`, `CSV`, `PNG`).
- **Auto-Grading Engine**: Supports text normalization, regex matching, keyword checks, MCQ grading, and partial scoring.
- **Real-Time Leaderboard & WebSockets**: Live ranking calculations (`score` DESC, `finished_at` ASC) and Django Channels WebSockets broadcast (`/ws/arena/<event_code>/`).
- **Admin Platform & Analytics**: Platform-wide metrics, event analytics, question accuracy stats, CSV report export, and security audit logs (`AuditLog`).
- **Production Infrastructure**: Health API (`/api/health/`), Celery background worker, Redis caching, Whitenoise static file serving, and Docker Compose stack.

---

## 🛠️ Quick Start (Local Development)

### 1. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```

### 3. Run Migrations & Seed Demo Data
```bash
python manage.py migrate
python manage.py seed_demo
```

### 4. Start Development Server
```bash
python manage.py runserver 8000
```

### 5. Access Interactive API Documentation
- **Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- **ReDoc**: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
- **Health Check**: [http://localhost:8000/api/health/](http://localhost:8000/api/health/)

---

## 🧪 Running Automated Unit Tests

```bash
python manage.py test
```

Includes test coverage for:
- Accounts & Auth (`test_auth.py`, `test_user.py`)
- Events (`test_events.py`)
- Questions (`test_questions.py`)
- Challenges (`test_challenges.py`)
- Participants & Progress (`test_participants.py`, `test_participant_auth.py`, `test_progress.py`)
- Submissions & Auto-Grading (`test_auto_grading.py`, `test_submissions.py`)
- Leaderboard (`test_leaderboard.py`)
- Audit Logs & Admin Platform (`test_audit.py`, `test_admin_platform.py`)
- Health Check & Security Throttling (`test_health.py`, `test_throttling.py`)
