import os
from supabase import create_client

supabase_url = None
supabase_key = None

with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='):
            supabase_url = line.split('=', 1)[1].strip()
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='):
            supabase_key = line.split('=', 1)[1].strip()

supabase = create_client(supabase_url, supabase_key)
res = supabase.table('profiles').select('first_name, gender, age, course, year, email, photo_urls').execute()

onboarded = []
for p in res.data:
    if p.get('first_name') and p.get('gender') and p.get('age') and p.get('photo_urls'):
        if len(p.get('photo_urls')) > 0:
            onboarded.append(p)

print(f'Total signed up: {len(res.data)}')
print(f'Fully onboarded: {len(onboarded)}\n')
for u in onboarded:
    print(f"- {u.get('first_name')} ({u.get('gender')}, {u.get('age')}) - {u.get('course')} {u.get('year')} - {u.get('email')}")