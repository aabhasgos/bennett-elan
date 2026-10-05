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

aabhas_id = 'f5f3125e-75bb-4ff9-85a5-48d3f008cadf'

# Check who swiped on Aabhas
likes = supabase.table('swipes').select('*').eq('swipee_id', aabhas_id).eq('action', 'right').execute()
print(f"People who swiped right on Aabhas: {len(likes.data)}")
for l in likes.data:
    # Get their name
    p = supabase.table('profiles').select('first_name, email').eq('id', l['swiper_id']).execute()
    if p.data:
        print(f" - {p.data[0]['first_name']} ({p.data[0]['email']})")
    else:
        print(f" - Profile deleted for ID: {l['swiper_id']}")

# Check who Aabhas swiped on
swipes = supabase.table('swipes').select('*').eq('swiper_id', aabhas_id).eq('action', 'right').execute()
print(f"People Aabhas swiped right on: {len(swipes.data)}")
for s in swipes.data:
    p = supabase.table('profiles').select('first_name, email').eq('id', s['swipee_id']).execute()
    if p.data:
        print(f" - {p.data[0]['first_name']} ({p.data[0]['email']})")
    else:
        print(f" - Profile deleted for ID: {s['swipee_id']}")

