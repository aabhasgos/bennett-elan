'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/utils/supabase/client'

const INTENTIONS = [
  { id: 'date', label: '♡ A Date' },
  { id: 'dance_partner', label: '♢ A Dance Partner' },
  { id: 'friends', label: '♧ Friends' },
  { id: 'group', label: '✦ A Group' },
  { id: 'figuring_out', label: '○ Still figuring it out' }
]

export default function OnboardingPage() {
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const [age, setAge] = useState<number | ''>('')
  const [gender, setGender] = useState<string>('')
  const [lookingFor, setLookingFor] = useState<string[]>([])
  const [intentions, setIntentions] = useState<string[]>([])
  
  const [photos, setPhotos] = useState<(File | null)>([null, null, null])
  const [photoPreview, setPhotoPreview] = useState<(string | null)[]>([null, null, null])
  
  const [availablePrompts, setAvailablePrompts] = useState<any[]>([])
  const [selectedPrompts, setSelectedPrompts] = useState<any[]>([null, null, null])
  const [promptAnswers, setPromptAnswers] = useState<string[]>(['', '', ''])
  
  const [availableInterests, setAvailableInterests] = useState<any[]>([])
  const [selectedInterests, setSelectedInterests] = useState<string[]>([])
  
  const [instagram, setInstagram] = useState('')

  const router = useRouter()
  const supabase = createClient()
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [promptsRes, interestsRes] = await Promise.all([
          fetch(`${API_URL}/prompts`),
          fetch(`${API_URL}/interests`)
        ])
        if (promptsRes.ok) setAvailablePrompts(await promptsRes.json())
        if (interestsRes.ok) setAvailableInterests(await interestsRes.json())
      } catch (err) {
        console.error("Failed to fetch initial data", err)
      }
    }
    fetchData()
  }, [])

  const handleNext = () => setStep(s => s + 1)
  const handleBack = () => setStep(s => s - 1)

  const toggleIntention = (id: string) => {
    setIntentions(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id])
  }

  const toggleInterest = (id: string) => {
    setSelectedInterests(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id])
  }

  const handlePhotoUpload = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const newPhotos: any = [...photos]
      newPhotos[index] = file
      setPhotos(newPhotos)
      
      const newPreviews = [...photoPreview]
      newPreviews[index] = URL.createObjectURL(file)
      setPhotoPreview(newPreviews)
    }
  }

  const uploadPhotosToSupabase = async (userId: string) => {
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
  }

  const handleFinish = async () => {
    setError(null)
    setLoading(true)

    try {
      const { data: { session }, error: sessionError } = await supabase.auth.getSession()
      
      if (sessionError || !session) {
        throw new Error("Session not found. Please log in again.")
      }

      // Upload photos first
      const photoUrls = await uploadPhotosToSupabase(session.user.id)

      const answers = selectedPrompts
        .map((p, i) => p ? { prompt_id: p.id, answer: promptAnswers[i], position: i } : null)
        .filter(Boolean)

      const payload = {
        profile_data: {
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
      }

      const res = await fetch(`${API_URL}/profile/setup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify(payload)
      })

      if (!res.ok) throw new Error(await res.text())
      
      router.push('/discover')
    } catch (err: any) {
      setError(err.message)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center p-4 relative overflow-hidden font-sans bg-rose-dark">
      
      <div className="absolute top-20 left-10 text-pink-primary opacity-20 text-6xl floating-heart pointer-events-none">♥</div>
      <div className="absolute bottom-40 right-10 text-pink-soft opacity-30 text-8xl floating-heart pointer-events-none" style={{ animationDelay: '2s' }}>♥</div>
      <div className="absolute top-1/2 right-20 w-32 h-32 bg-pink-primary/10 rounded-full blur-3xl pointer-events-none"></div>
      
      <div className="w-full max-w-lg mt-8 mb-20 space-y-8 z-10 relative">
        
        <div className="flex justify-between items-center mb-8 px-4">
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} className={`h-1.5 flex-1 mx-1 rounded-full transition-all duration-500 ${step >= i ? 'bg-pink-primary shadow-[0_0_10px_rgba(224,53,102,0.8)]' : 'bg-white/10'}`} />
          ))}
        </div>

        {error && (
          <div className="bg-burgundy/50 backdrop-blur-md border border-pink-primary/50 text-pink-soft p-4 rounded-2xl text-sm text-center shadow-lg">
            {error}
          </div>
        )}

        {/* STEP 1: Details & Intentions */}
        {step === 1 && (
          <div className="luxury-glass p-8 animate-in fade-in zoom-in-95 duration-500">
            <h2 className="text-4xl font-serif text-white mb-2 tracking-tight">Your Details</h2>
            <p className="text-pink-soft/80 mb-8 text-sm font-medium">Let's set up your Bennett Élan profile.</p>
            
            <div className="space-y-6">
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-champagne mb-2 ml-1">Age</label>
                  <input
                    type="number"
                    value={age}
                    onChange={(e) => setAge(parseInt(e.target.value))}
                    className="w-full bg-black/20 border border-white/10 rounded-2xl p-4 text-white focus:border-pink-primary outline-none transition-colors"
                    min="18"
                    placeholder="18+"
                  />
                </div>
                <div>
                  <label className="block text-sm text-champagne mb-2 ml-1">I am a...</label>
                  <select 
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className="w-full bg-black/20 border border-white/10 rounded-2xl p-4 text-white focus:border-pink-primary outline-none transition-colors"
                  >
                    <option value="" disabled>Select</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm text-champagne mb-2 ml-1">Looking to connect with...</label>
                <div className="flex gap-2">
                  {['Male', 'Female', 'Everyone'].map(g => (
                    <button
                      key={g}
                      onClick={() => setLookingFor([g])}
                      className={`flex-1 py-3 rounded-xl border text-sm font-semibold transition-all ${
                        lookingFor.includes(g) 
                          ? 'bg-pink-primary border-pink-primary text-white shadow-lg' 
                          : 'bg-black/20 border-white/10 text-white/70 hover:border-white/30'
                      }`}
                    >
                      {g}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm text-champagne mb-4 ml-1">What are you here for?</label>
                <div className="grid grid-cols-1 gap-2">
                  {INTENTIONS.map(intent => (
                    <button
                      key={intent.id}
                      onClick={() => toggleIntention(intent.id)}
                      className={`w-full text-left p-4 rounded-2xl border transition-all duration-300 ${
                        intentions.includes(intent.id) 
                          ? 'bg-gradient-to-r from-pink-primary/20 to-burgundy/40 border-pink-primary text-white shadow-md' 
                          : 'bg-black/20 border-white/10 text-white/70 hover:border-white/30'
                      }`}
                    >
                      {intent.label}
                    </button>
                  ))}
                </div>
              </div>

              <button 
                onClick={handleNext} 
                disabled={!age || age < 18 || !gender || lookingFor.length === 0 || intentions.length === 0}
                className="w-full button-3d text-white font-bold py-4 mt-8 disabled:opacity-50 tracking-wide"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: Photos */}
        {step === 2 && (
          <div className="luxury-glass p-8 animate-in fade-in zoom-in-95 duration-500">
            <h2 className="text-4xl font-serif text-white mb-2 tracking-tight">Your Photos</h2>
            <p className="text-pink-soft/80 mb-8 text-sm font-medium">Please upload exactly 3 photos (Required).</p>

            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2 relative aspect-[3/4] bg-black/30 rounded-3xl border-2 border-dashed border-white/20 flex flex-col items-center justify-center overflow-hidden group hover:border-pink-primary transition-colors cursor-pointer">
                {photoPreview[0] ? (
                  <img src={photoPreview[0]} className="w-full h-full object-cover" alt="Primary" />
                ) : (
                  <>
                    <span className="text-4xl mb-2 text-pink-primary">📸</span>
                    <span className="text-sm font-medium text-white/70">Main Profile Photo</span>
                  </>
                )}
                <input type="file" accept="image/*" onChange={(e) => handlePhotoUpload(0, e)} className="absolute inset-0 opacity-0 cursor-pointer" />
              </div>

              {[1, 2].map(index => (
                <div key={index} className="relative aspect-square bg-black/30 rounded-2xl border-2 border-dashed border-white/20 flex flex-col items-center justify-center overflow-hidden hover:border-pink-primary transition-colors cursor-pointer">
                  {photoPreview[index] ? (
                     <img src={photoPreview[index]} className="w-full h-full object-cover" alt={`Photo ${index+1}`} />
                  ) : (
                    <span className="text-2xl text-white/30">+</span>
                  )}
                  <input type="file" accept="image/*" onChange={(e) => handlePhotoUpload(index, e)} className="absolute inset-0 opacity-0 cursor-pointer" />
                </div>
              ))}
            </div>

            <div className="flex gap-4 mt-8">
              <button onClick={handleBack} className="px-6 py-4 rounded-full border border-white/20 text-white hover:bg-white/5 transition-colors">Back</button>
              <button 
                onClick={handleNext}
                disabled={photoPreview.includes(null)}
                className="flex-1 button-3d text-white font-bold py-4 disabled:opacity-50"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: Prompts */}
        {step === 3 && (
          <div className="luxury-glass p-8 animate-in fade-in zoom-in-95 duration-500">
            <h2 className="text-4xl font-serif text-white mb-2 tracking-tight">Be Candid</h2>
            <p className="text-pink-soft/80 mb-8 text-sm font-medium">Answer all 3 prompts. Show your true personality.</p>

            <div className="space-y-6">
              {[0, 1, 2].map(index => (
                <div key={index} className="space-y-3 p-5 rounded-2xl bg-black/20 border border-white/10 focus-within:border-pink-primary/50 transition-colors">
                  <select 
                    className="w-full bg-transparent text-pink-soft text-sm font-semibold outline-none pb-2 border-b border-white/10"
                    value={selectedPrompts[index]?.id || ''}
                    onChange={(e) => {
                      const p = availablePrompts.find(x => x.id === e.target.value)
                      const newSelected = [...selectedPrompts]
                      newSelected[index] = p
                      setSelectedPrompts(newSelected)
                    }}
                  >
                    <option value="" className="bg-rose-dark text-white/50">Select a prompt...</option>
                    {availablePrompts.map(p => (
                      <option key={p.id} value={p.id} className="bg-rose-dark">{p.question}</option>
                    ))}
                  </select>
                  
                  <textarea
                    placeholder="Your candid answer..."
                    value={promptAnswers[index]}
                    onChange={(e) => {
                      const newAns = [...promptAnswers]
                      newAns[index] = e.target.value
                      setPromptAnswers(newAns)
                    }}
                    className="w-full bg-transparent text-white font-serif text-lg resize-none outline-none h-20 placeholder:text-white/20"
                  />
                </div>
              ))}
            </div>

            <div className="flex gap-4 mt-8">
              <button onClick={handleBack} className="px-6 py-4 rounded-full border border-white/20 text-white hover:bg-white/5 transition-colors">Back</button>
              <button 
                onClick={handleNext}
                disabled={selectedPrompts.includes(null) || promptAnswers.some(a => a.trim() === '')}
                className="flex-1 button-3d text-white font-bold py-4 disabled:opacity-50"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* STEP 4: Interests */}
        {step === 4 && (
          <div className="luxury-glass p-8 animate-in fade-in zoom-in-95 duration-500">
            <h2 className="text-4xl font-serif text-white mb-2 tracking-tight">Your Passions</h2>
            <p className="text-pink-soft/80 mb-8 text-sm font-medium">Select a few things you enjoy to find your people.</p>

            <div className="flex flex-wrap gap-3">
              {availableInterests.map(interest => (
                <button
                  key={interest.id}
                  onClick={() => toggleInterest(interest.id)}
                  className={`px-5 py-2.5 rounded-full border text-sm font-medium transition-all duration-300 ${
                    selectedInterests.includes(interest.id)
                      ? 'bg-pink-primary border-pink-primary text-white shadow-[0_0_15px_rgba(224,53,102,0.4)]'
                      : 'bg-black/20 border-white/10 text-white/70 hover:border-white/30'
                  }`}
                >
                  {interest.name}
                </button>
              ))}
            </div>

            <div className="flex gap-4 mt-12">
              <button onClick={handleBack} className="px-6 py-4 rounded-full border border-white/20 text-white hover:bg-white/5 transition-colors">Back</button>
              <button 
                onClick={handleNext}
                disabled={selectedInterests.length === 0}
                className="flex-1 button-3d text-white font-bold py-4 disabled:opacity-50"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* STEP 5: Finalize */}
        {step === 5 && (
          <div className="luxury-glass p-10 animate-in fade-in zoom-in-95 duration-500 text-center relative overflow-hidden">
            
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(224,53,102,0.2),transparent_70%)] pointer-events-none"></div>

            <div className="w-24 h-24 bg-gradient-to-br from-pink-primary to-burgundy rounded-full flex items-center justify-center mx-auto mb-6 shadow-[0_0_30px_rgba(224,53,102,0.5)] relative z-10 border border-white/20">
              <span className="text-4xl">✨</span>
            </div>
            
            <h2 className="text-4xl font-serif text-white mb-2 tracking-tight relative z-10">Almost Ready</h2>
            <p className="text-pink-soft/80 mb-8 text-sm font-medium relative z-10">Connect your Instagram for a fully candid profile.</p>

            <div className="text-left mb-8 relative z-10">
              <label className="block text-sm text-champagne mb-2 ml-1">Instagram Handle (Optional)</label>
              <div className="flex items-center bg-black/20 border border-white/10 rounded-2xl p-4 focus-within:border-pink-primary transition-colors">
                <span className="text-pink-primary mr-3 text-lg">@</span>
                <input
                  type="text"
                  value={instagram}
                  onChange={(e) => setInstagram(e.target.value)}
                  placeholder="username"
                  className="w-full bg-transparent text-white outline-none font-medium text-lg"
                />
              </div>
            </div>

            <div className="flex gap-4 mt-8 relative z-10">
              <button onClick={handleBack} disabled={loading} className="px-6 py-4 rounded-full border border-white/20 text-white hover:bg-white/5 transition-colors">Back</button>
              <button 
                onClick={handleFinish}
                disabled={loading}
                className="flex-1 button-3d text-white font-bold py-4 disabled:opacity-50 flex items-center justify-center text-lg"
              >
                {loading ? 'Uploading...' : 'Enter Bennett Élan'}
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  )
}
