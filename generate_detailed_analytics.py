import os
import json
from supabase import create_client
from collections import Counter

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='): supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='): supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

# 1. Fetch Users
users_auth = supabase.table('profiles').select('id, email, first_name, gender, age').execute()
profiles = users_auth.data
onboarded = [p for p in profiles if p.get('first_name') and p.get('gender') and p.get('age')]
id_to_name = {p['id']: f"{p.get('first_name', 'Unknown')} ({p.get('gender', 'Unknown')})" for p in onboarded}

# 2. Fetch Swipes
all_swipes = []
page = 0
while True:
    res = supabase.table('swipes').select('swiper_id, swipee_id, action').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_swipes.extend(res.data)
    page += 1

right_swipes = Counter([s['swipee_id'] for s in all_swipes if s['action'] == 'like'])

# 3. Fetch Matches
matches = supabase.table('matches').select('*').execute().data

# 4. Fetch Messages
all_msgs = []
page = 0
while True:
    res = supabase.table('messages').select('*').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_msgs.extend(res.data)
    page += 1

msg_counts_per_match = {}
for m in all_msgs:
    mid = m['match_id']
    msg_counts_per_match[mid] = msg_counts_per_match.get(mid, 0) + 1

# Generate Markdown
out = []
out.append("# Bennett Elan - The Master Database Report")
out.append("This is a complete, unredacted dump of all ecosystem activity.\n")

out.append("## ?? Full Leaderboard (Likes Received)")
sorted_likes = right_swipes.most_common()
for i, (uid, count) in enumerate(sorted_likes):
    name = id_to_name.get(uid, "Deleted/Unknown User")
    out.append(f"{i+1}. **{name}** - {count} likes")

out.append("\n## ?? All Matches & Chat History")
for m in matches:
    u1 = id_to_name.get(m['user1_id'], "Deleted User")
    u2 = id_to_name.get(m['user2_id'], "Deleted User")
    msgs = msg_counts_per_match.get(m['id'], 0)
    out.append(f"- {u1} ?? {u2} (Messages: {msgs})")

out.append("\n## ?? Directory of All Onboarded Users")
for p in onboarded:
    out.append(f"- **{p['first_name']}** ({p['gender']}, {p['age']}) - {p['email']}")

with open('master_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
