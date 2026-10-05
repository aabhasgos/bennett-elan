import os
from supabase import create_client

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='): supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='): supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

# Get Pratham's ID
res_p = supabase.table('profiles').select('id, first_name').ilike('first_name', '%pratham%').execute()
if not res_p.data:
    print("Pratham not found in database.")
    exit()

pratham_ids = [p['id'] for p in res_p.data]

# Get all matches where Pratham is user1 or user2
matches = supabase.table('matches').select('*').execute().data

pratham_matches = []
for m in matches:
    if m['user1_id'] in pratham_ids or m['user2_id'] in pratham_ids:
        # Get the other user's ID
        other_id = m['user2_id'] if m['user1_id'] in pratham_ids else m['user1_id']
        other_res = supabase.table('profiles').select('first_name').eq('id', other_id).execute()
        other_name = other_res.data[0]['first_name'] if other_res.data else "Unknown"
        pratham_matches.append(other_name)

if pratham_matches:
    print("Pratham's matches:")
    for match in pratham_matches:
        print(f"- {match}")
else:
    print("Pratham has 0 matches.")
