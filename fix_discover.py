import re

with open('frontend/src/app/discover/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add match state
state_code = '''  const [profiles, setProfiles] = useState<any[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // New Match State
  const [matchData, setMatchData] = useState<{profile: any, match_id: string} | null>(null)'''
content = re.sub(r'  const \[profiles, setProfiles\] = useState<any\[\]>\(\[\]\)\n  const \[currentIndex, setCurrentIndex\] = useState\(0\)\n  const \[loading, setLoading\] = useState\(true\)\n  const \[error, setError\] = useState<string \| null>\(null\)', state_code, content)

# 2. Update handleAction to set matchData instead of just console.log
action_code = '''      if (res.ok) {
        const result = await res.json()
        if (result.status === 'match' && result.match_id) {
          setMatchData({ profile: currentProfile, match_id: result.match_id })
        }
      }'''
content = re.sub(r'      if \(res\.ok\) \{\n        const result = await res\.json\(\)\n        if \(result\.status === \'match\'\) \{\n          console\.log\("It\'s a Match!"\)\n        \}\n      \}', action_code, content)

# 3. Add match overlay UI just before <BottomNav />
match_ui = '''      </div>

      {/* Match Overlay */}
      {matchData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4 animate-in fade-in duration-300">
          <div className="text-center w-full max-w-sm flex flex-col items-center">
            <h2 className="text-4xl font-serif font-bold text-champagne mb-2 italic">It's a Match!</h2>
            <p className="text-white/80 text-sm tracking-widest uppercase mb-10">You and {matchData.profile.first_name} liked each other.</p>
            
            <div className="relative w-48 h-48 mb-12">
              <div className="absolute inset-0 bg-pink-primary rounded-full blur-[50px] opacity-50 animate-pulse"></div>
              <div className="w-48 h-48 rounded-full border-4 border-champagne overflow-hidden relative z-10 shadow-2xl">
                <img 
                  src={(matchData.profile.photo_urls && matchData.profile.photo_urls.length > 0) ? matchData.profile.photo_urls[0] : ''} 
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
                Keep Swiping
              </button>
            </div>
          </div>
        </div>
      )}

      <BottomNav />'''
content = content.replace('      </div>\n\n      <BottomNav />', match_ui)

with open('frontend/src/app/discover/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated discover page')