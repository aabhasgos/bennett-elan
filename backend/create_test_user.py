import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY") # Service role key

supabase: Client = create_client(url, key)

try:
    # Check if user exists
    res = supabase.auth.admin.list_users()
    exists = any(u.email == "test@bennett.edu.in" for u in res)
    
    if not exists:
        user = supabase.auth.admin.create_user({
            "email": "test@bennett.edu.in",
            "password": "password123",
            "email_confirm": True
        })
        print("Successfully created auto-verified test user.")
    else:
        print("Test user already exists.")
except Exception as e:
    print(f"Error: {e}")
