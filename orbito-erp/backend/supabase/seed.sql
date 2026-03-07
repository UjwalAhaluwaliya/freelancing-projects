-- Orbito ERP seed data (academic demo)
-- Login credentials:
-- admin@orbito.local / Admin@123
-- hr@orbito.local / Hr@12345
-- employee@orbito.local / Emp@12345

insert into public.profiles (id, email, full_name, role, department, password)
values
    (
        '11111111-1111-1111-1111-111111111111',
        'admin@orbito.local',
        'Orbito Admin',
        'admin',
        'Administration',
        '$2b$12$vmicA3pOM7UPP4Nt3R3qDe3mvPYSkt/Ncy.viq0e8BqyIDl39KFEq'
    ),
    (
        '22222222-2222-2222-2222-222222222222',
        'hr@orbito.local',
        'HR Manager',
        'hr',
        'Human Resources',
        '$2b$12$n3NTS31HjGC03PdROz/J4.b//9X0iDlekaQr3c3fNH111syWk5WgS'
    ),
    (
        '33333333-3333-3333-3333-333333333333',
        'employee@orbito.local',
        'Demo Employee',
        'employee',
        'Engineering',
        '$2b$12$HOWEr9LEOy07jOaAPverZ.hSA86.LTqBQkzZwSPVf2m6NPM1emUoy'
    )
on conflict (email) do nothing;

insert into public.candidates (id, full_name, email, phone, skills, total_experience, resume_url, overall_score, recommendation)
values
    (
        '44444444-4444-4444-4444-444444444444',
        'Aman Kumar',
        'aman.candidate@orbito.local',
        '9999999999',
        array['python', 'fastapi', 'postgresql'],
        3,
        'https://example.com/resume/aman',
        82,
        'Hire'
    ),
    (
        '55555555-5555-5555-5555-555555555555',
        'Priya Singh',
        'priya.candidate@orbito.local',
        '8888888888',
        array['react', 'typescript', 'ui-design'],
        2,
        'https://example.com/resume/priya',
        68,
        'Consider'
    )
on conflict (email) do nothing;

insert into public.job_descriptions (id, title, experience_level, location, employment_type, description, status)
values
    (
        '66666666-6666-6666-6666-666666666666',
        'Backend Developer',
        'Mid',
        'Remote',
        'Full-time',
        'Build and maintain FastAPI services with Supabase integrations.',
        'active'
    ),
    (
        '77777777-7777-7777-7777-777777777777',
        'Frontend Developer',
        'Junior',
        'Hybrid',
        'Full-time',
        'Develop React dashboards, ATS pages and AI interaction panels.',
        'active'
    )
on conflict (id) do nothing;

insert into public.applications (id, candidate_id, job_id, stage, stage_updated_at)
values
    (
        '88888888-8888-8888-8888-888888888888',
        '44444444-4444-4444-4444-444444444444',
        '66666666-6666-6666-6666-666666666666',
        'screening',
        now()
    ),
    (
        '99999999-9999-9999-9999-999999999999',
        '55555555-5555-5555-5555-555555555555',
        '77777777-7777-7777-7777-777777777777',
        'applied',
        now()
    )
on conflict (id) do nothing;

insert into public.interviews (id, application_id, interviewer_name, interview_date, status, feedback, score)
values
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        '88888888-8888-8888-8888-888888888888',
        'HR Manager',
        now() + interval '1 day',
        'scheduled',
        null,
        null
    )
on conflict (id) do nothing;

insert into public.leave_requests (id, employee_id, leave_type, start_date, end_date, days_requested, reason, status)
values
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        '33333333-3333-3333-3333-333333333333',
        'casual',
        current_date + 2,
        current_date + 3,
        2,
        'Personal work',
        'pending'
    )
on conflict (id) do nothing;

insert into public.notifications (id, user_id, title, message, is_read)
values
    (
        'cccccccc-cccc-cccc-cccc-cccccccccccc',
        '33333333-3333-3333-3333-333333333333',
        'Welcome to Orbito ERP',
        'Your employee account is ready for demo usage.',
        false
    ),
    (
        'dddddddd-dddd-dddd-dddd-dddddddddddd',
        '22222222-2222-2222-2222-222222222222',
        'Resume Shortlisted',
        'A candidate has crossed the shortlist threshold in demo data.',
        false
    )
on conflict (id) do nothing;

insert into public.achievements (id, user_id, points, reason)
values
    (
        'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
        '33333333-3333-3333-3333-333333333333',
        5,
        'Leave approved successfully'
    )
on conflict (id) do nothing;
