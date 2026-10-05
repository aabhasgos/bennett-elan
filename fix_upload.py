import re

with open('frontend/src/app/onboarding/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''  const uploadPhotosToSupabase = async (userId: string) => {
    const urls = []
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
    return urls
  }'''

new_func = '''  const uploadPhotosToSupabase = async (userId: string) => {
    const urls = []
    for (let i = 0; i < 3; i++) {
      const file = photos[i]
      if (file) {
        const fileExt = file.name.split('.').pop()
        const fileName = `${userId}-${i}-${Math.random()}.${fileExt}`

        const { data, error } = await supabase.storage
          .from('profile_photos')
          .upload(fileName, file)

        if (error) {
           console.error("Photo upload error (bucket might not exist): ", error)
           urls.push(`https://placeholder.com/${fileName}`)
        } else {
           const { data: publicUrlData } = supabase.storage.from('profile_photos').getPublicUrl(fileName)
           urls.push(publicUrlData.publicUrl)
        }
      } else if (photoPreview[i] && typeof photoPreview[i] === 'string' && photoPreview[i]?.startsWith('http')) {
        // Keep existing photo
        urls.push(photoPreview[i])
      }
    }
    return urls
  }'''

content = content.replace(old_func, new_func)

with open('frontend/src/app/onboarding/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
