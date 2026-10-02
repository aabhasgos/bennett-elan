import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def setup_all():
    try:
        # Create storage bucket for photos
        print("Creating storage bucket 'profile_photos'...")
        supabase.storage.create_bucket("profile_photos", {"public": True})
        print("Bucket created.")
    except Exception as e:
        print(f"Bucket might exist or error: {e}")

    try:
        # We need a place to store photo URLs. The easiest is adding an array column to profiles.
        # But we can't do DDL through the REST API directly without RPC.
        print("Please ensure you run the SQL to add photo_urls column.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    setup_all()
