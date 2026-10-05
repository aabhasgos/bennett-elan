import os
from supabase import create_client

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='): supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='): supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

prompts = supabase.table('profile_prompts').select('*').limit(20).execute()
for p in prompts.data:
    print(p['answer'])
