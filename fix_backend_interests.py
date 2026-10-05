import re

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Import Body
if 'from fastapi import FastAPI, HTTPException, Depends, Header, Body' not in content:
    content = content.replace(
        'from fastapi import FastAPI, HTTPException, Depends, Header',
        'from fastapi import FastAPI, HTTPException, Depends, Header, Body'
    )

old_sig = '''async def setup_profile(
    profile_data: ProfileUpdate, 
    preferences_data: PreferencesUpdate,
    answers: List[PromptAnswer],
    user_id: str = Depends(get_user_id)
):
    profile_dict = profile_data.dict(exclude_unset=True)
    if profile_dict:
        supabase.table('profiles').update(profile_dict).eq('id', user_id).execute()
        
    prefs = preferences_data.dict()
    prefs['profile_id'] = user_id
    supabase.table('preferences').upsert(prefs).execute()
    
    for ans in answers:
        supabase.table('profile_prompts').upsert({
            "profile_id": user_id,
            "prompt_id": ans.prompt_id,
            "answer": ans.answer,
            "position": ans.position
        }).execute()
        
    return {"status": "success", "message": "Profile setup complete."}'''

new_sig = '''async def setup_profile(
    profile_data: ProfileUpdate, 
    preferences_data: PreferencesUpdate,
    answers: List[PromptAnswer],
    interests: List[str] = Body(default=[]),
    user_id: str = Depends(get_user_id)
):
    profile_dict = profile_data.dict(exclude_unset=True)
    if profile_dict:
        supabase.table('profiles').update(profile_dict).eq('id', user_id).execute()
        
    prefs = preferences_data.dict()
    prefs['profile_id'] = user_id
    supabase.table('preferences').upsert(prefs).execute()
    
    # Answers
    for ans in answers:
        supabase.table('profile_prompts').upsert({
            "profile_id": user_id,
            "prompt_id": ans.prompt_id,
            "answer": ans.answer,
            "position": ans.position
        }).execute()
        
    # Interests
    if interests:
        # Clear old interests
        supabase.table('profile_interests').delete().eq('profile_id', user_id).execute()
        # Insert new
        interest_records = [{"profile_id": user_id, "interest_id": i_id} for i_id in interests]
        if interest_records:
            supabase.table('profile_interests').insert(interest_records).execute()
        
    return {"status": "success", "message": "Profile setup complete."}'''

content = content.replace(old_sig, new_sig)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
