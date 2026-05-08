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

## Planned Route Groups (Future)
- `/api/v1/auth`
- `/api/v1/users`
- `/api/v1/exam-sessions`
- `/api/v1/applications`
- `/api/v1/payments`
- `/api/v1/admit-cards`
- `/api/v1/results`
- `/api/v1/certificates`
- `/api/v1/reports`
- `/api/v1/ai`
