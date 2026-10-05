import os
import json
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

names = ['Souptika', 'akshitajain']
for name in names:
    res = supabase.table('profiles').select('email, first_name, photo_urls').ilike('first_name', f'%{name}%').execute()
    for p in res.data:
        print(f"Name: {p['first_name']}, Email: {p['email']}, Photos: {p['photo_urls']}")
