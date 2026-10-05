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
res = supabase.table('profiles').select('email, first_name').execute()

suspicious = []
for p in res.data:
    name = p.get('first_name')
    if name:
        name = name.lower().strip()
        if len(name) <= 1 or name in ['test', 'fake', 'xyz', 'bkl', 'moii', 'someone ph', 'test 2', 'n/a']:
            suspicious.append(p)

for s in suspicious:
    print(f"Suspicious: {s.get('first_name')} - {s.get('email')}")
