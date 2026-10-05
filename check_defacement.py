import os
import json
from supabase import create_client

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='): supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='): supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

res = supabase.table('profiles').select('id, first_name, photo_urls').execute()
prompts = supabase.table('profile_prompts').select('*').execute()

defaced_users = []
for p in res.data:
    name = p.get('first_name')
    urls = p.get('photo_urls', [])
    if urls and any('hacked' in u.lower() or 'troll' in u.lower() or 'placeholder' in u.lower() for u in urls):
        defaced_users.append(name)
        
for pr in prompts.data:
    ans = pr.get('answer', '').lower()
    if 'hacked' in ans or 'defaced' in ans or 'fuck' in ans:
        print(f"Suspicious prompt: {ans}")

print(f"Users with suspicious photos: {defaced_users}")
