-- Orbito ERP - Initial schema
-- Safe for repeated execution in academic setups.

create extension if not exists "pgcrypto";

create table if not exists public.profiles (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    full_name text not null,
    role text not null check (role in ('admin', 'hr', 'employee')),
    department text,
    password text,
    created_at timestamptz not null default now()
);

create table if not exists public.leave_requests (
    id uuid primary key default gen_random_uuid(),
    employee_id uuid not null references public.profiles(id) on delete cascade,
    leave_type text not null,
    start_date date not null,
    end_date date not null,
    days_requested integer not null,
    reason text not null,
    status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
    created_at timestamptz not null default now()
);

create table if not exists public.notifications (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles(id) on delete cascade,
    title text not null,
    message text not null,
    is_read boolean not null default false,
    created_at timestamptz not null default now()
);

create table if not exists public.candidates (
    id uuid primary key default gen_random_uuid(),
    full_name text not null,
    email text not null unique,
    phone text,
    skills text[] not null default '{}',
    total_experience integer,
    resume_url text,
    overall_score numeric(5,2),
    recommendation text,
    created_at timestamptz not null default now()
);

create table if not exists public.job_descriptions (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    department_id uuid,
    experience_level text,
    location text,
    employment_type text,
    description text not null,
    status text not null default 'active',
    created_at timestamptz not null default now()
);

create table if not exists public.applications (
    id uuid primary key default gen_random_uuid(),
    candidate_id uuid not null references public.candidates(id) on delete cascade,
    job_id uuid not null references public.job_descriptions(id) on delete cascade,
    stage text not null default 'applied' check (stage in ('applied', 'screening', 'interview', 'offer', 'hired', 'rejected')),
    stage_updated_at timestamptz,
    created_at timestamptz not null default now()
);

create table if not exists public.interviews (
    id uuid primary key default gen_random_uuid(),
    application_id uuid not null references public.applications(id) on delete cascade,
    interviewer_name text not null,
    interview_date timestamptz not null,
    status text not null default 'scheduled' check (status in ('scheduled', 'completed', 'cancelled')),
    feedback text,
    score numeric(5,2),
    created_at timestamptz not null default now()
);

create table if not exists public.achievements (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles(id) on delete cascade,
    points integer not null default 0,
    reason text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_profiles_role on public.profiles(role);
create index if not exists idx_leave_requests_employee_id on public.leave_requests(employee_id);
create index if not exists idx_notifications_user_id on public.notifications(user_id);
create index if not exists idx_candidates_email on public.candidates(email);
create index if not exists idx_job_descriptions_status on public.job_descriptions(status);
create index if not exists idx_applications_candidate_id on public.applications(candidate_id);
create index if not exists idx_applications_job_id on public.applications(job_id);
create index if not exists idx_applications_stage on public.applications(stage);
create index if not exists idx_interviews_application_id on public.interviews(application_id);
create index if not exists idx_achievements_user_id on public.achievements(user_id);
