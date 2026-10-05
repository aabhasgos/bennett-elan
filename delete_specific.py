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

names_to_delete = ["Anonymous", "Anusha", "Nananan"]

for name in names_to_delete:
    res = supabase.table('profiles').select('email, first_name').ilike('first_name', name).execute()
    if res.data:
        for p in res.data:
            email = p['email']
            supabase.table('profiles').delete().eq('email', email).execute()
            print(f"Deleted: {p['first_name']} ({email})")
    else:
        print(f"Could not find exact match for {name}")
