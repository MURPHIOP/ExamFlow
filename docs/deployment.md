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
