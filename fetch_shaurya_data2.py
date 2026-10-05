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

res = supabase.table('profiles').select('*').eq('email', email).execute()
profile = res.data[0]
user_id = profile['id']

prefs = supabase.table('preferences').select('*').eq('profile_id', user_id).execute()
prompts = supabase.table('profile_prompts').select('*, prompts(question)').eq('profile_id', user_id).execute()
swipes_given = supabase.table('swipes').select('swipee_id, action').eq('swiper_id', user_id).execute()
swipes_received = supabase.table('swipes').select('swiper_id, action').eq('swipee_id', user_id).execute()
matches = supabase.table('matches').select('*').or_(f"user1_id.eq.{user_id},user2_id.eq.{user_id}").execute()

out = []
out.append("=== PROFILE ===")
out.append(json.dumps(profile, indent=2))
out.append("\n=== PREFERENCES ===")
out.append(json.dumps(prefs.data[0] if prefs.data else {}, indent=2))
out.append("\n=== PROMPTS ===")
for p in prompts.data:
    out.append(f"Q: {p['prompts']['question']}\nA: {p['answer']}")
out.append(f"\n=== SWIPES ===")
out.append(f"Swipes made by him: {len(swipes_given.data)}")
out.append(f"Right swipes received: {len([s for s in swipes_received.data if s['action'] == 'right'])}")
out.append(f"\n=== MATCHES ===")
out.append(f"Total Matches: {len(matches.data)}")

with open('shaurya_data.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
