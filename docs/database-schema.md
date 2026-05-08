# Database Schema (Implemented Foundation)

This document summarizes the implemented backend database foundation in `apps/api`.

## ORM and Migration Stack
- SQLAlchemy 2.x typed ORM (`Mapped`, `mapped_column`, `relationship`)
- PostgreSQL-oriented schema with UUID primary keys
- Alembic configured in `apps/api/alembic` with initial migration
- Seed script available at `python -m app.db.seed`

## Reusable Model Mixins
- `UUIDPrimaryKeyMixin`
- `TimestampMixin`
- `SoftDeleteMixin`
- `AuditMetadataMixin` (available for future audit creator/updater metadata)

## Implemented Tables
- `users`
- `student_profiles`
- `institutions`
- `exam_sessions`
- `subjects`
- `grade_levels`
- `exam_fees`
- `exam_centres`
- `applications`
- `payments`
- `documents`
- `centre_allocations`
- `admit_cards`
- `marks_entries`
- `results`
- `certificates`
- `support_requests`
- `notifications`
- `audit_logs`
- `ai_jobs`
- `ai_review_items`

## Implemented Enums
- `UserRole`
- `Gender`
- `InstitutionStatus`
- `ExamSessionStatus`
- `ApplicationStatus`
- `PaymentStatus`
- `PaymentProvider`
- `DocumentType`
- `DocumentStatus`
- `CentreStatus`
- `ResultStatus`
- `CertificateStatus`
- `SupportStatus`
- `NotificationChannel`
- `NotificationStatus`
- `AIReviewStatus`
- `AIJobType`
- `AIJobStatus`

## Constraints and Indexing Highlights
- UUID PKs on all major entities
- Unique constraints on identifiers like:
  - `users.email`, `users.phone`
  - `exam_sessions.code`
  - `subjects.code`
  - `applications.application_number`
  - payment provider references and receipt fields
  - `admit_cards.roll_number`
  - `certificates.certificate_number`
- Composite unique constraints:
  - `grade_levels(subject_id, code)`
  - `exam_fees(exam_session_id, subject_id, grade_level_id)`
- Indexed high-query columns for status, foreign keys, and lookup codes

## Seed Data Included
- Super admin user
- Admin user
- Core subjects (Music, Dance, Drawing, Painting, Karate, Tabla, Vocal, Instrumental, Rabindra Sangeet, Classical Dance, Fine Arts)
- One exam session: `Annual Examination 2026` (`BSP-ANNUAL-2026`)
- Five centres: Kolkata, Howrah, Bardhaman, Siliguri, Durgapur
- Grade levels for selected subjects and baseline exam fees

## Commands (from `apps/api`)
1. `python3.11 -m venv .venv`
2. `source .venv/bin/activate` (Windows: `.venv\Scripts\Activate.ps1`)
3. `pip install -r requirements.txt`
4. `alembic upgrade head`
5. `python -m app.db.seed`
6. `pytest`

## Notes
- This step focuses on schema, migration, enums, and seed foundation only.
- Auth endpoints, payment processing logic, AI business workflows, and PDF generation are intentionally deferred.
