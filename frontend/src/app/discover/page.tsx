'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/utils/supabase/client'
import { useRouter } from 'next/navigation'
import BottomNav from '@/components/BottomNav'

export default function DiscoverPage() {
  const [profiles, setProfiles] = useState<any[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  const supabase = createClient()
  const router = useRouter()
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

  useEffect(() => {
    fetchProfiles()
  }, [])

  const fetchProfiles = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      
      const res = await fetch(`${API_URL}/discover`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`
        }
      })
      
      if (!res.ok) throw new Error("Failed to fetch discovery feed")
      
      const data = await res.json()
      setProfiles(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async (action: 'like' | 'pass') => {
    if (currentIndex >= profiles.length) return
    const currentProfile = profiles[currentIndex]
    
    // Optimistic UI update: instantly move to next profile
    setCurrentIndex(prev => prev + 1)
    
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return

      const res = await fetch(`${API_URL}/swipe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({
          swipee_id: currentProfile.id,
          action: action
        })
      })

      if (res.ok) {
        const result = await res.json()
        if (result.status === 'match') {
          console.log("It's a Match!")
        }
      }
    } catch (err) {
      console.error("Action failed", err)
    }
  }

  if (error) {
    return (
      <div className="min-h-screen bg-rose-dark flex flex-col items-center justify-center p-4">
        <div className="luxury-glass p-8 text-center max-w-sm rounded-3xl">
          <p className="text-red-400 font-bold mb-4">Error loading profiles</p>
          <p className="text-white text-sm mb-6">{error}</p>
          <button onClick={fetchProfiles} className="button-3d text-white font-bold py-3 px-6 rounded-full text-xs uppercase tracking-widest">Try Again</button>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-rose-dark flex flex-col items-center p-4">
        <div className="w-full max-w-md flex-1 flex flex-col pt-4 pb-20">
          <div className="flex-1 luxury-glass flex flex-col overflow-hidden">
             <div className="h-[60%] skeleton border-b border-pink-primary/20"></div>
             <div className="p-4 flex-1 flex flex-col gap-4">
                <div className="h-6 w-1/2 skeleton rounded-full"></div>
                <div className="flex gap-2">
                  <div className="h-8 w-20 skeleton rounded-full"></div>
                  <div className="h-8 w-24 skeleton rounded-full"></div>
                </div>
                <div className="h-20 w-full skeleton mt-4 rounded-xl"></div>
             </div>
          </div>
          <div className="flex justify-center gap-6 mt-6">
            <div className="w-16 h-16 rounded-full skeleton"></div>
            <div className="w-16 h-16 rounded-full skeleton"></div>
          </div>
        </div>
        <BottomNav />
      </div>
    )
  }

  if (!profiles || !Array.isArray(profiles) || currentIndex >= profiles.length) {
    return (
      <div className="min-h-screen bg-rose-dark flex flex-col items-center justify-center p-4 relative overflow-hidden">
        {/* 3D Floating Elements */}
        <div className="absolute top-20 left-10 text-pink-primary opacity-20 text-6xl floating-heart">♥</div>
        <div className="absolute bottom-40 right-10 text-pink-soft opacity-30 text-8xl floating-heart" style={{ animationDelay: '2s' }}>♥</div>
        
        <div className="luxury-glass p-8 text-center max-w-sm z-10">
          <h2 className="text-3xl text-white font-serif font-bold mb-4">You're all caught up!</h2>
          <p className="text-pink-soft mb-8 text-sm">Check back later for more verified Bennett students.</p>
          <button onClick={fetchProfiles} className="w-full button-3d text-white font-bold py-4 uppercase tracking-widest text-xs">Refresh</button>
        </div>
        <BottomNav />
      </div>
    )
  }

  const profile = profiles[currentIndex]

  if (!profile) return null

  return (
    <div className="min-h-screen bg-rose-dark flex flex-col items-center p-4 overflow-hidden relative">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-pink-primary/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="w-full max-w-md flex-1 flex flex-col pt-4 pb-24 z-10">
        
        {/* Main Card */}
        <div className="flex-1 luxury-glass overflow-y-auto flex flex-col relative shadow-[0_20px_50px_rgba(42,10,24,0.5)]">
          
          {/* Full-bleed Image Section */}
          <div className="relative h-[65%] min-h-[400px] bg-black/40 flex items-center justify-center overflow-hidden">
             {profile.photo_urls && profile.photo_urls.length > 0 ? (
                <img src={profile.photo_urls[0]} alt={profile.first_name || 'User'} className="absolute inset-0 w-full h-full object-cover" />
             ) : (
                <div className="absolute inset-0 bg-gradient-to-br from-burgundy to-rose-dark flex items-center justify-center">
                   <span className="text-9xl text-white/5 font-serif font-bold">{profile.first_name?.[0] || 'A'}</span>
                </div>
             )}
             
             <div className="absolute inset-x-0 bottom-0 h-2/3 bg-gradient-to-t from-rose-dark via-rose-dark/50 to-transparent pointer-events-none"></div>
             
             {/* Text overlay on image */}
             <div className="absolute bottom-0 left-0 right-0 p-6">
                <div className="flex items-center gap-3 mb-1">
                  <h2 className="text-4xl font-bold text-white font-serif drop-shadow-md">
                    {profile.first_name || 'Anonymous'}
                  </h2>
                  <span className="bg-pink-primary text-white text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-widest shadow-[0_0_10px_rgba(224,53,102,0.5)]">
                    Verified
                  </span>
                </div>
                <p className="text-pink-soft/90 text-sm font-medium flex items-center gap-2">
                  <span className="w-2 h-2 bg-pink-primary rounded-full inline-block shadow-[0_0_5px_rgba(224,53,102,0.8)]"></span>
                  {profile.age || '18'} {profile.course ? `· ${profile.course}` : ''}
                </p>
             </div>
          </div>

          {/* Details Section */}
          <div className="p-6 flex flex-col gap-8">
            
            {/* Interests */}
            <div>
              <h3 className="text-[10px] uppercase tracking-widest text-pink-soft/80 mb-3 font-bold">Passions</h3>
              <div className="flex flex-wrap gap-2">
                {profile.profile_interests?.map((pi: any) => (
                  <span key={pi.interest_id} className="px-4 py-2 bg-white/5 border border-white/10 rounded-full text-white text-xs font-medium backdrop-blur-sm">
                    {pi.interests?.name}
                  </span>
                ))}
                {(!profile.profile_interests || profile.profile_interests.length === 0) && (
                  <span className="text-pink-soft/50 text-sm italic">No interests added.</span>
                )}
              </div>
            </div>

            {/* Prompts */}
            <div className="space-y-4">
              <h3 className="text-[10px] uppercase tracking-widest text-pink-soft/80 mb-1 font-bold">Candid Answers</h3>
              {profile.profile_prompts?.map((pp: any) => (
                <div key={pp.id} className="bg-white/5 border-l-2 border-pink-primary p-4 rounded-r-2xl">
                  <p className="text-pink-soft/70 text-xs font-semibold mb-2">{pp.prompts?.question}</p>
                  <p className="text-white text-lg font-serif leading-relaxed">{pp.answer}</p>
                </div>
              ))}
            </div>

            {/* Photos / Instagram Section */}
            {(profile.instagram_handle || (profile.photo_urls && profile.photo_urls.length > 1)) && (
              <div>
                <div className="flex items-center justify-between mb-3">
                   <h3 className="text-[10px] uppercase tracking-widest text-pink-soft/80 font-bold">More Photos</h3>
                   {profile.instagram_handle && (
                     <span className="text-pink-primary font-bold text-xs">@{profile.instagram_handle}</span>
                   )}
                </div>
                <div className="grid grid-cols-2 gap-4">
                  {(profile.photo_urls || []).slice(1, 3).map((url: string, i: number) => (
                     <div key={i} className="aspect-square bg-white/5 rounded-xl border border-white/10 overflow-hidden shadow-lg">
                        <img src={url} alt="Photo" className="w-full h-full object-cover hover:scale-105 transition-transform duration-500" />
                     </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-8 mt-8">
          <button 
            onClick={() => handleAction('pass')}
            className="w-16 h-16 rounded-full bg-black/40 border border-white/20 flex items-center justify-center text-white/50 hover:bg-black/60 hover:text-white transition-all hover:scale-105 shadow-xl backdrop-blur-md"
          >
            <span className="text-2xl font-bold">✕</span>
          </button>
          
          <button 
            onClick={() => handleAction('like')}
            className="w-16 h-16 rounded-full bg-gradient-to-br from-pink-primary to-burgundy flex items-center justify-center text-white transition-all hover:scale-110 shadow-[0_10px_30px_rgba(224,53,102,0.6)] border border-pink-soft/30"
          >
            <span className="text-3xl font-bold">♥</span>
          </button>
        </div>

      </div>

      <BottomNav />
    </div>
  )
}
