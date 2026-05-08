# Architecture Blueprint (Foundation)

## Product Vision
ExamFlow automates end-to-end examination workflows for cultural, art, and skill-based boards, reducing manual effort, errors, and turnaround time.

## Main Roles
- Student
- Guardian
- Institution
- Admin Employee
- Examiner
- Super Admin

## Main Modules
- Public website
- Authentication and role-based access
- Student, Institution, Admin, Super Admin dashboards
- Exam sessions, subjects/art forms, applications
- Payments, receipts, verification, centres, roll numbers
- Admit cards, marks, results, certificates
- AI-assisted admin productivity and anomaly flags
- Reports, exports, notifications, audit logs

## High-Level Architecture
- Frontend: Next.js App Router with shared design system and theme tokens
- Backend: FastAPI modular API with service/repository boundaries
- Database: PostgreSQL
- Storage: Cloudinary or S3-compatible
- Async tasks: worker-ready architecture for documents/notifications (future)
- Observability: structured logging, health endpoints, and deployment checks

## Build Phases
1. Monorepo foundation (current)
2. Database schema + migrations
3. Auth + RBAC
4. Application lifecycle and verification
5. Payments and receipts
6. Centre allocation + admit cards
7. Marks, results, certificates
8. AI/ML assist modules
9. Hardening, scale, and deployment
