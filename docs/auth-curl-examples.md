# ExamFlow Authentication - cURL Examples

These examples demonstrate how to test the authentication and authorization APIs using `curl`.

## Prerequisites

```bash
# Backend running on localhost:8000
export API_URL="http://localhost:8000/api/v1"

# Or production
export API_URL="https://api.yourdomain.com/api/v1"
```

## Student Registration

### Register a new student

```bash
curl -X POST "$API_URL/auth/register/student" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Shreyan Mitra",
    "email": "shreyan@example.com",
    "phone": "9876543210",
    "password": "Student@12345",
    "confirm_password": "Student@12345",
    "date_of_birth": "2000-01-15",
    "gender": "Male",
    "guardian_name": "Guardian Name",
    "guardian_phone": "9876543211",
    "district": "Kolkata",
    "state": "West Bengal",
    "address": "123 Main Street",
    "pincode": "700001"
  }'
```

### Response (201 Created)

```json
{
  "success": true,
  "message": "Student registered successfully",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "shreyan@example.com",
    "phone": "9876543210"
  }
}
```

---

## Institution Registration

### Register a new institution

```bash
curl -X POST "$API_URL/auth/register/institution" \
  -H "Content-Type: application/json" \
  -d '{
    "institution_name": "Kolkata Music Academy",
    "contact_person_name": "Admin Person",
    "email": "academy@example.com",
    "phone": "9876543211",
    "password": "Academy@12345",
    "confirm_password": "Academy@12345",
    "registration_number": "REG-KMA-001",
    "district": "Kolkata",
    "state": "West Bengal",
    "address": "456 Academy Road",
    "pincode": "700001"
  }'
```

### Response (201 Created)

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

---

## Login

### Login with email

```bash
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "shreyan@example.com",
    "password": "Student@12345"
  }'
```

### Login with phone

```bash
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "9876543210",
    "password": "Student@12345"
  }'
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJyb2xlIjoic3R1ZGVudCIsImV4cCI6MTcxNTE2NzY3MCwiaWF0IjoxNzE1MTY1ODcwLCJ0eXBlIjoiYWNjZXNzIn0.signature...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJyb2xlIjoic3R1ZGVudCIsImV4cCI6MTcxNTc3MDY3MCwiaWF0IjoxNzE1MTY1ODcwLCJ0eXBlIjoicmVmcmVzaCJ9.signature...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "full_name": "Shreyan Mitra",
      "email": "shreyan@example.com",
      "phone": "9876543210",
      "role": "student",
      "is_active": true,
      "is_verified": false
    }
  }
}
```

### Store tokens for later requests

```bash
# After login, store the token
export ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
export REFRESH_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Get Current User

### Get authenticated user details

```bash
curl -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Current user retrieved",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "Shreyan Mitra",
    "email": "shreyan@example.com",
    "phone": "9876543210",
    "role": "student",
    "is_active": true,
    "is_verified": false
  }
}
```

---

## Logout

### Logout (client-side token deletion for MVP)

```bash
curl -X POST "$API_URL/auth/logout" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Response (200 OK)

```json
{
  "success": true,
  "message": "Logout successful. Please delete the token from client storage."
}
```

**Note:** For JWT MVP, the server doesn't maintain a token blacklist. The client must delete the token from its local storage.

---

## Protected Routes (RBAC Testing)

### Get current user (protected endpoint)

```bash
curl -X GET "$API_URL/protected/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Response (200 OK)

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

### Admin-only endpoint (should fail for student)

```bash
curl -X GET "$API_URL/protected/admin-only" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Response (403 Forbidden - if user is student)

```json
{
  "detail": "Insufficient permissions"
}
```

---

### Admin-only endpoint (should work for admin)

```bash
# First login as admin
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "admin@mbtechnosoft.com",
    "password": "Admin@12345"
  }'

# Extract admin access token
export ADMIN_TOKEN="<admin_access_token>"

# Try admin-only endpoint
curl -X GET "$API_URL/protected/admin-only" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Response (200 OK - if user is admin or super admin)

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

---

### Super Admin-only endpoint

```bash
# First login as super admin
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "superadmin@mbtechnosoft.com",
    "password": "Admin@12345"
  }'

# Extract super admin access token
export SUPER_ADMIN_TOKEN="<super_admin_access_token>"

# Try super admin-only endpoint
curl -X GET "$API_URL/protected/super-admin-only" \
  -H "Authorization: Bearer $SUPER_ADMIN_TOKEN"
```

### Response (200 OK - if user is super admin)

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

## Error Scenarios

### Missing token

```bash
curl -X GET "$API_URL/auth/me"
```

### Response (403 Forbidden)

```json
{
  "detail": "Not authenticated"
}
```

---

### Invalid token

```bash
curl -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer invalid_token"
```

### Response (401 Unauthorized)

```json
{
  "detail": "Invalid authentication credentials"
}
```

---

### Wrong password

```bash
curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "shreyan@example.com",
    "password": "WrongPassword@123"
  }'
```

### Response (401 Unauthorized)

```json
{
  "success": false,
  "detail": "Invalid credentials"
}
```

---

### Duplicate email

```bash
# First registration
curl -X POST "$API_URL/auth/register/student" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Student One",
    "email": "duplicate@example.com",
    "password": "Student@12345",
    "confirm_password": "Student@12345"
  }'

# Second registration with same email
curl -X POST "$API_URL/auth/register/student" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Student Two",
    "email": "duplicate@example.com",
    "password": "Student@12345",
    "confirm_password": "Student@12345"
  }'
```

### Response (409 Conflict)

```json
{
  "detail": "Email already registered"
}
```

---

## Testing Workflow

### Complete flow for testing

```bash
# 1. Register student
REGISTER=$(curl -s -X POST "$API_URL/auth/register/student" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Student",
    "email": "test@example.com",
    "password": "Test@12345",
    "confirm_password": "Test@12345"
  }')

echo "Registration Response:"
echo $REGISTER | jq .

# 2. Login
LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "test@example.com",
    "password": "Test@12345"
  }')

echo "Login Response:"
echo $LOGIN | jq .

# 3. Extract token
TOKEN=$(echo $LOGIN | jq -r '.data.access_token')

# 4. Get current user
curl -s -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 5. Try protected route
curl -s -X GET "$API_URL/protected/me" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 6. Try admin route (should fail for student)
curl -s -X GET "$API_URL/protected/admin-only" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 7. Logout
curl -s -X POST "$API_URL/auth/logout" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

---

## Debugging Tips

### Pretty print JSON

```bash
curl -s <url> | jq .
```

### See all response headers

```bash
curl -i -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### See request and response

```bash
curl -v -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier":"user@example.com","password":"Pass@123"}'
```

### Check token expiration

```bash
# Decode JWT (requires `jq` and base64 decoding)
echo $ACCESS_TOKEN | cut -d'.' -f2 | base64 -D | jq .
```

Expected output:
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "role": "student",
  "exp": 1715167670,
  "iat": 1715165870,
  "type": "access"
}
```
