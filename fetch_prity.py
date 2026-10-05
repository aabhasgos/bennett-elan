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

res = supabase.table('profiles').select('*').ilike('first_name', '%prity%').execute()

if not res.data:
    print("User not found by first name 'prity'. Let's search by instagram_handle '%sakshi%'")
    res = supabase.table('profiles').select('*').ilike('instagram_handle', '%sakshi%').execute()

for p in res.data:
    print(json.dumps(p, indent=2))
