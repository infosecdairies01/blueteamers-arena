# BlueTeamers Arena — Production Deployment Guide

This guide details the complete production deployment procedures, environment variable configuration, security checklist, and Docker stack setup for the **BlueTeamers Arena** Django REST Framework backend.

---

## 🏗️ Architecture Overview

The backend uses a containerized multi-service architecture:

- **Web Server**: Gunicorn WSGI + Whitenoise Static File Middleware
- **Database**: PostgreSQL 16 (UUID primary keys, indexed tables)
- **Cache & Channel Layer**: Redis 7
- **Task Queue**: Celery Worker + Celery Beat (periodic task scheduler)
- **API Specification**: OpenAPI 3.0 via `drf-spectacular` / Swagger UI

---

## ⚙️ Environment Variables Reference

Create a `.env` file in the `backend/` directory:

```env
# Core Django
SECRET_KEY=production-super-secret-key-change-in-prod
DEBUG=False
ALLOWED_HOSTS=api.blueteamers.io,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://arena.blueteamers.io,http://localhost:5173

# Database & Redis
DATABASE_URL=postgres://blueteamers_user:blueteamers_password@blueteamers_db:5432/blueteamers_db
REDIS_URL=redis://blueteamers_redis:6379/0

# SimpleJWT Lifetimes
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
```

---

## 🚀 Deployment Steps (Docker Compose)

### 1. Build and Start All Services
```bash
docker-compose up -d --build
```

### 2. Apply Database Migrations
```bash
docker-compose exec blueteamers_api python manage.py migrate
```

### 3. Seed Initial Demo Data (Events, Challenges, Evidence, Questions, Admins)
```bash
docker-compose exec blueteamers_api python manage.py seed_demo
```

### 4. Collect Static Files for Whitenoise
```bash
docker-compose exec blueteamers_api python manage.py collectstatic --no-input
```

---

## 🏥 Health Check & Monitoring

Verify application health by sending a `GET` request to:

```http
GET /api/health/
```

Expected Response (`200 OK`):
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-07-28T22:47:29Z",
    "components": {
      "database": { "status": "healthy", "engine": "postgresql" },
      "cache": { "status": "healthy", "backend": "redis/memory" },
      "storage": { "status": "healthy", "writable": true }
    }
  },
  "message": "Application health check passed."
}
```

---

## 🔐 Production Security Checklist

- [x] **`DEBUG = False`** enforced in `config/settings/production.py`.
- [x] **JWT Token Blacklisting**: Active via SimpleJWT token blacklist model.
- [x] **Rate Limiting**: Throttling configured for `/api/v1/auth/login/` (5/min) and `/api/v1/arena/verify-code/` (10/min).
- [x] **Security Headers**: `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = 'DENY'` active.
- [x] **Public Serializer Sanitization**: Ground truth answers and explanations stripped on student endpoints.
- [x] **Audit Logging**: All admin actions logged in `AuditLog`.
