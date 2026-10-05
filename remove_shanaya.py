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

# Find Shanaya Singh
res = supabase.table('profiles').select('email, first_name').ilike('first_name', '%Shanaya%').execute()

if res.data:
    for p in res.data:
        email = p['email']
        # Delete
        del_res = supabase.table('profiles').delete().eq('email', email).execute()
        print(f"Deleted {p['first_name']} - {email}")
else:
    print("Could not find anyone with the name Shanaya")
