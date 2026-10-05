import re

with open('frontend/src/app/onboarding/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add state for existing photos
content = content.replace("const [photoPreview, setPhotoPreview] = useState<(string | null)[]>([null, null, null])", "const [photoPreview, setPhotoPreview] = useState<(string | null)[]>([null, null, null])\n  const [existingPhotoUrls, setExistingPhotoUrls] = useState<string[]>([])")

# 2. Update useEffect to parse edit mode and prefill
new_use_effect = '''  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession()
        if (session) {
          const isEdit = window.location.search.includes('edit=true')
          const { data: profile } = await supabase.from('profiles').select('*').eq('id', session.user.id).single()
          
          if (profile) {
            if (profile.first_name && profile.gender && !isEdit) {
              router.push('/discover')
              return
            }
            
            // Prefill data
            if (profile.first_name) setFirstName(profile.first_name)
            if (profile.age) setAge(profile.age)
            if (profile.gender) setGender(profile.gender)
            if (profile.instagram_handle) setInstagram(profile.instagram_handle)
            if (profile.photo_urls && profile.photo_urls.length > 0) {
               const paddedUrls = [...profile.photo_urls]
               while (paddedUrls.length < 3) paddedUrls.push(null)
               setPhotoPreview(paddedUrls.slice(0, 3))
               setExistingPhotoUrls(profile.photo_urls)
            }
          }
        }
      } catch(err) {
        console.error(err)
      }'''

content = re.sub(r'  useEffect\(\(\) => \{\n    const fetchData = async \(\) => \{\n      try \{\n        const \{ data: \{ session \} \} = await supabase.auth.getSession\(\)\n        if \(session\) \{\n          // Check if user is already onboarded\n          const \{ data: profile \} = await supabase.from\(\'profiles\'\).select\(\'first_name, gender\'\).eq\(\'id\', session.user.id\).single\(\)\n          if \(profile && profile.first_name && profile.gender\) \{\n            router.push\(\'/discover\'\)\n            return\n          \}\n        \}\n      \} catch\(err\) \{\n        console.error\(err\)\n      \}', new_use_effect, content, flags=re.DOTALL)

# 3. Update handleFinish to correctly merge existing photos
old_upload = '''      let urls: string[] = []
      for (let i = 0; i < photos.length; i++) {
        const file = photos[i]
        if (file) {
          const fileExt = file.name.split('.').pop()
          const fileName = `${userId}-${i}-${Math.random()}.${fileExt}`
          
          const { data, error } = await supabase.storage
            .from('profile_photos')
            .upload(fileName, file)
            
          if (error) {
             console.error("Photo upload error (bucket might not exist): ", error)
             // If storage bucket is missing in MVP, we just use a placeholder to not block the user
             urls.push(`https://placeholder.com/${fileName}`)
          } else {
             const { data: publicUrlData } = supabase.storage.from('profile_photos').getPublicUrl(fileName)
             urls.push(publicUrlData.publicUrl)
          }
        }
      }
      return urls'''

new_upload = '''      let urls: string[] = []
      for (let i = 0; i < 3; i++) {
        const file = photos[i]
        if (file) {
          const fileExt = file.name.split('.').pop()
          const fileName = `${userId}-${i}-${Math.random()}.${fileExt}`
          
          const { data, error } = await supabase.storage
            .from('profile_photos')
            .upload(fileName, file)
            
          if (error) {
             console.error("Photo upload error", error)
             urls.push(`https://placeholder.com/${fileName}`)
          } else {
             const { data: publicUrlData } = supabase.storage.from('profile_photos').getPublicUrl(fileName)
             urls.push(publicUrlData.publicUrl)
          }
        } else if (existingPhotoUrls[i]) {
          urls.push(existingPhotoUrls[i])
        }
      }
      return urls'''

content = content.replace(old_upload, new_upload)

with open('frontend/src/app/onboarding/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
