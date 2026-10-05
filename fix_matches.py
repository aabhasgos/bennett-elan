import re

with open('frontend/src/app/matches/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State changes
state_code = '''  const [matches, setMatches] = useState<any[]>([])
  const [likes, setLikes] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedLike, setSelectedLike] = useState<any | null>(null)
  const [matchData, setMatchData] = useState<{profile: any, match_id: string} | null>(null)'''
content = re.sub(r'  const \[matches, setMatches\] = useState<any\[\]>\(\[\]\)\n  const \[loading, setLoading\] = useState\(true\)', state_code, content)

# 2. Fetch changes
fetch_code = '''  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) {
        router.push('/login')
        return
      }

      // Fetch matches
      const matchesRes = await fetch(${API_URL}/matches, {
        headers: { 'Authorization': Bearer  }
      })
      if (matchesRes.ok) setMatches(await matchesRes.json())
      
      // Fetch incoming likes
      const likesRes = await fetch(${API_URL}/likes, {
        headers: { 'Authorization': Bearer  }
      })
      if (likesRes.ok) setLikes(await likesRes.json())

    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAction = async (action: 'like' | 'pass') => {
    if (!selectedLike) return
    const currentProfile = selectedLike
    
    // Optimistic UI
    setLikes(prev => prev.filter(p => p.id !== currentProfile.id))
    setSelectedLike(null)

    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return

      const res = await fetch(${API_URL}/swipe, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': Bearer 
        },
        body: JSON.stringify({
          swipee_id: currentProfile.id,
          action: action
        })
      })

      if (res.ok) {
        const result = await res.json()
        if (result.status === 'match' && result.match_id) {
          setMatchData({ profile: currentProfile, match_id: result.match_id })
          // Refresh matches in background
          fetchData()
        }
      }
    } catch (err) {
      console.error("Action failed", err)
    }
  }'''
content = re.sub(r'  useEffect\(\(\) => \{\n    fetchMatches\(\)\n  \}, \[\]\)\n\n  const fetchMatches = async \(\) => \{.*?\}\n  \}', fetch_code, content, flags=re.DOTALL)

# 3. UI Changes: add Likes horizontal row before matches list
likes_ui = '''        {/* Incoming Likes Section */}
        {!loading && likes.length > 0 && (
          <div className="mb-10">
            <h2 className="text-xl font-serif text-white font-bold mb-4 drop-shadow-md">Likes You ({likes.length})</h2>
            <div className="flex gap-4 overflow-x-auto pb-4 snap-x hide-scrollbar">
              {likes.map(like => (
                <div 
                  key={like.id} 
                  onClick={() => setSelectedLike(like)}
                  className="snap-start flex-shrink-0 w-32 h-44 rounded-2xl overflow-hidden relative cursor-pointer border border-pink-primary/30 shadow-[0_10px_20px_rgba(224,53,102,0.3)] hover:scale-105 transition-transform"
                >
                  <img 
                    src={like.photo_urls?.[0]} 
                    className="w-full h-full object-cover blur-sm" 
                    alt="Like" 
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-rose-dark/90 via-rose-dark/40 to-transparent flex flex-col justify-end p-3">
                    <span className="text-white font-bold font-serif text-lg">{like.first_name}</span>
                    <span className="text-pink-primary font-bold text-xs">Tap to view</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex items-center justify-between mb-8">'''
content = content.replace('        <div className="flex items-center justify-between mb-8">', likes_ui)

# 4. Add modals at the bottom
modals_ui = '''      </div>

      {/* Selected Like Modal */}
      {selectedLike && (
        <div className="fixed inset-0 z-40 flex flex-col items-center justify-center bg-black/90 backdrop-blur-md px-4 animate-in fade-in duration-300">
          <div className="w-full max-w-sm luxury-glass p-2 relative overflow-hidden flex flex-col h-[70vh]">
            <img src={selectedLike.photo_urls?.[0]} className="w-full h-full object-cover rounded-xl" />
            <div className="absolute bottom-2 left-2 right-2 bg-rose-dark/90 p-4 rounded-xl backdrop-blur-md border border-white/10 text-center">
               <h2 className="text-2xl font-serif text-white font-bold">{selectedLike.first_name}, {selectedLike.age}</h2>
               <p className="text-pink-soft text-sm mt-1">{selectedLike.course} {selectedLike.year}</p>
               <div className="flex justify-center gap-6 mt-6">
                 <button onClick={() => handleAction('pass')} className="w-14 h-14 rounded-full bg-black/50 border border-white/20 text-white flex items-center justify-center text-xl hover:bg-black/70 transition-all">✕</button>
                 <button onClick={() => handleAction('like')} className="w-14 h-14 rounded-full bg-gradient-to-br from-pink-primary to-burgundy text-white flex items-center justify-center text-3xl shadow-[0_5px_20px_rgba(224,53,102,0.6)] transition-all">♥</button>
               </div>
            </div>
          </div>
          <button onClick={() => setSelectedLike(null)} className="mt-6 text-white/50 text-sm tracking-widest uppercase hover:text-white">Close</button>
        </div>
      )}

      {/* Match Overlay */}
      {matchData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4 animate-in fade-in zoom-in-95 duration-300">
          <div className="text-center w-full max-w-sm flex flex-col items-center">
            <h2 className="text-4xl font-serif font-bold text-champagne mb-2 italic">It's a Match!</h2>
            <p className="text-white/80 text-sm tracking-widest uppercase mb-10">You and {matchData.profile.first_name} liked each other.</p>
            
            <div className="relative w-48 h-48 mb-12">
              <div className="absolute inset-0 bg-pink-primary rounded-full blur-[50px] opacity-50 animate-pulse"></div>
              <div className="w-48 h-48 rounded-full border-4 border-champagne overflow-hidden relative z-10 shadow-2xl">
                <img 
                  src={matchData.profile.photo_urls?.[0]} 
                  alt={matchData.profile.first_name} 
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            <div className="w-full space-y-4">
              <button 
                onClick={() => router.push('/chat/' + matchData.match_id)}
                className="w-full button-3d text-white font-bold py-4 rounded-full shadow-lg"
              >
                Send a Message
              </button>
              <button 
                onClick={() => setMatchData(null)}
                className="w-full border border-white/20 text-white font-bold py-4 rounded-full hover:bg-white/10 transition-colors"
              >
                Go Back
              </button>
            </div>
          </div>
        </div>
      )}

      <BottomNav />'''
content = content.replace('      </div>\n      <BottomNav />', modals_ui)

with open('frontend/src/app/matches/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated matches page')