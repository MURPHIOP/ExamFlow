# Supabase PostgreSQL Setup

Supabase is supported as the preferred hosted PostgreSQL option for ExamFlow. Use it as the production database for the FastAPI backend. The frontend must never connect directly to the database.

## Setup Steps

1. Create a Supabase project.
2. Open **Project Settings → Database**.
3. Copy the PostgreSQL connection string.
4. Replace the password with your actual database password.
5. Set the backend environment variable:

```bash
DATABASE_URL="postgresql+psycopg://postgres.xxx:password@aws-xxx.pooler.supabase.com:6543/postgres"
```

6. If the pooler requires a direct connection for migrations, add:

```bash
DIRECT_DATABASE_URL="postgresql+psycopg://postgres.xxx:password@db.xxx.supabase.co:5432/postgres"
```

7. Do not expose the Supabase service role key in the frontend.
8. Run migrations from the backend:

```bash
cd apps/api
alembic upgrade head
```

9. Run the safe seed script if needed:

```bash
python -m app.db.seed
```

10. Start the backend and verify health:

```bash
uvicorn app.main:app --reload
curl http://localhost:8000/health
```

## Notes

- Use Supabase pooler for runtime connections if required.
- Use the direct connection string for migration tasks if the pooler blocks DDL.
- SQLAlchemy/Alembic remains the source of truth for schema changes.
- Prisma is only a frontend mirror and tooling helper.
