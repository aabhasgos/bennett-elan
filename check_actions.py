import os
from supabase import create_client
from collections import Counter

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='):
            supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='):
            supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

page = 0
all_actions = []
while True:
    res = supabase.table('swipes').select('action').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_actions.extend([r['action'] for r in res.data])
    page += 1
    
c = Counter(all_actions)
print(c)
