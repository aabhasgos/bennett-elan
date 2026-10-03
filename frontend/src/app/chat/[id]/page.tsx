'use client'

import { useState, useEffect, useRef } from 'react'
import { createClient } from '@/utils/supabase/client'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'

export default function ChatPage() {
  const params = useParams()
  const router = useRouter()
  const matchId = params.id as string
  
  const [messages, setMessages] = useState<any[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [userId, setUserId] = useState<string | null>(null)
  const [partnerProfile, setPartnerProfile] = useState<any>(null)
  
  const supabase = createClient()
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'
  const messagesEndRef = useRef<HTMLDivElement>(null)


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
    fetchSession()
    fetchMessages()
    
    // (In a real app, set up Supabase realtime subscription here)
    const interval = setInterval(fetchMessages, 3000)
    return () => clearInterval(interval)
  }, [matchId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchSession = async () => {
     const { data } = await supabase.auth.getSession()
     if (data.session) setUserId(data.session.user.id)
     // Fallback for dev bypass logic if needed, but chat needs real UUID to differentiate sender/receiver.
     // For MVP, we will rely on the token logic.
  }

  const fetchMessages = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return

      const res = await fetch(`${API_URL}/chat/${matchId}`, {
        headers: { 'Authorization': `Bearer ${session.access_token}` }
      })
      
      if (res.ok) {
        const data = await res.json()
        setMessages(data)
      }
    } catch (err) {
      console.error(err)
    }
  }

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newMessage.trim()) return
    
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return

      await fetch(`${API_URL}/chat/${matchId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({ content: newMessage })
      })
      
      setNewMessage('')
      fetchMessages() // Refresh instantly
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="min-h-screen bg-rose-dark flex flex-col relative overflow-hidden font-sans">
      
      {/* Header */}
      <div className="bg-rose-dark/90 backdrop-blur-md border-b border-white/10 p-4 sticky top-0 z-50 flex items-center gap-4">
        <button onClick={() => router.push('/matches')} className="text-pink-soft hover:text-white transition-colors">
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div className="flex items-center gap-3">
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
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-24">
        
        {/* Icebreaker */}
        <div className="flex justify-center my-6">
          <div className="bg-white/5 border border-white/10 px-6 py-3 rounded-full backdrop-blur-sm shadow-lg text-center max-w-xs">
            <p className="text-xs text-pink-soft/80 font-bold tracking-widest uppercase mb-1">Icebreaker</p>
            <p className="text-white text-sm">"Are you actually planning an outfit or deciding on the day?"</p>
          </div>
        </div>

        {messages.map((msg, idx) => {
           // Basic logic to determine if it's "me" or "them". 
           // In Dev bypass, if userId isn't fully set, we just alternate or check ID.
           const isMe = userId ? msg.sender_id === userId : (idx % 2 === 0); 
           
           return (
             <div key={msg.id} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
               <div className={`max-w-[75%] p-4 rounded-2xl ${
                 isMe 
                   ? 'bg-gradient-to-br from-pink-primary to-burgundy text-white rounded-br-sm shadow-[0_5px_15px_rgba(224,53,102,0.4)]' 
                   : 'bg-white/10 text-white rounded-bl-sm border border-white/10 backdrop-blur-md'
               }`}>
                 <p className="text-sm">{msg.content}</p>
               </div>
             </div>
           )
        })}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 p-4 bg-rose-dark/90 backdrop-blur-md border-t border-white/10">
        <form onSubmit={sendMessage} className="flex gap-2 max-w-md mx-auto">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 bg-black/30 border border-white/10 rounded-full px-6 py-3 text-white focus:outline-none focus:border-pink-primary/50 text-sm transition-colors"
          />
          <button 
            type="submit"
            disabled={!newMessage.trim()}
            className="w-12 h-12 rounded-full button-3d flex items-center justify-center text-white disabled:opacity-50"
          >
            <svg className="w-5 h-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
      </div>

    </div>
  )
}
