import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def seed_profiles():
    dummies = [
        {"email": "daphne@bennett.edu.in", "name": "Daphne", "gender": "Female", "age": 19},
        {"email": "simon@bennett.edu.in", "name": "Simon", "gender": "Male", "age": 21},
        {"email": "kate@bennett.edu.in", "name": "Kate", "gender": "Female", "age": 20},
    ]

    for d in dummies:
        try:
            # Check if exists
            res = supabase.auth.admin.list_users()
            exists = any(u.email == d["email"] for u in res)
            
            if not exists:
                user_res = supabase.auth.admin.create_user({
                    "email": d["email"],
                    "password": "password123",
                    "email_confirm": True
                })
                uid = user_res.user.id
                
                # Update profile
                supabase.table('profiles').update({
                    "first_name": d["name"],
                    "age": d["age"],
                    "gender": d["gender"],
                    "is_verified": True
                }).eq("id", uid).execute()
                
                print(f"Created dummy: {d['name']}")
            else:
                print(f"Dummy {d['name']} already exists.")
        except Exception as e:
            print(f"Error creating {d['name']}: {e}")

if __name__ == "__main__":
    seed_profiles()
