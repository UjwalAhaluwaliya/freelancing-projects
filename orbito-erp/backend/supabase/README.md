# Supabase Setup (Academic)

## Apply migration

Run SQL from:

- `supabase/migrations/20260303_001_init_schema.sql`

## Load demo seed

Run SQL from:

- `supabase/seed.sql`

## Notes

- The seed provides demo users, candidates, jobs, applications, interviews, notifications and achievements.
- If you rerun seed, `ON CONFLICT` avoids duplicate records.
- For class demo, this is enough to show full end-to-end flows quickly.
