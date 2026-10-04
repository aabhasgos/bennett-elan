from fastapi import FastAPI, HTTPException, Depends, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

app = FastAPI(title="Bennett Élan API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows Vercel frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- Models ---
class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    course: Optional[str] = None
    year: Optional[str] = None
    instagram_handle: Optional[str] = None
    photo_urls: Optional[List[str]] = None

class PreferencesUpdate(BaseModel):
    intentions: List[str]
    looking_for_gender: List[str]
    min_age: int
    max_age: int

class PromptAnswer(BaseModel):
    prompt_id: str
    answer: str
    position: int

# --- Auth Dependency ---
async def get_user_id(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No authorization header")
        
    try:
        token = authorization.split(" ")[1]
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Bennett Élan API is running."}

@app.get("/prompts")
def get_active_prompts():
    response = supabase.table('prompts').select('*').eq('is_active', True).execute()
    return response.data

@app.get("/interests")
def get_interests():
    response = supabase.table('interests').select('*').execute()
    return response.data

@app.post("/profile/setup")
async def setup_profile(
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
        
    return {"status": "success", "message": "Profile setup complete."}

@app.get("/discover")
async def get_discovery_profiles(user_id: str = Depends(get_user_id)):
    # 1. Get user preferences
    prefs_res = supabase.table('preferences').select('*').eq('profile_id', user_id).execute()
    if not prefs_res.data:
        raise HTTPException(status_code=400, detail="Preferences not set")
    
    user_prefs = prefs_res.data[0]
    looking_for = user_prefs.get('looking_for_gender', [])
    
    # 2. Get swiped profile IDs to exclude them
    swipes_res = supabase.table('swipes').select('swipee_id').eq('swiper_id', user_id).execute()
    swiped_ids = [s['swipee_id'] for s in swipes_res.data]
    swiped_ids.append(user_id) # Exclude self
    
    # 3. Query profiles
    query = supabase.table('profiles')\
        .select('*, profile_prompts(*, prompts(*)), profile_interests(*, interests(*))')
        
    if looking_for and 'everyone' not in [g.lower() for g in looking_for]:
        query = query.in_('gender', looking_for)
        
    profiles_res = query.execute()
        
    # Filter out swiped profiles
    discovery_feed = [p for p in profiles_res.data if p['id'] not in swiped_ids]
    return discovery_feed
    
class SwipeAction(BaseModel):
    swipee_id: str
    action: str

class ChatMessage(BaseModel):
    content: str

@app.post("/swipe")
async def process_swipe(swipe: SwipeAction, user_id: str = Depends(get_user_id)):
    # Insert swipe
    supabase.table('swipes').upsert({
        "swiper_id": user_id,
        "swipee_id": swipe.swipee_id,
        "action": swipe.action
    }).execute()
    
    # Check for mutual match
    if swipe.action == 'like':
        mutual = supabase.table('swipes')\
            .select('*')\
            .eq('swiper_id', swipe.swipee_id)\
            .eq('swipee_id', user_id)\
            .eq('action', 'like')\
            .execute()
            
        if mutual.data:
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
            return {"status": "match", "match_id": match_id}
            
    return {"status": "success"}


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

@app.get("/matches")
async def get_matches(user_id: str = Depends(get_user_id)):
    matches = supabase.table('matches')\
        .select('*')\
        .or_(f"user1_id.eq.{user_id},user2_id.eq.{user_id}")\
        .execute()
        
    result = []
    for m in matches.data:
        other_id = m['user1_id'] if m['user2_id'] == user_id else m['user2_id']
        profile = supabase.table('profiles').select('id, first_name, age, gender').eq('id', other_id).execute()
        if profile.data:
            result.append({
                "match_id": m['id'],
                "created_at": m['created_at'],
                "profile": profile.data[0]
            })
            
    return result

@app.get("/chat/{match_id}")
async def get_chat(match_id: str, user_id: str = Depends(get_user_id)):
    messages = supabase.table('messages')\
        .select('*')\
        .eq('match_id', match_id)\
        .order('created_at', desc=False)\
        .execute()
    return messages.data

@app.post("/chat/{match_id}")
async def send_message(match_id: str, msg: ChatMessage, user_id: str = Depends(get_user_id)):
    res = supabase.table('messages').insert({
        "match_id": match_id,
        "sender_id": user_id,
        "content": msg.content
    }).execute()
    return res.data[0]
