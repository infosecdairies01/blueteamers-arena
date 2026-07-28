# Blueteamers Arena — Backend (Phase 1)

Production-ready Django 5 REST Framework backend for **Blueteamers Arena**, implementing custom UUID User model, JWT authentication, RBAC (Super Admin, Admin permissions), Password Reset workflows, Service Layer & Repository pattern architecture, Docker, and OpenAPI Swagger documentation.

---

## Technical Features

- **Python 3.12 & Django 5.1**
- **Django REST Framework (DRF) 3.15**
- **Service Layer & Repository/Selector Architecture**
- **SimpleJWT Authentication** with Token Blacklisting & Refresh
- **Custom User Model** (`AbstractUser`) using **UUID Primary Keys**
- **Role-Based Access Control**:
  - `IsAdmin` (`ADMIN` or `SUPER_ADMIN` or `is_staff`)
  - `IsSuperAdmin` (`SUPER_ADMIN` or `is_superuser`)
- **Authentication Endpoints**:
  - `POST /api/v1/auth/login/`
  - `POST /api/v1/auth/token/refresh/`
  - `POST /api/v1/auth/logout/`
  - `POST /api/v1/auth/change-password/`
  - `POST /api/v1/auth/forgot-password/`
  - `POST /api/v1/auth/reset-password/`
  - `GET/PUT/PATCH /api/v1/auth/me/`
- **Swagger / OpenAPI Documentation**: `drf-spectacular` at `/api/schema/swagger-ui/`
- **Docker & Docker Compose Integration**

---

## Project Structure

```
backend/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── common/          # BaseModel, exception handlers, response wrappers
    ├── accounts/        # User model, Auth services, serializers, viewsets
    └── api/             # Versioned API routes (/api/v1/)
```

---

## Local Quick Start (Docker)

```bash
# Clone and enter backend directory
cd backend

# Copy environment variables
cp .env.example .env

# Start containers with Docker Compose
docker compose up --build -d

# Run migrations inside container
docker compose exec web python manage.py migrate

# Create a superadmin user
docker compose exec web python manage.py createsuperuser
```

API Documentation will be accessible at:
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **Redoc**: `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

---

## Running Unit Tests

```bash
docker compose exec web python manage.py test apps.accounts
```
