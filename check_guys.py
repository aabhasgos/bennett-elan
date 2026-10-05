import os
from supabase import create_client

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='):
            supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='):
            supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

names = ['Aditya', 'Adarsh', 'Yash', 'Kshitij Tanwar', 'Tanishk', 'Arnav']
for n in names:
    res = supabase.table('profiles').select('email, first_name').ilike('first_name', f'%{n}%').execute()
    print(f'{n}: found {len(res.data)}')
