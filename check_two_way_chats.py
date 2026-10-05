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

# Get all profiles
res_p = supabase.table('profiles').select('id, first_name').execute()
profiles = {p['id']: p.get('first_name', 'Unknown') for p in res_p.data}

# Get matches
res_m = supabase.table('matches').select('*').execute()
matches = {m['id']: m for m in res_m.data}

# Get messages
res_msg = supabase.table('messages').select('*').execute()
messages = res_msg.data

# Group messages by match_id and sender_id
chat_activity = {} # match_id -> set of sender_ids
message_counts = {} # match_id -> total messages

for msg in messages:
    mid = msg['match_id']
    sid = msg['sender_id']
    
    if mid not in chat_activity:
        chat_activity[mid] = set()
    chat_activity[mid].add(sid)
    
    message_counts[mid] = message_counts.get(mid, 0) + 1

two_way_chats = []

for mid, senders in chat_activity.items():
    if len(senders) >= 2: # Both users replied
        match = matches.get(mid)
        if match:
            u1 = profiles.get(match['user1_id'], 'Deleted User')
            u2 = profiles.get(match['user2_id'], 'Deleted User')
            total = message_counts[mid]
            two_way_chats.append((u1, u2, total))

# Sort by total messages
two_way_chats.sort(key=lambda x: x[2], reverse=True)

out = [f"Total Two-Way Conversations: {len(two_way_chats)}\n"]
for chat in two_way_chats:
    out.append(f"?? {chat[0]} & {chat[1]} (??? {chat[2]} messages exchanged)")

with open('two_way.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print(f"Two-way chats: {len(two_way_chats)}")
