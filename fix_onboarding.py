import re

with open('frontend/src/app/onboarding/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of the useEffect
pattern = r'  useEffect\(\(\) => \{\n    const fetchData = async \(\) => \{'
replacement = '''  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession()
        if (session) {
          // Check if user is already onboarded
          const { data: profile } = await supabase.from('profiles').select('first_name, gender').eq('id', session.user.id).single()
          if (profile && profile.first_name && profile.gender) {
            router.push('/discover')
            return
          }
        }
      } catch(err) {
        console.error(err)
      }
'''
content = re.sub(pattern, replacement, content)

with open('frontend/src/app/onboarding/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)