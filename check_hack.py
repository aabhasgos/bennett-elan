import os
from supabase import create_client

supabase_url = None
supabase_key = None
with open('frontend/.env.local', 'r') as f:
    for line in f:
        if line.startswith('NEXT_PUBLIC_SUPABASE_URL='): supabase_url = line.split('=', 1)[1].strip().strip('\'"')
        elif line.startswith('NEXT_PUBLIC_SUPABASE_ANON_KEY='): supabase_key = line.split('=', 1)[1].strip().strip('\'"')
supabase = create_client(supabase_url, supabase_key)

res = supabase.table('profiles').select('id, first_name, photo_urls').execute()
for p in res.data:
    urls = p.get('photo_urls', [])
    if urls:
        for u in urls:
            if 'clkdukkxstcrgheaettp.supabase.co' not in u and 'placeholder.com' not in u and 'googleusercontent' not in u:
                print(f"WEIRD URL FOUND for {p['first_name']}: {u}")
                
prompts = supabase.table('profile_prompts').select('*').execute()
for p in prompts.data:
    ans = p.get('answer', '')
    if 'hacked' in ans.lower() or 'pwned' in ans.lower():
        print(f"HACKED PROMPT: {ans}")
print("Check complete.")
