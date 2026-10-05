import re

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update swipe endpoint to return match_id
old_swipe = '''        if mutual.data:
            # Create match
            try:
                supabase.table('matches').insert({
                    "user1_id": min(user_id, swipe.swipee_id),
                    "user2_id": max(user_id, swipe.swipee_id)
                }).execute()
            except Exception:
                pass
            return {"status": "match"}'''

new_swipe = '''        if mutual.data:
            # Create match
            match_id = None
            try:
                match_res = supabase.table('matches').insert({
                    "user1_id": min(user_id, swipe.swipee_id),
                    "user2_id": max(user_id, swipe.swipee_id)
                }).execute()
                match_id = match_res.data[0]['id']
            except Exception:
                existing = supabase.table('matches').select('id').eq('user1_id', min(user_id, swipe.swipee_id)).eq('user2_id', max(user_id, swipe.swipee_id)).execute()
                if existing.data:
                    match_id = existing.data[0]['id']
            return {"status": "match", "match_id": match_id}'''

content = content.replace(old_swipe, new_swipe)

# Add /likes endpoint
likes_endpoint = '''
@app.get("/likes")
async def get_incoming_likes(user_id: str = Depends(get_user_id)):
    # 1. Get who liked me
    liked_me_res = supabase.table('swipes').select('swiper_id').eq('swipee_id', user_id).eq('action', 'like').execute()
    liked_me_ids = [row['swiper_id'] for row in liked_me_res.data]
    
    if not liked_me_ids:
        return []
        
    # 2. Get who I have already swiped on
    my_swipes_res = supabase.table('swipes').select('swipee_id').eq('swiper_id', user_id).execute()
    my_swiped_ids = [row['swipee_id'] for row in my_swipes_res.data]
    
    # 3. Filter out those I've already reacted to
    pending_ids = [uid for uid in liked_me_ids if uid not in my_swiped_ids]
    
    if not pending_ids:
        return []
        
    # 4. Fetch their profiles
    profiles_res = supabase.table('profiles').select('id, first_name, age, gender, photo_urls, course, year').in_('id', pending_ids).execute()
    return profiles_res.data
'''

if '@app.get("/likes")' not in content:
    # Insert before /matches
    content = content.replace('@app.get("/matches")', likes_endpoint + '\n@app.get("/matches")')

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated backend')