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

# 1. Matches
matches_res = supabase.table('matches').select('user1_id, user2_id').execute()
matched_users = set()
for m in matches_res.data:
    matched_users.add(m['user1_id'])
    matched_users.add(m['user2_id'])

# 2. Chatters
messages_res = supabase.table('messages').select('sender_id').execute()
chatting_users = set()
for msg in messages_res.data:
    chatting_users.add(msg['sender_id'])

print(f"Total Matches Formed: {len(matches_res.data)}")
print(f"Users with at least one match: {len(matched_users)}")
print(f"Total Messages Sent: {len(messages_res.data)}")
print(f"Users who have sent at least one message: {len(chatting_users)}")
