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

fake_emails = [
    "thereyougoman78789878@gmail.com",
    "goswami.0aabhas@gmail.com",
    "harshita70046@gmail.com",
    "nayshamohan20@gmail.com"
]

deleted_count = 0
for email in fake_emails:
    # We can delete from profiles where email = X
    # Using ANON_KEY we might not have RLS permission to delete other users unless RLS is disabled.
    # Earlier we disabled RLS on profiles!
    res = supabase.table('profiles').delete().eq('email', email).execute()
    if res.data:
        deleted_count += len(res.data)
        print(f"Deleted profile for: {email}")

print(f"Total fake profiles removed: {deleted_count}")
