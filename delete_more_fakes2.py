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

fakes = [
    "samiisgoodgood@gmail.com",
    "sonam.s4994@gmail.com",
    "milindismokey@gmail.com",
    "mudgal971@gmail.com",
    "namanl1609@gmail.com",
    "laldharsan154@gmail.com",
    "namanlal1609@gmail.com",
    "oahshhshsha@gmail.com",
    "johnnnn815@gmail.com",
    "rubysinghrubysingh25@gmail.com"
]

for email in fakes:
    res = supabase.table('profiles').delete().eq('email', email).execute()
    print(f"Deleted: {email}")
