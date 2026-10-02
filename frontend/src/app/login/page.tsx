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


  const handleGoogleLogin = async () => {
    try {
      setLoading(true)
      setError(null)
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: window.location.origin + '/onboarding'
        }
      })
      if (error) throw error
    } catch (err: any) {
      setError(err.message)
      setLoading(false)
    }
  }

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
            
            <div className="relative py-2">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-white/10"></div>
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="bg-rose-dark px-2 text-white/50">OR</span>
              </div>
            </div>

            <button 
              type="button" 
              onClick={handleGoogleLogin}
              disabled={loading}
              className="w-full bg-white/5 border border-white/10 hover:bg-white/10 text-white font-bold py-4 rounded-xl disabled:opacity-50 transition-colors flex items-center justify-center gap-3"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Continue with Google
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
