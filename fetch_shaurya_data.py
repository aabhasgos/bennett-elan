import os
import json
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

email = 'lucifer071008@gmail.com'

# 1. Profile
res = supabase.table('profiles').select('*').eq('email', email).execute()
if not res.data:
    print("User not found.")
    exit()
    
profile = res.data[0]
user_id = profile['id']

print("=== PROFILE ===")
print(json.dumps(profile, indent=2))

# 2. Preferences
prefs = supabase.table('preferences').select('*').eq('profile_id', user_id).execute()
print("\n=== PREFERENCES ===")
print(json.dumps(prefs.data[0] if prefs.data else {}, indent=2))

# 3. Prompts
prompts = supabase.table('profile_prompts').select('*, prompts(question)').eq('profile_id', user_id).execute()
print("\n=== PROMPTS ===")
for p in prompts.data:
    print(f"Q: {p['prompts']['question']}")
    print(f"A: {p['answer']}")

# 4. Swipes
# Who he swiped right on
swipes_given = supabase.table('swipes').select('swipee_id, action').eq('swiper_id', user_id).execute()
# Who swiped right on him
swipes_received = supabase.table('swipes').select('swiper_id, action').eq('swipee_id', user_id).execute()

print(f"\n=== SWIPES ===")
print(f"Total swipes made: {len(swipes_given.data)}")
print(f"Total right swipes received: {len([s for s in swipes_received.data if s['action'] == 'right'])}")

# 5. Matches
matches = supabase.table('matches').select('*').or_(f"user1_id.eq.{user_id},user2_id.eq.{user_id}").execute()
print(f"\n=== MATCHES ===")
print(f"Total Matches: {len(matches.data)}")

