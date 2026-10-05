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

# 1. User Base
users_auth = supabase.table('profiles').select('id, email, first_name, gender, age, is_verified').execute()
profiles = users_auth.data
total_signups = len(profiles)

onboarded = [p for p in profiles if p.get('first_name') and p.get('gender') and p.get('age')]
males = len([p for p in onboarded if p['gender'] == 'Male'])
females = len([p for p in onboarded if p['gender'] == 'Female'])
verified = len([p for p in onboarded if p.get('is_verified')])

# 2. Swipes (Pagination)
all_swipes = []
page = 0
while True:
    res = supabase.table('swipes').select('*').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_swipes.extend(res.data)
    page += 1

total_swipes = len(all_swipes)
right_swipes = len([s for s in all_swipes if s['action'] == 'right'])
left_swipes = len([s for s in all_swipes if s['action'] == 'left'])
super_likes = len([s for s in all_swipes if s['action'] not in ['right', 'left']])

right_swiped_counts = Counter([s['swipee_id'] for s in all_swipes if s['action'] == 'right'])
top_swiped = right_swiped_counts.most_common(10)

# 3. Matches
matches = supabase.table('matches').select('*').execute().data
total_matches = len(matches)

# 4. Messages
all_msgs = []
page = 0
while True:
    res = supabase.table('messages').select('*').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_msgs.extend(res.data)
    page += 1

total_messages = len(all_msgs)

chat_activity = {}
msg_counts_per_match = {}
for m in all_msgs:
    mid = m['match_id']
    if mid not in chat_activity: chat_activity[mid] = set()
    chat_activity[mid].add(m['sender_id'])
    msg_counts_per_match[mid] = msg_counts_per_match.get(mid, 0) + 1

chats_started = len(chat_activity)
two_way_chats = len([mid for mid, senders in chat_activity.items() if len(senders) >= 2])

id_to_name = {p['id']: p.get('first_name', 'Unknown') for p in profiles}
id_to_gender = {p['id']: p.get('gender', 'Unknown') for p in profiles}

top_popular_names = [(id_to_name.get(uid, "Unknown"), id_to_gender.get(uid, "Unknown"), count) for uid, count in top_swiped]

out = f"""# Bennett A%lan - Comprehensive Analytics Report

## ?? User Base
- **Total Signups:** {total_signups}
- **Fully Onboarded:** {len(onboarded)}
  - ?? Males: {males}
  - ?? Females: {females}
  - ?? Other: {len(onboarded) - males - females}
- **Verified Profiles:** {verified}

## ?? Swipe Activity
- **Total Swipes:** {total_swipes}
  - ?? Right Swipes (Likes): {right_swipes} ({(right_swipes/max(total_swipes,1)*100):.1f}%)
  - ? Left Swipes (Passes): {left_swipes} ({(left_swipes/max(total_swipes,1)*100):.1f}%)

## ?? Matches & Chat Engagement
- **Total Matches Formed:** {total_matches}
- **Chats Initiated:** {chats_started} ({(chats_started/max(total_matches, 1)*100):.1f}% of matches)
- **Two-Way Conversations:** {two_way_chats} ({(two_way_chats/max(chats_started, 1)*100):.1f}% of chats started)
- **Total Messages Sent:** {total_messages}

## ?? Top 10 Most Popular Users (Most Likes Received)
"""

for i, (name, gender, count) in enumerate(top_popular_names):
    out += f"{i+1}. **{name}** ({gender}) - {count} likes\n"

with open('analytics_dump2.md', 'w', encoding='utf-8') as f:
    f.write(out)
