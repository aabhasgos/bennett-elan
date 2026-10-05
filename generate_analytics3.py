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

users_auth = supabase.table('profiles').select('id, email, first_name, gender, age, is_verified').execute()
profiles = users_auth.data
total_signups = len(profiles)

onboarded = [p for p in profiles if p.get('first_name') and p.get('gender') and p.get('age')]
males = len([p for p in onboarded if p['gender'] == 'Male'])
females = len([p for p in onboarded if p['gender'] == 'Female'])
verified = len([p for p in onboarded if p.get('is_verified')])

all_swipes = []
page = 0
while True:
    res = supabase.table('swipes').select('*').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_swipes.extend(res.data)
    page += 1

total_swipes = len(all_swipes)
right_swipes = len([s for s in all_swipes if s['action'] == 'like'])
left_swipes = len([s for s in all_swipes if s['action'] == 'pass'])

right_swiped_counts = Counter([s['swipee_id'] for s in all_swipes if s['action'] == 'like'])
top_swiped = right_swiped_counts.most_common(10)

matches = supabase.table('matches').select('*').execute().data
total_matches = len(matches)

all_msgs = []
page = 0
while True:
    res = supabase.table('messages').select('*').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_msgs.extend(res.data)
    page += 1

total_messages = len(all_msgs)

chat_activity = {}
for m in all_msgs:
    mid = m['match_id']
    if mid not in chat_activity: chat_activity[mid] = set()
    chat_activity[mid].add(m['sender_id'])

chats_started = len(chat_activity)
two_way_chats = len([mid for mid, senders in chat_activity.items() if len(senders) >= 2])

id_to_name = {p['id']: p.get('first_name', 'Unknown') for p in profiles}
id_to_gender = {p['id']: p.get('gender', 'Unknown') for p in profiles}

top_popular_names = [(id_to_name.get(uid, "Unknown"), id_to_gender.get(uid, "Unknown"), count) for uid, count in top_swiped]

out = f"""# Bennett Elan - Executive Analytics Report

## ?? User Base Growth
- **Total Registered Accounts:** {total_signups}
- **Fully Onboarded Active Users:** {len(onboarded)}
  - ?? Males: {males}
  - ?? Females: {females}
  - ?? Other: {len(onboarded) - males - females}
- **Verified Profiles:** {verified}

## ?? Swiping Behavior
- **Total Network Swipes:** {total_swipes:,}
  - ?? Likes (Right Swipes): {right_swipes:,} ({(right_swipes/max(total_swipes,1)*100):.1f}%)
  - ? Passes (Left Swipes): {left_swipes:,} ({(left_swipes/max(total_swipes,1)*100):.1f}%)

## ?? Match & Chat Engagement
- **Total Matches Formed:** {total_matches}
- **Conversations Started:** {chats_started} ({(chats_started/max(total_matches, 1)*100):.1f}% of all matches)
- **Active Two-Way Chats:** {two_way_chats} ({(two_way_chats/max(chats_started, 1)*100):.1f}% of started chats)
- **Total Messages Exchanged:** {total_messages:,}

## ?? Top 10 Most Popular Users (Highest Likes)
"""

for i, (name, gender, count) in enumerate(top_popular_names):
    out += f"{i+1}. **{name}** ({gender}) - {count} Likes\n"

with open('C:/Users/aabha/.gemini/antigravity/brain/5a64ec79-12f5-4965-85a8-ed82fe9e1b22/executive_analytics.md', 'w', encoding='utf-8') as f:
    f.write(out)
