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
res = supabase.table('profiles').select('id, first_name, gender, age, photo_urls').execute()

total_signups = len(res.data)
onboarded_males = 0
onboarded_females = 0
onboarded_other = 0

for p in res.data:
    if p.get('first_name') and p.get('gender') and p.get('age') and p.get('photo_urls'):
        urls = p.get('photo_urls')
        if isinstance(urls, list) and len(urls) > 0:
            gender = p.get('gender').lower()
            if gender == 'male':
                onboarded_males += 1
            elif gender == 'female':
                onboarded_females += 1
            else:
                onboarded_other += 1

total_onboarded = onboarded_males + onboarded_females + onboarded_other

print(f"Total people who hit the login page (Signups): {total_signups}")
print(f"Total fully onboarded users: {total_onboarded}")
print(f" - Males: {onboarded_males}")
print(f" - Females: {onboarded_females}")
print(f" - Other/Not specified: {onboarded_other}")
