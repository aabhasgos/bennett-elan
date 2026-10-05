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
res = supabase.table('profiles').select('photo_urls').execute()

has_photo = 0
for p in res.data:
    urls = p.get('photo_urls')
    if urls and isinstance(urls, list) and len(urls) > 0:
        has_photo += 1

print(f'Total signups: {len(res.data)}')
print(f'Users with at least one photo: {has_photo}')
