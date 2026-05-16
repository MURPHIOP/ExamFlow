# Deployment Guide

## Backend

Recommended targets: Render, Railway, or DigitalOcean.

### Render settings

- Root Directory: `apps/api`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Required environment variables

- `APP_ENV=production`
- `DATABASE_URL`
- `DIRECT_DATABASE_URL` if needed
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM=HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`
- `BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `RAZORPAY_WEBHOOK_SECRET`
- `STORAGE_PROVIDER=local`
- `EMAIL_PROVIDER` if configured

## Frontend

Recommended target: Vercel.

### Vercel settings

- Root Directory: `apps/web`
- Build Command: `npm run build`

### Required environment variables

- `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1`
- `NEXT_PUBLIC_APP_URL=https://your-frontend.vercel.app`
- `NEXT_PUBLIC_RAZORPAY_KEY_ID` if payment checkout needs it

## PostgreSQL

Use Supabase PostgreSQL or Neon PostgreSQL as the production database.

## Deployment Steps

1. Create the PostgreSQL database.
2. Add the database connection string to the backend environment.
3. Deploy the backend.
4. Run `alembic upgrade head` on the production database.
5. Seed only safe default rows if needed.
6. Deploy the frontend.
7. Set CORS to the frontend domain.
8. Configure Razorpay webhook URL.
9. Verify auth, application, payment, and document flows.
# Deployment Plan

## Targets
- Frontend: Vercel
- Backend: Render / Railway / DigitalOcean
- Database: Neon / Supabase / Railway PostgreSQL
- Storage: Cloudinary / S3-compatible provider

## Environment Strategy
- Separate environments: local, staging, production
- Distinct credentials and database instances per environment

## Required Deployment Variables
- App identity and environment variables
- Frontend public URLs
- API host/port and CORS origins
- Database URL
- Future auth/payment/storage/email/AI provider keys

## Delivery Approach
1. Deploy frontend and backend independently
2. Validate health endpoint and CORS
3. Attach managed PostgreSQL
4. Add storage provider configuration
5. Enable monitoring and alerting

## Current Step Scope
Deployment files are minimal placeholders for local/dev readiness. Full CI/CD and production hardening will be implemented in later prompts.
