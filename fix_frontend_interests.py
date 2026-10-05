import re

with open('frontend/src/app/onboarding/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_payload = '''      const payload = {
        profile_data: {
          first_name: firstName,
          age: Number(age),
          gender: gender,
          instagram_handle: instagram || null,
          photo_urls: photoUrls
        },
        preferences_data: {
          intentions,
          looking_for_gender: lookingFor,
          min_age: 18,
          max_age: 25
        },
        answers
      }'''

new_payload = '''      const payload = {
        profile_data: {
          first_name: firstName,
          age: Number(age),
          gender: gender,
          instagram_handle: instagram || null,
          photo_urls: photoUrls
        },
        preferences_data: {
          intentions,
          looking_for_gender: lookingFor,
          min_age: 18,
          max_age: 25
        },
        answers,
        interests: selectedInterests
      }'''

content = content.replace(old_payload, new_payload)

old_prefill = '''            const { data: profilePrompts } = await supabase.from('profile_prompts').select('*, prompts(*)').eq('profile_id', session.user.id)
            if (profilePrompts && profilePrompts.length > 0) {
               const sPrompts = [null, null, null]
               const pAnswers = ['', '', '']
               profilePrompts.forEach((pp: any) => {
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

new_prefill = '''            const { data: profilePrompts } = await supabase.from('profile_prompts').select('*, prompts(*)').eq('profile_id', session.user.id)
            if (profilePrompts && profilePrompts.length > 0) {
               const sPrompts = [null, null, null]
               const pAnswers = ['', '', '']
               profilePrompts.forEach((pp: any) => {
                  if (pp.position >= 0 && pp.position < 3) {
                     sPrompts[pp.position] = pp.prompts
                     pAnswers[pp.position] = pp.answer
                  }
               })
               setSelectedPrompts(sPrompts)
               setPromptAnswers(pAnswers)
            }
            
            // Also fetch existing interests
            const { data: profileInterests } = await supabase.from('profile_interests').select('interest_id').eq('profile_id', session.user.id)
            if (profileInterests && profileInterests.length > 0) {
               setSelectedInterests(profileInterests.map((pi: any) => pi.interest_id))
            }
          }
        }
      } catch(err) {'''

content = content.replace(old_prefill, new_prefill)

with open('frontend/src/app/onboarding/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
