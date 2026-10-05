import os
import json
from supabase import create_client
from datetime import datetime, timezone

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='): supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='): supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

res = supabase.table('profiles').select('id, email, first_name, updated_at, photo_urls').execute()
profiles = res.data

for p in profiles:
    # If updated_at is within the last 3 hours (since the report)
    # The report was at ~18:15 UTC. Current time is ~20:30 UTC.
    print(f"{p['first_name']} | {p['email']} | {p['updated_at']}")
