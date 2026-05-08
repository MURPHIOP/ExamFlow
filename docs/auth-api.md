# ExamFlow Authentication & Authorization API

## Overview

ExamFlow implements a complete JWT-based authentication and role-based access control (RBAC) system using FastAPI, SQLAlchemy ORM, and passlib.

## Security Architecture

### Password Hashing

- **Algorithm**: PBKDF2-SHA256 with 260,000 iterations
- **Rationale**: Cross-platform compatibility (works reliably on all platforms including macOS M1), proven security
- **Never stored**: Plain text passwords are never stored; only cryptographic hashes are persisted

### JWT Tokens

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Access Token Expiry**: 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Refresh Token Expiry**: 7 days (configurable via `REFRESH_TOKEN_EXPIRE_DAYS`)
- **Secret Key**: Loaded from `JWT_SECRET_KEY` environment variable (must be 32+ characters in production)

### Role-Based Access Control (RBAC)

Supported roles:
- `SUPER_ADMIN` - System administrator with full access
- `ADMIN` - Staff admin with broad permissions
- `EXAMINER` - Examiner with exam-related permissions (seeded, not publicly registered)
- `STUDENT` - Student user with student permissions
- `INSTITUTION` - Institution/Academy user with institutional permissions
- `GUARDIAN` - Guardian role (model exists for future use)

## API Endpoints

### Authentication Routes

Prefix: `/api/v1/auth`

#### POST /register/student
Register a new student user.

**Request Body:**
```json
{
  "full_name": "Shreyan Mitra",
  "email": "student@example.com",
  "phone": "9876543210",
  "password": "Student@12345",
  "confirm_password": "Student@12345",
  "date_of_birth": "2000-01-15",
  "gender": "Male",
  "guardian_name": "Guardian Name",
  "guardian_phone": "9876543211",
  "district": "Kolkata",
  "state": "West Bengal",
  "address": "123 Main St",
  "pincode": "700001"
}
```

**Validation:**
- `full_name`: Required, minimum 2 characters
- `email` or `phone`: At least one required
- `email`: Valid email format if provided
- `phone`: Minimum 10 digits if provided
- `password`: Minimum 8 characters
- `confirm_password`: Must match password
- `email` and `phone`: Must be unique globally

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Student registered successfully",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "student@example.com",
    "phone": "9876543210"
  }
}
```

**Error Responses:**
- `409 Conflict`: Email or phone already registered
- `422 Unprocessable Entity`: Validation failed

---

#### POST /register/institution
Register a new institution user.

**Request Body:**
```json
{
  "institution_name": "Kolkata Music Academy",
  "contact_person_name": "Admin Person",
  "email": "academy@example.com",
  "phone": "9876543211",
  "password": "Academy@12345",
  "confirm_password": "Academy@12345",
  "registration_number": "REG-001",
  "district": "Kolkata",
  "state": "West Bengal",
  "address": "456 Academy Rd",
  "pincode": "700001"
}
```

**Validation:** Same as student registration

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Institution registered successfully. Awaiting approval.",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "email": "academy@example.com",
    "phone": "9876543211",
    "institution_name": "Kolkata Music Academy"
  }
}
```

**Note:** Institution is created with `status=pending` and requires admin approval.

---

#### POST /login
Authenticate user with email or phone and password.

**Request Body:**
```json
{
  "identifier": "student@example.com",
  "password": "Student@12345"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "full_name": "Shreyan Mitra",
      "email": "student@example.com",
      "phone": "9876543210",
      "role": "student",
      "is_active": true,
      "is_verified": false
    }
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials (generic message, doesn't reveal if user exists)
- `403 Forbidden`: User account is inactive

---

#### GET /me
Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Current user retrieved",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "Shreyan Mitra",
    "email": "student@example.com",
    "phone": "9876543210",
    "role": "student",
    "is_active": true,
    "is_verified": false
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User is inactive

---

#### POST /logout
Logout user (client-side token deletion for JWT MVP).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout successful. Please delete the token from client storage."
}
```

**Note:** For JWT MVP, logout is stateless. Client must delete the token from local storage. Server-side token blacklisting is intentionally not implemented.

---

### Protected Routes (RBAC Test)

Prefix: `/api/v1/protected`

#### GET /me
Get current user (accessible to all authenticated users).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Current user retrieved",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "Shreyan Mitra",
    "role": "student"
  }
}
```

---

#### GET /admin-only
Admin or Super Admin only.

**Response (200 OK - if authorized):**
```json
{
  "success": true,
  "message": "You have admin access",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "full_name": "Admin Employee",
    "role": "admin"
  }
}
```

**Response (403 Forbidden - if not authorized):**
```json
{
  "detail": "Insufficient permissions"
}
```

---

#### GET /super-admin-only
Super Admin only.

**Response (200 OK - if authorized):**
```json
{
  "success": true,
  "message": "You have super admin access",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "full_name": "Super Admin",
    "role": "super_admin"
  }
}
```

---

## Development Credentials

**These are for local development only. Never use in production.**

### Super Admin
- Email: `superadmin@mbtechnosoft.com`
- Password: `Admin@12345`
- Role: `super_admin`

### Admin
- Email: `admin@mbtechnosoft.com`
- Password: `Admin@12345`
- Role: `admin`

### Examiner
- Email: `examiner@mbtechnosoft.com`
- Password: `Admin@12345`
- Role: `examiner`

## Security Features

### 1. Password Security
- Passwords hashed with PBKDF2-SHA256 (260,000 iterations)
- Password minimum length: 8 characters
- Never logged or exposed in error messages

### 2. JWT Security
- Signed with HS256 algorithm
- Expiration enforced
- Tampered tokens rejected
- Type claim distinguishes access vs refresh tokens

### 3. User Uniqueness
- Email addresses are unique globally
- Phone numbers are unique globally
- Validation occurs before user creation

### 4. Login Feedback
- Generic "Invalid credentials" message for both wrong password and unknown user
- Prevents user enumeration attacks
- Failed login attempts logged in AuditLog

### 5. Audit Logging
- `USER_REGISTERED`: New user registration
- `USER_LOGIN_SUCCESS`: Successful login (includes IP)
- `USER_LOGIN_FAILED`: Failed login attempt (includes IP, does not expose identifier)
- `PASSWORD_CHANGED`: Password change by user

### 6. Role-Based Access Control
- Dependencies for enforcing roles: `require_super_admin()`, `require_admin_or_super_admin()`, `require_student()`, `require_institution()`, etc.
- Automatic 403 Forbidden responses for insufficient permissions
- Roles checked at route level

## Configuration

### Environment Variables

```bash
# JWT Configuration
JWT_SECRET_KEY="your-secret-key-min-32-chars-in-production"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
REFRESH_TOKEN_EXPIRE_DAYS="7"
PASSWORD_MIN_LENGTH="8"

# Database
DATABASE_URL="postgresql+psycopg://user:password@host:5432/examflow"

# CORS
BACKEND_CORS_ORIGINS="http://localhost:3000,https://yourdomain.com"
```

## Testing

All auth components are tested with unit tests:

```bash
cd apps/api
source .venv/bin/activate
pytest app/tests/test_auth.py -v
```

### Test Coverage
- Password hashing and verification
- JWT token creation and decoding
- Schema validation (all registration/login schemas)
- RBAC dependency functions

## Production Checklist

- [ ] Set strong `JWT_SECRET_KEY` (32+ characters, random)
- [ ] Set `APP_ENV=production`
- [ ] Use HTTPS for all endpoints
- [ ] Implement token refresh endpoint if needed
- [ ] Set up database backups
- [ ] Monitor audit logs for suspicious activity
- [ ] Implement rate limiting on auth endpoints
- [ ] Use secure password reset flow (not yet implemented)
- [ ] Enable HTTPS-only cookies if using session-based auth
- [ ] Test all RBAC rules with production roles
