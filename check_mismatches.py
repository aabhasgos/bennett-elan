import os
import re
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
res = supabase.table('profiles').select('first_name, email, gender, age, photo_urls').execute()

flagged = []

for p in res.data:
    if not p.get('first_name') or not p.get('email'): continue
    
    first_name = p['first_name'].strip().lower()
    email = p['email'].strip().lower()
    username = email.split('@')[0]
    
    # 1. Skip if university email (since it's an ID number)
    if 'bennett.edu.in' in email:
        continue
        
    # 2. Check if name is extremely short
    if len(first_name) <= 2:
        flagged.append(p)
        continue
        
    # 3. Check for mismatch
    # Split first name in case they wrote "John Doe"
    name_parts = first_name.split()
    matched = False
    
    for part in name_parts:
        if len(part) > 2 and part in username:
            matched = True
            break
            
    # Some common nicknames or Indian names might not exactly match the email if they use a family email
    if not matched:
        # Check if the username is just a completely different name
        flagged.append(p)

print(f"Total checked: {len(res.data)}")
for f in flagged:
    print(f"- {f['first_name']} ({f['gender']}, {f['age']}) | Email: {f['email']}")

