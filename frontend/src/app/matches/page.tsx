'use client'

import { useState, useEffect } from 'react'
import { createClient } from '@/utils/supabase/client'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import BottomNav from '@/components/BottomNav'

export default function MatchesPage() {
  const [matches, setMatches] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  
  const supabase = createClient()
  const router = useRouter()
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

  useEffect(() => {
    fetchMatches()
  }, [])

  const fetchMatches = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) {
        router.push('/login')
        return
      }

      const res = await fetch(`${API_URL}/matches`, {
        headers: { 'Authorization': `Bearer ${session.access_token}` }
      })
      
      if (res.ok) {
        const data = await res.json()
        setMatches(data)
      }
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-rose-dark flex flex-col p-4 relative overflow-hidden font-sans">
      
      {/* 3D Background */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-pink-primary/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="w-full max-w-md mx-auto flex-1 flex flex-col pt-8 pb-24 z-10">
        
        <div className="flex items-center justify-between mb-8">
           <h1 className="text-4xl font-serif text-white font-bold drop-shadow-md">Matches</h1>
           <span className="bg-pink-primary/20 text-pink-primary px-3 py-1 rounded-full text-xs font-bold border border-pink-primary/30">
             {matches.length}
           </span>
        </div>

        {loading ? (
          <div className="space-y-4">
             {[1,2,3].map(i => (
               <div key={i} className="luxury-glass p-4 flex items-center gap-4">
                  <div className="w-16 h-16 rounded-full skeleton"></div>
                  <div className="flex-1 space-y-2">
                     <div className="h-4 w-1/3 skeleton rounded"></div>
                     <div className="h-3 w-1/2 skeleton rounded"></div>
                  </div>
               </div>
             ))}
          </div>
        ) : matches.length === 0 ? (
          <div className="luxury-glass p-8 text-center mt-10">
            <span className="text-6xl mb-4 block">💌</span>
            <h2 className="text-2xl text-white font-serif mb-2">No matches yet</h2>
            <p className="text-pink-soft text-sm">Keep swiping to find your people for Ball Night.</p>
            <Link href="/discover" className="inline-block mt-6 px-6 py-3 button-3d text-white font-bold rounded-full text-sm">
              Keep Discovering
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {matches.map(match => (
              <Link key={match.match_id} href={`/chat/${match.match_id}`}>
                <div className="luxury-glass p-4 flex items-center gap-4 transition-transform hover:scale-[1.02] cursor-pointer group">
                  
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-pink-primary to-burgundy p-0.5">
                    <div className="w-full h-full rounded-full bg-rose-dark flex items-center justify-center border-2 border-transparent group-hover:border-white/20 transition-all">
                       <span className="text-2xl font-serif text-pink-soft font-bold">
                         {match.profile.first_name[0]}
                       </span>
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="text-lg text-white font-bold font-serif">{match.profile.first_name}</h3>
                    <p className="text-pink-soft/70 text-xs">Tap to chat & plan your night ✨</p>
                  </div>
                  
                  <div className="text-white/20 group-hover:text-pink-primary transition-colors">
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

      </div>
      <BottomNav />
    </div>
  )
}
