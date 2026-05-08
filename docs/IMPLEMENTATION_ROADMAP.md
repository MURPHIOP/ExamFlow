# ExamFlow - Complete Implementation Roadmap

**Last Updated:** 8 May 2026  
**Project:** ExamFlow by M.B. Technosoft Pvt Ltd  
**Status:** Phase A Complete, Ready for Phase B+

---

## PROJECT COMPLETION STATUS

### ✅ COMPLETED PHASES

**Phase A: Razorpay Payment + Receipt Workflow** [100% Complete]
- ✅ Payment order creation
- ✅ Payment signature verification (HMAC SHA256)
- ✅ Receipt number generation (MBT-RCPT-{YEAR}-{SEQUENCE})
- ✅ Webhook handling (idempotent)
- ✅ Application status transition (payment_pending → paid)
- ✅ Admin payment viewing
- ✅ Comprehensive tests
- ✅ Documentation

**Status:** Production-ready for integration testing

---

## REMAINING PHASES ROADMAP

### Priority 1: CRITICAL FOUNDATION (Complete Before Public Beta)

#### Phase B: Document Generation Foundation [NEXT]
**Goal:** Create reusable document service architecture for PDFs, QR codes, storage

**Time Estimate:** 2-3 hours

**Files to Create:**
- `app/services/pdf_generation_service.py` - HTML to PDF conversion
- `app/services/qr_code_service.py` - QR code generation (abstracted in document_service.py)
- `app/services/storage_service.py` - Multi-provider storage (local/Cloudinary/S3)
- `app/schemas/document.py` - Document metadata schemas
- `app/repositories/document_repository.py` - Already exists, verify structure
- `app/api/v1/documents.py` - Document download/retrieve routes
- `app/tests/test_document_generation.py` - Tests

**Key Implementation:**
```python
# Use WeasyPrint or Playwright for PDF generation
# Local storage for development (apps/api/storage/documents/)
# Cloud storage abstraction for production
# QR codes embedded in PDFs
# Configurable storage provider via STORAGE_PROVIDER env var
```

**Routes to Implement:**
```
GET    /api/v1/documents/{document_id}
GET    /api/v1/documents/{document_id}/download
POST   /api/v1/documents/admin/regenerate/{document_id}
POST   /api/v1/verify/document/{qr_code}
```

---

#### Phase C: Receipt PDF Generation [DEPENDS ON B]
**Goal:** Generate payment receipt PDFs automatically after payment success

**Time Estimate:** 1-2 hours

**Files to Modify:**
- `app/services/payment_service.py` - Trigger receipt PDF generation after payment_verified
- `app/models/payment.py` - Add receipt_document_id if needed
- `app/templates/receipt.html` - Template for receipt PDF

**Files to Create:**
- `app/services/receipt_generation_service.py` - Orchestrate receipt PDF + metadata
- `app/migrations/xxx_add_receipt_document_id_to_payment.py` - Optional: link document

**Key Implementation:**
- After payment verified, call receipt_generation_service.generate_receipt()
- Create Document metadata record
- Store PDF to storage service
- Link to Payment record
- Make accessible via GET /api/v1/payments/{payment_id}/receipt/download

---

#### Phase D: Exam Centre Allocation + Roll Number [DEPENDS ON B, C]
**Goal:** Admins allocate exam centres to applications after payment verification

**Time Estimate:** 2-3 hours

**Models to Add:**
- `CentreAllocation` - Store allocation details
- Update `Application` - Add centre_allocation_id, roll_number fields

**Files to Create:**
- `app/schemas/centre_allocation.py`
- `app/repositories/centre_allocation_repository.py`
- `app/services/centre_allocation_service.py`
- `app/services/roll_number_service.py`
- `app/api/v1/centre_allocations.py`
- `app/tests/test_centre_allocation.py`

**Roll Number Format:**
```
MBT-{SUBJECT_CODE}-{CENTRE_CODE}-{YEAR}-{SEQUENCE}
Example: MBT-BSP-MBT001-2026-000001
```

**Routes:**
```
GET    /api/v1/centre-allocations/admin
POST   /api/v1/centre-allocations/admin/{application_id}/allocate
POST   /api/v1/centre-allocations/admin/{application_id}/auto-recommend
PATCH  /api/v1/centre-allocations/admin/{allocation_id}
GET    /api/v1/centre-allocations/admin/centres/{centre_id}/capacity
```

**Key Rules:**
- Only Admin/Super Admin
- Application must be approved or paid
- Centre must have capacity
- Roll number generated
- Application status → centre_allocated
- Audit log: CENTRE_ALLOCATED

---

#### Phase E: Admit Card Generation [DEPENDS ON D]
**Goal:** Generate admit cards for centre-allocated applications

**Time Estimate:** 2-3 hours

**Models to Add:**
- `AdmitCard` - Store admit card details
- `Application` - Add admit_card_id field

**Files to Create:**
- `app/schemas/admit_card.py`
- `app/repositories/admit_card_repository.py`
- `app/services/admit_card_service.py`
- `app/api/v1/admit_cards.py`
- `app/tests/test_admit_cards.py`
- `app/templates/admit_card.html`

**Routes:**
```
POST   /api/v1/admit-cards/admin/{application_id}/generate
POST   /api/v1/admit-cards/admin/bulk-generate
GET    /api/v1/admit-cards/my
GET    /api/v1/admit-cards/my/{admit_card_id}
GET    /api/v1/admit-cards/admin
GET    /api/v1/admit-cards/admin/{admit_card_id}
GET    /api/v1/verify/admit-card/{qr_code_value}
```

**Key Features:**
- Admin generates, student/institution downloads own
- PDF with QR code
- Application status → admit_card_generated
- Public verification endpoint (safe fields only)
- Prevent duplicate active admit cards

---

#### Phase F: Marks Entry + Result Publishing [DEPENDS ON E]
**Goal:** Examiners enter marks, admins publish results

**Time Estimate:** 3-4 hours

**Models to Add:**
- `MarksEntry` - Store marks for each application
- `Result` - Store published result with grade calculation

**Files to Create:**
- `app/schemas/marks.py`
- `app/schemas/result.py`
- `app/repositories/marks_repository.py`
- `app/repositories/result_repository.py`
- `app/services/marks_service.py`
- `app/services/result_service.py`
- `app/api/v1/marks.py`
- `app/api/v1/results.py`
- `app/tests/test_results.py`

**Routes:**
```
POST   /api/v1/marks/admin/{application_id}
PATCH  /api/v1/marks/admin/{marks_entry_id}
GET    /api/v1/marks/admin

POST   /api/v1/results/admin/{application_id}/prepare
POST   /api/v1/results/admin/{result_id}/publish
POST   /api/v1/results/admin/bulk-publish
GET    /api/v1/results/my
GET    /api/v1/results/my/{result_id}
GET    /api/v1/results/search (public, with verification)
GET    /api/v1/results/admin
GET    /api/v1/results/admin/{result_id}
```

**Grade Calculation:**
```
90+    → A+
80-89  → A
70-79  → B+
60-69  → B
50-59  → C
<50    → Fail
```

**Key Rules:**
- Only Admin/Super Admin/Examiner can enter marks
- Application must be admit_card_generated
- Marks remain draft until published
- Result publish changes application status → result_published
- Public search requires roll/app number + DOB or phone
- No private data exposed publicly

---

#### Phase G: Certificate Generation + Verification [DEPENDS ON F]
**Goal:** Generate digitally verifiable certificates after result publication

**Time Estimate:** 2-3 hours

**Models to Add:**
- `Certificate` - Store certificate details

**Files to Create:**
- `app/schemas/certificate.py`
- `app/repositories/certificate_repository.py`
- `app/services/certificate_number_service.py`
- `app/services/certificate_service.py`
- `app/api/v1/certificates.py`
- `app/tests/test_certificates.py`
- `app/templates/certificate.html`

**Certificate Number Format:**
```
MBT-CERT-BSP-{YEAR}-{6_DIGIT_SEQUENCE}
Example: MBT-CERT-BSP-2026-000001
```

**Routes:**
```
POST   /api/v1/certificates/admin/{application_id}/generate
POST   /api/v1/certificates/admin/bulk-generate
GET    /api/v1/certificates/my
GET    /api/v1/certificates/my/{certificate_id}
GET    /api/v1/certificates/admin
GET    /api/v1/certificates/admin/{certificate_id}
POST   /api/v1/certificates/admin/{certificate_id}/revoke (Super Admin only)
GET    /api/v1/verify/certificate/{certificate_number} (public)
GET    /api/v1/verify/certificate/qr/{qr_code_value} (public)
```

**Key Rules:**
- Only Admin/Super Admin can generate
- Application must be result_published
- Do not generate if result failed (configurable)
- QR code + PDF
- Application status → certificate_issued
- Prevent duplicate active certificates
- Public verification shows valid/revoked/not found
- Revocation tracked (Super Admin audit only)

---

### Priority 2: FRONTEND INTEGRATION (Make Backend Testable)

#### Phase I: Frontend API Client + Auth Integration
**Goal:** Connect frontend to backend safely, set up auth flow

**Time Estimate:** 3-4 hours

**Files to Create:**
- `apps/web/lib/api-client.ts` - Axios wrapper with JWT handling
- `apps/web/lib/auth-context.tsx` - Auth state management
- `apps/web/hooks/use-auth.ts` - Custom auth hook
- `apps/web/hooks/use-current-user.ts` - Current user hook
- `apps/web/components/protected-route.tsx` - Route protection
- `apps/web/lib/validators/` - Zod schemas for form validation

**Implementation:**
```typescript
// api-client.ts
- Use NEXT_PUBLIC_API_URL environment variable
- Axios instance with JWT interceptor
- Auto-refresh token on expiry
- Error handling with toast notifications
- No secrets in client code

// Auth context
- Store JWT in httpOnly cookies if possible
- Fallback to localStorage
- Provide login, register, logout functions
- Handle role-based redirects
- Prevent direct auth page access when logged in

// Hooks
- useAuth() - Get current auth state
- useCurrentUser() - Fetch and cache current user
- useProtectedRoute() - Require authentication
```

**Test:**
```bash
cd apps/web
npm run lint
npm run build
```

---

#### Phase J: Premium Frontend Design System
**Goal:** Create elite, professional UI matching specification

**Time Estimate:** 4-5 hours

**Components to Create:**
- `components/layout/Dashboard-Shell.tsx` - Main layout
- `components/layout/AppSidebar.tsx` - Left sidebar
- `components/layout/TopNavbar.tsx` - Top navigation
- `components/common/StatCard.tsx` - KPI card
- `components/common/ChartCard.tsx` - Chart container
- `components/common/DataTable.tsx` - Reusable table
- `components/common/StatusBadge.tsx` - Status indicator
- `components/common/PageHeader.tsx` - Page title
- `components/forms/FormSection.tsx` - Form wrapper
- `components/states/EmptyState.tsx` - Empty state
- `components/states/ErrorState.tsx` - Error display
- `components/states/LoadingSkeleton.tsx` - Skeleton loader
- `components/dialogs/ConfirmDialog.tsx` - Confirmation
- `components/theme/ThemeToggle.tsx` - Dark/light mode
- `components/role/RoleGuard.tsx` - Role-based visibility

**Design:**
- Left sidebar with navigation
- Top navbar with profile dropdown, notifications
- Violet/indigo primary color
- CSS variables for theming
- Responsive mobile navigation
- Professional neutral backgrounds
- Light/dark mode with next-themes
- Accessible contrast ratios
- Polished forms and inputs
- Modal and dialog system

---

### Priority 3: STUDENT & INSTITUTION DASHBOARDS (Make Platform Usable)

#### Phase L: Student Dashboard Frontend
**Goal:** Students can apply, pay, download documents

**Time Estimate:** 3-4 hours

**Routes:**
```
/student
/student/profile
/student/applications
/student/applications/new
/student/applications/[id]
/student/payments
/student/receipts
/student/admit-cards
/student/results
/student/certificates
/student/support
```

**Key Pages:**
- New application form (session, subject, grade selection)
- Application list (filters by status)
- Create payment order
- Razorpay checkout integration
- Verify payment
- Download receipt/admit-card/certificate
- View result
- Support request form

---

#### Phase M: Institution Dashboard Frontend
**Goal:** Institutions manage student applications in bulk

**Time Estimate:** 3-4 hours

**Routes:**
```
/institution
/institution/profile
/institution/students
/institution/applications
/institution/applications/new
/institution/bulk-upload
/institution/payments
/institution/admit-cards
/institution/results
/institution/certificates
/institution/reports
```

---

#### Phase N: Admin Dashboard Frontend
**Goal:** Admins verify applications, allocate centres, manage system

**Time Estimate:** 4-5 hours

**Routes:**
```
/admin
/admin/applications (list, filter, bulk actions)
/admin/applications/[id] (detail, verify, approve/reject)
/admin/payments (list all payments)
/admin/verification (pending verifications)
/admin/exam-sessions (CRUD)
/admin/subjects (CRUD)
/admin/grade-levels (CRUD)
/admin/exam-fees (CRUD)
/admin/exam-centres (CRUD, capacity management)
/admin/centre-allocation (allocate, recommend)
/admin/admit-cards (generate, bulk-generate)
/admin/marks (entry, bulk-upload)
/admin/results (prepare, publish, bulk-publish)
/admin/certificates (generate, bulk-generate, revoke)
/admin/ai-tools (various AI features)
/admin/reports (analytics, exports)
/admin/audit-logs (view all admin actions)
/admin/support (handle support requests)
```

---

#### Phase O: Super Admin Frontend
**Goal:** Super admins manage users, settings, system health

**Time Estimate:** 2-3 hours

**Routes:**
```
/super-admin
/super-admin/users (list, create, manage roles)
/super-admin/employees (staff management)
/super-admin/roles (role definitions)
/super-admin/settings (system configuration)
/super-admin/templates (email/SMS templates if implemented)
/super-admin/payment-settings (Razorpay config UI)
/super-admin/ai-settings (AI model configuration)
/super-admin/audit-logs (full system audit)
/super-admin/backups (database backups if implemented)
/super-admin/system-health (health checks, monitoring)
```

---

### Priority 4: PUBLIC WEBSITE & MARKETING

#### Phase K: Public Website
**Goal:** Professional landing page, public info pages

**Time Estimate:** 3-4 hours

**Pages:**
```
/ (homepage)
/about
/exam-notices
/subjects
/exam-sessions
/apply (public apply info)
/result (public result search with verification)
/verify/certificate (QR verification)
/verify/admit-card (QR verification)
/contact
/login
/register
```

---

### Priority 5: ADVANCED FEATURES (Post-MVP)

#### Phase H: AI/ML Admin Tools
**Goal:** AI-assisted admin operations (suggestions only, no auto-approval)

**Time Estimate:** 5-6 hours

**Features:**
- OCR-assisted legacy form digitization
- Duplicate detection (phone, email, DOB matching)
- Spelling correction suggestions
- Exam centre recommendation engine
- Anomaly detection (suspicious patterns)
- Result analytics and insights
- Admin assistant (natural language search)

**Key Rule:** AI only suggests/detects/summarizes. Humans approve everything.

---

#### Phase P: Reports + Exports
**Goal:** CSV/Excel exports, analytics dashboards

**Time Estimate:** 2-3 hours

**Routes:**
```
GET /api/v1/reports/admin/summary
GET /api/v1/reports/admin/applications/export
GET /api/v1/reports/admin/payments/export
GET /api/v1/reports/admin/results/export
GET /api/v1/reports/admin/certificates/export
```

---

#### Phase Q: Notifications
**Goal:** In-app notifications, eventually email/SMS

**Time Estimate:** 2-3 hours

**Events:**
- Application submitted
- Payment success
- Correction requested
- Application approved/rejected
- Admit card generated
- Result published
- Certificate issued

---

#### Phase R: Testing + Hardening
**Goal:** Fix remaining tests, security audit, performance optimization

**Time Estimate:** 3-4 hours

**Checklist:**
- Fix all remaining pytest errors
- 100% test pass rate
- Frontend build passes
- TypeScript strict mode
- No hydration mismatches
- RBAC enforced on all routes
- Ownership validated on all operations
- No secrets in code
- Comprehensive error handling

---

#### Phase S: Deployment
**Goal:** Production readiness, CI/CD, monitoring

**Time Estimate:** 3-4 hours

**Backend Deployment:**
- Railway/Render/DigitalOcean
- Environment variables configured
- Database migrations automated
- Email service configured (SendGrid/AWS SES)
- Error tracking (Sentry)
- APM monitoring (New Relic/Datadog)

**Frontend Deployment:**
- Vercel
- Environment variables configured
- Automatic deployments on push
- Preview deployments for PRs

---

## IMPLEMENTATION SEQUENCE

### Week 1 (Foundations)
1. Phase B: Document Generation Service ✓
2. Phase C: Receipt PDF Generation ✓
3. Phase D: Centre Allocation ✓

### Week 2 (Core Features)
4. Phase E: Admit Card Generation ✓
5. Phase F: Marks & Results ✓
6. Phase G: Certificates ✓

### Week 3 (Frontend Setup)
7. Phase I: Frontend API Client ✓
8. Phase J: Design System ✓

### Week 4 (Student/Institution)
9. Phase L: Student Dashboard ✓
10. Phase M: Institution Dashboard ✓

### Week 5 (Admin & Public)
11. Phase N: Admin Dashboard ✓
12. Phase K: Public Website ✓

### Week 6 (Advanced & Launch)
13. Phase H: AI Tools (optional for MVP)
14. Phase P: Reports (optional for MVP)
15. Phase Q: Notifications (optional for MVP)
16. Phase R: Testing ✓
17. Phase S: Deployment ✓

---

## DEVELOPMENT COMMANDS

### Start Backend
```bash
cd /Users/shreyan/Documents/examFlow-mbtechnosoft
docker-compose up -d
cd apps/api
alembic upgrade head
python -m uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd apps/web
npm run dev
```

### Run Backend Tests
```bash
cd apps/api
pytest -q
```

### Run Frontend Tests
```bash
cd apps/web
npm run lint
npm run build
```

---

## KEY TECHNICAL DECISIONS

1. **Database:** PostgreSQL with SQLAlchemy ORM + Alembic migrations
2. **PDF Generation:** WeasyPrint (primary) or Playwright (fallback)
3. **Storage:** Local for dev, Cloudinary/S3 abstraction for prod
4. **QR Codes:** qrcode library with PIL
5. **Frontend:** Next.js App Router + TypeScript + Tailwind
6. **Forms:** React Hook Form + Zod validation
7. **API Client:** Axios with JWT interceptor
8. **Theme:** next-themes with CSS variables
9. **Components:** ShadCN UI (customizable)
10. **Charts:** Recharts for analytics
11. **Notifications:** Sonner toast notifications

---

## SECURITY CHECKLIST

- [ ] All HMAC signatures verified before accepting payments
- [ ] Webhooks verified with signature
- [ ] No secrets in frontend code
- [ ] Ownership validated on all user-specific operations
- [ ] RBAC enforced on all admin routes
- [ ] No direct SQL injection possible (using ORM)
- [ ] File uploads validated if implemented
- [ ] CORS configured properly
- [ ] HTTPS only in production
- [ ] Database credentials in environment variables
- [ ] JWT tokens stored securely
- [ ] Password hashing (bcrypt/argon2)
- [ ] Rate limiting on auth endpoints
- [ ] Audit logs for all admin actions
- [ ] No production secrets in git

---

## PERFORMANCE TARGETS

- Backend API response: <200ms
- Payment processing: <500ms
- PDF generation: <2s
- Frontend Lighthouse score: >90
- Database queries: All paginated, no N+1

---

## MONITORING & OBSERVABILITY

- Application logs to stdout
- Error tracking (Sentry integration ready)
- Performance monitoring (APM ready)
- Health check endpoints
- Database query logging (dev only)
- Request/response logging

---

## FUTURE ENHANCEMENTS (Post-MVP)

1. Video proctored exams
2. Mobile app (React Native)
3. AI-powered exam difficulty calibration
4. Blockchain certificate verification
5. Payment plan/EMI options
6. Multi-language support
7. WhatsApp/SMS integration
8. Advanced analytics with ML
9. Candidate performance prediction
10. Exam question generation with GPT

---

## CONTACTS & SUPPORT

**Project Owner:** M.B. Technosoft Pvt Ltd  
**Framework:** FastAPI + Next.js  
**Database:** PostgreSQL 12+  
**Deployment:** Vercel + Railway/Render  
**Monitoring:** Sentry + New Relic  

---

**Last Updated:** 8 May 2026  
**Next Review:** After Phase B completion  
**Prepared by:** Senior Full-Stack Architect
