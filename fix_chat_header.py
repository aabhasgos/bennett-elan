import re

with open('frontend/src/app/chat/[id]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add state
state_code = '''  const [messages, setMessages] = useState<any[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [userId, setUserId] = useState<string | null>(null)
  const [partnerProfile, setPartnerProfile] = useState<any>(null)'''
content = re.sub(r'  const \[messages, setMessages\] = useState<any\[\]>\(\[\]\)\n  const \[newMessage, setNewMessage\] = useState\(\'\'\)\n  const \[userId, setUserId\] = useState<string \| null>\(null\)', state_code, content)

# 2. Add fetch logic in useEffect
fetch_logic = '''
  useEffect(() => {
    const fetchPartnerProfile = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return
      const { data: match } = await supabase.from('matches').select('user1_id, user2_id').eq('id', matchId).single()
      if (match) {
        const partnerId = match.user1_id === session.user.id ? match.user2_id : match.user1_id
        const { data: profile } = await supabase.from('profiles').select('first_name, photo_urls').eq('id', partnerId).single()
        setPartnerProfile(profile)
      }
    }
    fetchPartnerProfile()
'''
content = content.replace('  useEffect(() => {\n    fetchSession()\n    fetchMessages()', fetch_logic + '    fetchSession()\n    fetchMessages()')

# 3. Update Header HTML
header_old = '''        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-pink-primary/20 flex items-center justify-center border border-pink-primary/50">
            <span className="text-xl">?</span>
          </div>
          <div>
            <h2 className="text-white font-bold font-serif">Ball Night Match</h2>
            <p className="text-pink-soft/70 text-xs">Plan your night together</p>
          </div>
        </div>'''

header_new = '''        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-pink-primary/20 flex items-center justify-center border border-pink-primary/50 overflow-hidden shrink-0">
            {partnerProfile?.photo_urls?.[0] ? (
              <img src={partnerProfile.photo_urls[0]} alt="Partner" className="w-full h-full object-cover" />
            ) : (
              <span className="text-xl font-bold font-serif text-pink-soft">{partnerProfile?.first_name?.[0] || '?'}</span>
            )}
          </div>
          <div>
            <h2 className="text-white font-bold font-serif">{partnerProfile ? partnerProfile.first_name : 'Loading...'}</h2>
            <p className="text-pink-soft/70 text-xs">Plan your night together</p>
          </div>
        </div>'''

content = content.replace(header_old, header_new)

with open('frontend/src/app/chat/[id]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
