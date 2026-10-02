'use client'

import { useState } from 'react'
import { createClient } from '@/utils/supabase/client'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sentOtp, setSentOtp] = useState(false)
  const [otp, setOtp] = useState('')

  const supabase = createClient()
  const router = useRouter()

  const handleSendOtp = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    if (!email) {
      setError("Please enter an email address.")
      return
    }

    setLoading(true)
    const { error: signInError } = await supabase.auth.signInWithOtp({
      email,
      options: {
        shouldCreateUser: true,
      }
    })

    if (signInError) {
      setError(signInError.message)
    } else {
      setSentOtp(true)
    }
    setLoading(false)
  }

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const { error: verifyError } = await supabase.auth.verifyOtp({
      email,
      token: otp,
      type: 'email'
    })

    if (verifyError) {
      setError(verifyError.message)
      setLoading(false)
    } else {
      router.push('/onboarding')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-rose-dark p-4 relative overflow-hidden font-sans">
      
      {/* 3D Background */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-pink-primary/10 rounded-full blur-[100px] pointer-events-none"></div>
      
      <div className="w-full max-w-sm luxury-glass p-8 z-10 relative shadow-[0_15px_40px_rgba(42,10,24,0.6)]">
        
        <div className="text-center mb-8">
          <h1 className="text-3xl font-serif text-white font-bold mb-2">Bennett Élan</h1>
          <p className="text-pink-soft text-xs uppercase tracking-widest font-bold">Verification</p>
        </div>

        {error && (
          <div className="bg-burgundy/50 border border-pink-primary/50 text-pink-soft p-3 rounded-xl text-sm mb-6 text-center backdrop-blur-md">
            {error}
          </div>
        )}

        {!sentOtp ? (
          <form onSubmit={handleSendOtp} className="space-y-6">
            <div>
              <label className="block text-sm text-champagne mb-2 ml-1">Bennett Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="e.g. name@example.com"
                className="w-full bg-black/20 border border-white/10 rounded-xl p-4 text-white focus:border-pink-primary outline-none transition-colors"
                required
              />
            </div>
            <button 
              type="submit" 
              disabled={loading}
              className="w-full button-3d text-white font-bold py-4 rounded-xl disabled:opacity-50"
            >
              {loading ? 'Sending Code...' : 'Send Verification Code'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyOtp} className="space-y-6 animate-in fade-in zoom-in-95 duration-300">
            <div>
              <p className="text-sm text-pink-soft/80 mb-4 text-center">We sent a login code to <br/><span className="text-white font-bold">{email}</span></p>
              <input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="Enter login code"
                className="w-full bg-black/20 border border-white/10 rounded-xl p-4 text-white text-center tracking-[0.5em] focus:border-pink-primary outline-none transition-colors text-xl font-bold"
                required
              />
            </div>
            <button 
              type="submit" 
              disabled={loading}
              className="w-full button-3d text-white font-bold py-4 rounded-xl disabled:opacity-50"
            >
              {loading ? 'Verifying...' : 'Verify & Enter'}
            </button>
            
            <button 
              type="button"
              onClick={() => setSentOtp(false)}
              className="w-full text-center text-xs text-champagne/60 hover:text-white transition-colors mt-4"
            >
              Use a different email
            </button>
          </form>
        )}
      </div>
    </div>
  )
}
