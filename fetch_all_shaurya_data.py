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

emails = [
    'shaurya08singh@gmail.com',
    'lucifer071008@gmail.com',
    'shaurya19feb@gmail.com',
    'shauryathakurr2008@gmail.com'
]

out = []

for email in emails:
    res = supabase.table('profiles').select('*').eq('email', email).execute()
    if not res.data:
        out.append(f"# User Profile: Not Found ({email})\n")
        continue
        
    profile = res.data[0]
    user_id = profile['id']
    name = profile.get('first_name') or 'No Name Set'
    
    out.append(f"# User Profile: {name}")
    out.append(f"**ID:** `{user_id}`")
    out.append(f"**Email:** `{email}`")
    out.append(f"**Account Created:** `{profile['created_at']}`\n")
    
    out.append("## Basic Info")
    out.append(f"- **Age:** {profile.get('age', 'Not set')}")
    out.append(f"- **Gender:** {profile.get('gender', 'Not set')}")
    out.append(f"- **Instagram:** {profile.get('instagram_handle', 'Not set')}")
    out.append(f"- **Verification:** {'Verified' if profile.get('is_verified') else 'Pending'}\n")
    
    prefs = supabase.table('preferences').select('*').eq('profile_id', user_id).execute()
    if prefs.data:
        p = prefs.data[0]
        out.append("## Preferences")
        look = p.get('looking_for_gender', [])
        out.append(f"- **Looking For:** {', '.join(look) if look else 'Not set'} (Ages {p.get('min_age', '?')}-{p.get('max_age', '?')})")
        intents = p.get('intentions', [])
        out.append(f"- **Intentions:** {', '.join(intents) if intents else 'Not set'}\n")
    else:
        out.append("## Preferences\nNot set up yet.\n")
        
    prompts = supabase.table('profile_prompts').select('*, prompts(question)').eq('profile_id', user_id).execute()
    if prompts.data:
        out.append("## Prompts & Answers")
        for p in prompts.data:
            out.append(f"**Q: {p['prompts']['question']}**")
            # clean answer of bad characters just in case
            ans = p['answer'].replace('\n', ' ')
            out.append(f"A: {ans}\n")
    else:
        out.append("## Prompts & Answers\nNone.\n")
        
    swipes_given = supabase.table('swipes').select('swipee_id, action').eq('swiper_id', user_id).execute()
    swipes_received = supabase.table('swipes').select('swiper_id, action').eq('swipee_id', user_id).execute()
    matches = supabase.table('matches').select('*').or_(f"user1_id.eq.{user_id},user2_id.eq.{user_id}").execute()
    
    out.append("## Activity Stats")
    out.append(f"- **Swipes Made:** {len(swipes_given.data)}")
    out.append(f"- **Right Swipes Received:** {len([s for s in swipes_received.data if s['action'] == 'right'])}")
    out.append(f"- **Total Matches:** {len(matches.data)}\n")
    
    out.append("## Uploaded Photos")
    urls = profile.get('photo_urls')
    if urls and len(urls) > 0:
        for i, url in enumerate(urls):
            out.append(f"- [Photo {i+1}]({url})")
    else:
        out.append("- No photos uploaded.")
        
    out.append("\n---\n")

with open('all_shauryas.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
