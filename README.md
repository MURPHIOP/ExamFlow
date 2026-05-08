# ExamFlow by M.B. Technosoft Pvt Ltd

ExamFlow is a full-scale examination automation platform for cultural, academic, art, and skill-based examination bodies such as Bangiya Sangeet Parishad.

## Problem Statement
Many examination organizations still rely on manual operations for form entry, verification, admit card preparation, marks entry, result publishing, and certificate generation. This causes delays, data-entry errors, and heavy administrative workload.

This repository contains the **monorepo foundation and base setup only**.

## Company
**M.B. Technosoft Pvt Ltd**

## Tech Stack
- Frontend: Next.js (App Router), TypeScript, Tailwind CSS, next-themes, Framer Motion, Recharts, TanStack Query
- Backend: FastAPI, Pydantic, SQLAlchemy 2.x, Alembic
- Database: PostgreSQL
- Tooling: npm workspaces, ESLint, Prettier, pytest, Docker Compose

## Monorepo Structure

```text
examflow-mbtechnosoft/
├── apps/
│   ├── web/
│   └── api/
├── packages/
│   ├── shared/
│   ├── ui/
│   └── config/
├── docs/
├── infra/
├── .env.example
├── docker-compose.yml
├── package.json
└── README.md
```

## Local Setup

### 1) Clone and configure env
```bash
cp .env.example .env
```

### 2) Install frontend dependencies
```bash
npm install
```

### 3) Run frontend (Next.js)
```bash
npm run dev:web
```

### 4) Setup backend Python environment
macOS/Linux:
```bash
cd apps/api
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env
```

Windows (PowerShell):
```powershell
cd apps/api
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ../../.env.example .env
```

### 5) Run PostgreSQL using Docker
```bash
docker compose up -d postgres
```
Optional pgAdmin:
```bash
docker compose --profile admin up -d pgadmin
```

### 6) Run Alembic migration (from apps/api)
```bash
alembic revision --autogenerate -m "initial database schema"
alembic upgrade head
```

### 7) Seed development data (from apps/api)
```bash
python -m app.db.seed
```

This seeds:
- **Super Admin**: `superadmin@mbtechnosoft.com` / `Admin@12345`
- **Admin**: `admin@mbtechnosoft.com` / `Admin@12345`
- **Examiner**: `examiner@mbtechnosoft.com` / `Admin@12345`
- Exam subjects, sessions, centres, grade levels, and fees

### 8) Run backend API (from apps/api)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access Swagger API docs: `http://localhost:8000/docs`

### 9) Test authentication endpoints
See [auth-curl-examples.md](docs/auth-curl-examples.md) for complete examples.

Quick test:

```bash
# Register student
curl -X POST "http://localhost:8000/api/v1/auth/register/student" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Student",
    "email": "test@example.com",
    "password": "Test@12345",
    "confirm_password": "Test@12345"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "test@example.com",
    "password": "Test@12345"
  }'

# Get current user (use token from login response)
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>"

# Test admin-only route (will fail for student)
curl -X GET "http://localhost:8000/api/v1/protected/admin-only" \
  -H "Authorization: Bearer <access_token>"
```

### 10) Run backend tests (from apps/api)
```bash
pytest
```

Current test coverage:
- Password hashing and verification (24 tests)
- JWT token creation and decoding
- Schema validation for registration/login
- User response schemas
- Password change validation


## Current Completed Features
- Monorepo structure with apps/packages/docs/infra
- Next.js frontend base app with premium dashboard foundation UI
- Light and dark mode with next-themes
- Shared constants package
- FastAPI backend base initialization and health endpoints (`/`, `/health`, `/api/v1/health`)
- Global exception handling and env-based CORS setup
- Complete SQLAlchemy database model foundation with 21 models, enums, relationships, indexes, UUID PKs, and soft-delete/timestamp mixins
- Alembic setup with initial database schema migration verified (661 lines SQL generated)
- Development seed script with hashed passwords for super admin, admin, and examiner users
- Backend test coverage for health and database model metadata/imports (7 tests, all passing)
- Basic Docker Compose for local PostgreSQL
- **Authentication & Authorization Layer** ✅
  - JWT-based authentication with HS256 algorithm
  - Password hashing with PBKDF2-SHA256 (260,000 iterations) - cross-platform compatible
  - Role-Based Access Control (RBAC) for 6 roles: super_admin, admin, examiner, student, institution, guardian
  - Student registration endpoint with email/phone uniqueness validation
  - Institution registration endpoint (creates pending approval status)
  - Login endpoint (email or phone + password) with last_login tracking
  - Get current user endpoint (`/auth/me`)
  - Logout endpoint (stateless JWT MVP)
  - Protected routes with role-based access (super-admin-only, admin-only, authenticated-only)
  - Comprehensive auth test suite (24 unit tests covering schemas, JWT, password hashing)
  - Audit logging for registration, login success/fail, password changes
  - Transactional user + profile creation (Student/Institution) with rollback safety
  - User repository and auth service layers following clean architecture
  - Dependency injection for RBAC enforcement
  - OpenAPI/Swagger documentation with auth routes
- Architecture/security/deployment/docs updated for current backend status

## Intentionally Not Implemented Yet
- Payment gateway business flow (Razorpay order/verify/webhooks)
- AI/ML business workflow execution logic
- PDF generation pipelines (receipt/admit card/certificate)
- Full dashboard APIs and production analytics endpoints
- Password reset flow
- Email verification flow
- Token refresh endpoint (JWT refresh strategy deferred for MVP)
- Server-side token blacklisting (stateless JWT MVP)

## Next Build Step
Core exam setup APIs (exam sessions, subjects, grades, fees management endpoints).

## Documentation

### API Guides
- [Authentication & Authorization API](docs/auth-api.md) - Complete JWT auth system documentation
- [Authentication cURL Examples](docs/auth-curl-examples.md) - Ready-to-use curl commands for testing all auth endpoints

### Deployment & Architecture
See `docs/` directory for detailed system design, security plan, and technical specifications
