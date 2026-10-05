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

# Get Aabhas profile ID
res = supabase.table('profiles').select('id, email, first_name').ilike('email', '%aabhasgos2%').execute()
if not res.data:
    print("Could not find Aabhas")
else:
    aabhas_id = res.data[0]['id']
    print(f"Found Aabhas: {aabhas_id}")
    
    # Check matches
    matches = supabase.table('matches').select('*').or_(f"user1_id.eq.{aabhas_id},user2_id.eq.{aabhas_id}").execute()
    print(f"Matches found: {len(matches.data)}")
    for m in matches.data:
        print(m)
