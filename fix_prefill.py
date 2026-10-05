import re

with open('frontend/src/app/onboarding/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_prefill = '''            if (profile.photo_urls && profile.photo_urls.length > 0) {
               const paddedUrls = [...profile.photo_urls]
               while (paddedUrls.length < 3) paddedUrls.push(null)
               setPhotoPreview(paddedUrls.slice(0, 3))
               setExistingPhotoUrls(profile.photo_urls)
            }
          }
        }
      } catch(err) {'''

new_prefill = '''            if (profile.photo_urls && profile.photo_urls.length > 0) {
               const paddedUrls = [...profile.photo_urls]
               while (paddedUrls.length < 3) paddedUrls.push(null)
               setPhotoPreview(paddedUrls.slice(0, 3))
               setExistingPhotoUrls(profile.photo_urls)
            }

            // Also fetch existing prompts and prefill
            const { data: profilePrompts } = await supabase.from('profile_prompts').select('*, prompts(*)').eq('profile_id', session.user.id)
            if (profilePrompts && profilePrompts.length > 0) {
               const sPrompts = [null, null, null]
               const pAnswers = ['', '', '']
               profilePrompts.forEach(pp => {
                  if (pp.position >= 0 && pp.position < 3) {
                     sPrompts[pp.position] = pp.prompts
                     pAnswers[pp.position] = pp.answer
                  }
               })
               setSelectedPrompts(sPrompts)
               setPromptAnswers(pAnswers)
            }
          }
        }
      } catch(err) {'''

content = content.replace(old_prefill, new_prefill)

with open('frontend/src/app/onboarding/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
