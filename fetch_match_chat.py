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

# Get all profiles for mapping
res_p = supabase.table('profiles').select('id, first_name').execute()
profiles = {p['id']: p.get('first_name', 'Unknown') for p in res_p.data}

# Get matches
res_m = supabase.table('matches').select('*').execute()
matches = res_m.data

# Get messages to see who chatted
res_msg = supabase.table('messages').select('*').execute()
messages = res_msg.data

# Find which matches had chats
chat_counts = {} # match_id -> number of messages
for msg in messages:
    mid = msg['match_id']
    chat_counts[mid] = chat_counts.get(mid, 0) + 1

output = []
for m in matches:
    name1 = profiles.get(m['user1_id'], 'Deleted User')
    name2 = profiles.get(m['user2_id'], 'Deleted User')
    mid = m['id']
    
    msgs = chat_counts.get(mid, 0)
    if msgs > 0:
        output.append(f"?? {name1} matched with {name2} (??? {msgs} messages sent)")
    else:
        output.append(f"?? {name1} matched with {name2} (No messages yet)")

# Write output to file so it doesn't clutter terminal if it's long
with open('matches_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"Total Matches: {len(matches)}")
print(f"Total Chats: {len([c for c in chat_counts.values() if c > 0])}")
