'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/utils/supabase/client'
import { useRouter } from 'next/navigation'
import BottomNav from '@/components/BottomNav'

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null)
  const supabase = createClient()
  const router = useRouter()
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) {
        router.push('/login')
        return
      }

      const { data: profiles, error } = await supabase
        .from('profiles')
        .select('*, profile_prompts(*, prompts(*)), profile_interests(*, interests(*))')
        .eq('id', session.user.id)
        .limit(1)

      if (profiles && profiles.length > 0) {
        setProfile(profiles[0])
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/login')
  }

  return (
    <div className="min-h-screen bg-rose-dark flex flex-col p-4 relative overflow-hidden font-sans">
      
      <div className="absolute top-0 left-0 w-64 h-64 bg-pink-primary/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="w-full max-w-md mx-auto flex-1 flex flex-col pt-8 pb-24 z-10 space-y-6">
        
        <div className="flex items-center justify-between mb-2">
           <h1 className="text-4xl font-serif text-white font-bold drop-shadow-md">Profile</h1>
           <button onClick={handleLogout} className="text-pink-soft text-xs font-bold uppercase tracking-widest border border-pink-soft/30 px-4 py-2 rounded-full hover:bg-white/5 transition-colors">
             Log Out
           </button>
        </div>

        {profile ? (
          <>
            <div className="luxury-glass overflow-hidden rounded-3xl p-6 flex flex-col items-center text-center">
               <div className="w-32 h-32 rounded-full bg-gradient-to-br from-pink-primary to-burgundy p-1 mb-4">
                 <div className="w-full h-full bg-rose-dark rounded-full flex items-center justify-center border-4 border-black/20 overflow-hidden">
                    {profile.photo_urls && profile.photo_urls.length > 0 ? (
                      <img src={profile.photo_urls[0]} alt="Avatar" className="w-full h-full object-cover" />
                    ) : (
                      <span className="text-5xl font-serif text-white font-bold">{profile.first_name?.[0] || 'A'}</span>
                    )}
                 </div>
               </div>
               
               <h2 className="text-3xl text-white font-serif font-bold mb-1">{profile.first_name}</h2>
               <p className="text-pink-soft text-sm font-medium">{profile.email}</p>
               
               <div className="flex gap-2 mt-4">
                 <span className="bg-white/5 border border-white/10 px-4 py-1.5 rounded-full text-xs text-white">Age: {profile.age}</span>
                 <span className="bg-white/5 border border-white/10 px-4 py-1.5 rounded-full text-xs text-white">{profile.gender || 'Not set'}</span>
               </div>
            </div>

            <div className="luxury-glass p-6 rounded-3xl">
              <h3 className="text-white font-bold text-sm mb-4">Account Status</h3>
              <div className="flex items-center justify-between p-4 bg-white/5 border border-white/10 rounded-2xl">
                 <div className="flex items-center gap-3">
                    <span className="text-2xl">🎓</span>
                    <div>
                      <p className="text-white font-bold text-sm">Bennett Student</p>
                      <p className="text-pink-soft/70 text-xs">Verified Domain</p>
                    </div>
                 </div>
                 {profile.is_verified ? (
                   <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-xs font-bold border border-green-500/30">Verified</span>
                 ) : (
                   <span className="bg-yellow-500/20 text-yellow-400 px-3 py-1 rounded-full text-xs font-bold border border-yellow-500/30">Pending</span>
                 )}
              </div>
            </div>

            {profile.profile_prompts && profile.profile_prompts.length > 0 && (
              <div className="space-y-4 w-full text-left">
                <h3 className="text-white font-bold text-sm px-2">Your Prompts</h3>
                {profile.profile_prompts.map((pp: any, i: number) => (
                  <div key={i} className="luxury-glass p-5 rounded-3xl">
                    <p className="text-pink-soft text-xs font-semibold uppercase tracking-wider mb-2">{pp.prompts?.question}</p>
                    <p className="text-white text-lg font-serif">{pp.answer}</p>
                  </div>
                ))}
              </div>
            )}

            <button onClick={() => router.push('/onboarding?edit=true')} className="button-3d text-white font-bold py-4 rounded-full w-full uppercase tracking-widest text-sm">
               Edit Profile
            </button>
          </>
        ) : (
          <div className="h-64 luxury-glass rounded-3xl skeleton flex items-center justify-center">
            <span className="text-white/50">Loading profile...</span>
          </div>
        )}

      </div>
      <BottomNav />
    </div>
  )
}
