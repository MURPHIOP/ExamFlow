# API Contract (Foundation)

## Base URLs
- Local API root: `http://localhost:8000`
- Versioned API base: `http://localhost:8000/api/v1`

## Standard Response Format
```json
{
  "success": true,
  "message": "Human readable message",
  "data": {},
  "meta": {}
}
```

`data` and `meta` are optional depending on endpoint type.

## Current Endpoints
- `GET /`
- `GET /health`
- `GET /api/v1/health`

Health response:
```json
{
  "success": true,
  "message": "ExamFlow API is running",
  "service": "ExamFlow by M.B. Technosoft Pvt Ltd",
  "version": "0.1.0",
  "environment": "development"
}
```

## Implemented Route Groups
- `/api/v1/auth` - Authentication (login, register)
- `/api/v1/exam-sessions` - Exam session management
- `/api/v1/applications` - Application workflows

## Planned Route Groups (Future)
- `/api/v1/users`
- `/api/v1/payments`
- `/api/v1/admit-cards`
- `/api/v1/results`
- `/api/v1/certificates`
- `/api/v1/reports`
- `/api/v1/ai`

---

# Application API Contract

## Authentication
All application endpoints require JWT token in Authorization header:
```
Authorization: Bearer <access_token>
```

## Student Routes

### Create Application (Draft)
**POST** `/api/v1/applications/student`

**Access**: Student only

**Request Body**:
```json
{
  "exam_session_id": "uuid",
  "subject_id": "uuid",
  "grade_level_id": "uuid (optional)",
  "preferred_centre_id": "uuid (optional)",
  "student_notes": "string (optional)"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Application draft created successfully",
  "data": {
    "id": "uuid",
    "application_number": "MBT-BSP-2026-000128",
    "status": "draft",
    "fee_amount": "500.00"
  }
}
```

### List My Applications
**GET** `/api/v1/applications/my?page=1&page_size=20&status=draft&exam_session_id=uuid`

**Access**: Student only

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 20)
- `status` (string, optional): draft, submitted, payment_pending, under_verification, correction_required, approved, rejected
- `exam_session_id` (uuid, optional)

**Response**:
```json
{
  "success": true,
  "message": "Applications retrieved successfully",
  "data": {
    "items": [
      {
        "id": "uuid",
        "application_number": "MBT-BSP-2026-000128",
        "student_id": "uuid",
        "exam_session_id": "uuid",
        "subject_id": "uuid",
        "status": "draft",
        "fee_amount": "500.00",
        "submitted_at": null,
        "approved_at": null,
        "created_at": "2026-05-08T10:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

### Get My Application
**GET** `/api/v1/applications/my/{application_id}`

**Access**: Student owner only

**Response**:
```json
{
  "success": true,
  "message": "Application retrieved successfully",
  "data": {
    "id": "uuid",
    "application_number": "MBT-BSP-2026-000128",
    "student_id": "uuid",
    "institution_id": null,
    "exam_session_id": "uuid",
    "subject_id": "uuid",
    "grade_level_id": "uuid",
    "preferred_centre_id": "uuid",
    "allocated_centre_id": null,
    "status": "draft",
    "fee_amount": "500.00",
    "admin_remarks": null,
    "rejection_reason": null,
    "correction_notes": null,
    "student_notes": "My notes",
    "submitted_at": null,
    "verified_at": null,
    "approved_at": null,
    "rejected_at": null,
    "created_at": "2026-05-08T10:00:00Z",
    "updated_at": "2026-05-08T10:00:00Z"
  }
}
```

### Update My Application
**PATCH** `/api/v1/applications/my/{application_id}`

**Access**: Student owner only, only in draft or correction_required status

**Request Body**:
```json
{
  "subject_id": "uuid (optional)",
  "grade_level_id": "uuid (optional)",
  "preferred_centre_id": "uuid (optional)",
  "student_notes": "string (optional)"
}
```

**Response**: Same as Get My Application

### Submit My Application
**POST** `/api/v1/applications/my/{application_id}/submit`

**Access**: Student owner only

**Request Body**:
```json
{
  "confirmation": true,
  "declaration_accepted": true
}
```

**Response**:
```json
{
  "success": true,
  "message": "Application submitted successfully",
  "data": {
    "id": "uuid",
    "application_number": "MBT-BSP-2026-000128",
    "status": "payment_pending",
    "fee_amount": "500.00",
    "submitted_at": "2026-05-08T10:00:00Z"
  }
}
```

**Status Transition Logic**:
- If `fee_amount > 0`: status becomes `payment_pending`
- If `fee_amount == 0`: status becomes `submitted`

---

## Institution Routes

### Create Application for Student
**POST** `/api/v1/applications/institution`

**Access**: Institution only (must be APPROVED status)

**Request Body**:
```json
{
  "student_user_id": "uuid (optional)",
  "existing_student_profile_id": "uuid (optional)",
  "student_data": {
    "full_name": "string (required if creating new)",
    "email": "string (optional)",
    "phone": "string (optional)",
    "date_of_birth": "string (optional)",
    "gender": "male|female|other|prefer_not_to_say (optional)",
    "guardian_name": "string (optional)",
    "guardian_phone": "string (optional)",
    "address_line_1": "string (optional)",
    "address_line_2": "string (optional)",
    "district": "string (optional)",
    "state": "string (optional)",
    "pincode": "string (optional)"
  },
  "exam_session_id": "uuid",
  "subject_id": "uuid",
  "grade_level_id": "uuid (optional)",
  "preferred_centre_id": "uuid (optional)",
  "institution_notes": "string (optional)"
}
```

**Note**: Provide EITHER `student_user_id` OR `existing_student_profile_id` OR `student_data`

**Response** (201 Created): Same as student create

### List Institution Applications
**GET** `/api/v1/applications/institution?page=1&page_size=20&status=draft&exam_session_id=uuid&subject_id=uuid`

**Access**: Institution only

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 20)
- `status` (string, optional)
- `exam_session_id` (uuid, optional)
- `subject_id` (uuid, optional)

**Response**: Same as student list

### Get Institution Application
**GET** `/api/v1/applications/institution/{application_id}`

**Access**: Institution owner only

**Response**: Same as get my application

### Update Institution Application
**PATCH** `/api/v1/applications/institution/{application_id}`

**Access**: Institution owner only, only in draft or correction_required status

**Request Body**: Same as student update

**Response**: Same as get application

### Submit Institution Application
**POST** `/api/v1/applications/institution/{application_id}/submit`

**Access**: Institution owner only

**Request Body**:
```json
{
  "confirmation": true,
  "declaration_accepted": true
}
```

**Response**: Same as student submit

---

## Admin Routes

### List All Applications
**GET** `/api/v1/applications/admin?page=1&page_size=20&search=&status=&exam_session_id=&subject_id=&grade_level_id=&institution_id=&district=`

**Access**: Admin or Super Admin only

**Query Parameters**:
- `page` (int, default: 1)
- `page_size` (int, default: 20)
- `search` (string, optional): searches application number, student name, email, phone
- `status` (string, optional)
- `exam_session_id` (uuid, optional)
- `subject_id` (uuid, optional)
- `grade_level_id` (uuid, optional)
- `institution_id` (uuid, optional)
- `preferred_centre_id` (uuid, optional)
- `allocated_centre_id` (uuid, optional)
- `district` (string, optional): filters by student's district

**Response**: Same as list applications

### Get Application
**GET** `/api/v1/applications/admin/{application_id}`

**Access**: Admin or Super Admin only

**Response**: Same as get application

### Mark Under Verification
**POST** `/api/v1/applications/admin/{application_id}/mark-under-verification`

**Access**: Admin or Super Admin only

**Allowed From Statuses**: `submitted`, `payment_pending`, `correction_required`

**Request Body**: (empty)

**Response**:
```json
{
  "success": true,
  "message": "Application marked under verification successfully",
  "data": {
    "id": "uuid",
    "application_number": "MBT-BSP-2026-000128",
    "status": "under_verification",
    "verified_at": "2026-05-08T10:00:00Z"
  }
}
```

### Request Correction
**POST** `/api/v1/applications/admin/{application_id}/request-correction`

**Access**: Admin or Super Admin only

**Allowed From Statuses**: `under_verification`

**Request Body**:
```json
{
  "correction_notes": "Please correct spelling of student name",
  "due_date": "2026-05-15 (optional)"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Correction requested successfully",
  "data": {
    "id": "uuid",
    "status": "correction_required",
    "correction_notes": "Please correct spelling of student name"
  }
}
```

### Approve Application
**POST** `/api/v1/applications/admin/{application_id}/approve`

**Access**: Admin or Super Admin only

**Allowed From Statuses**: `under_verification`

**Request Body**:
```json
{
  "admin_remarks": "Application looks good (optional)",
  "allocated_centre_id": "uuid (optional, centre allocation comes later)"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Application approved successfully",
  "data": {
    "id": "uuid",
    "status": "approved",
    "approved_at": "2026-05-08T10:00:00Z"
  }
}
```

### Reject Application
**POST** `/api/v1/applications/admin/{application_id}/reject`

**Access**: Admin or Super Admin only

**Allowed From Statuses**: `under_verification`, `correction_required`

**Request Body**:
```json
{
  "rejection_reason": "Required documents not submitted"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Application rejected successfully",
  "data": {
    "id": "uuid",
    "status": "rejected",
    "rejection_reason": "Required documents not submitted",
    "rejected_at": "2026-05-08T10:00:00Z"
  }
}
```

---

## Document Metadata Routes

### Create Document Metadata
**POST** `/api/v1/applications/{application_id}/documents`

**Access**: Application owner (student/institution) or Admin

**Note**: This is metadata-only. Actual file upload/cloud storage integration comes later.

**Request Body**:
```json
{
  "document_type": "ID_PROOF|ADDRESS_PROOF|MARK_SHEET|OTHER",
  "file_name": "student_id.pdf (optional)",
  "file_url": "s3://bucket/path/to/file or local://path",
  "mime_type": "application/pdf (optional)",
  "file_size_bytes": 102400 (optional)
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Document metadata created successfully",
  "data": {
    "id": "uuid",
    "document_type": "ID_PROOF",
    "file_name": "student_id.pdf",
    "file_url": "s3://bucket/path/to/file",
    "mime_type": "application/pdf",
    "file_size_bytes": 102400,
    "status": "uploaded",
    "created_at": "2026-05-08T10:00:00Z"
  }
}
```

### List Application Documents
**GET** `/api/v1/applications/{application_id}/documents?page=1&page_size=20`

**Access**: Application owner or Admin

**Response**:
```json
{
  "success": true,
  "message": "Documents retrieved successfully",
  "data": {
    "items": [
      {
        "id": "uuid",
        "document_type": "ID_PROOF",
        "file_name": "student_id.pdf",
        "file_url": "s3://bucket/path/to/file",
        "mime_type": "application/pdf",
        "file_size_bytes": 102400,
        "created_at": "2026-05-08T10:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Exam fee is not configured for this session/subject/grade"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Application not found"
}
```

### 422 Unprocessable Entity
```json
{
  "success": false,
  "message": "Application cannot be edited in payment_pending status. Editable statuses: [draft, correction_required]"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Internal server error"
}
```

---

## Application Status Lifecycle (Current Step)

```
draft
  ↓
submitted (if fee = 0)
  ↓
payment_pending (if fee > 0)
  ↓
under_verification (admin manual mode or after payment)
  ├─→ correction_required (admin requests correction)
  │   ├─→ submitted (student resubmits)
  │   │   ↓
  │   │   under_verification
  │   │
  │   └─→ rejected (admin rejects)
  │
  ├─→ approved
  │
  └─→ rejected
```

**Note**: `paid` status will be set by payment module when Razorpay integration is complete.

---

## Permission Matrix

| Operation | Student | Institution | Admin | Super Admin | Public |
|-----------|---------|-------------|-------|------------|--------|
| Create own application | ✓ | - | - | - | - |
| Create app for student | - | ✓ | - | - | - |
| View own applications | ✓ | ✓ | - | - | - |
| View all applications | - | - | ✓ | ✓ | - |
| Update draft app | ✓ | ✓ | - | - | - |
| Submit application | ✓ | ✓ | - | - | - |
| Mark under verification | - | - | ✓ | ✓ | - |
| Request correction | - | - | ✓ | ✓ | - |
| Approve application | - | - | ✓ | ✓ | - |
| Reject application | - | - | ✓ | ✓ | - |
| Add document metadata | ✓ | ✓ | ✓ | ✓ | - |
