import re

with open('frontend/src/app/login/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the whole form block and the "OR" divider.
# We'll just replace the content between {!sentOtp ? ( ... ) : ( ... )}
# Actually, the simplest is to replace the entire return block.

new_return = '''  return (
    <div className="min-h-screen flex items-center justify-center bg-rose-dark p-4 relative overflow-hidden font-sans">
      
      {/* 3D Background */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-pink-primary/10 rounded-full blur-[100px] pointer-events-none"></div>
      
      <div className="w-full max-w-sm luxury-glass p-8 z-10 relative shadow-[0_15px_40px_rgba(42,10,24,0.6)]">
        
        <div className="text-center mb-10">
          <h1 className="text-3xl font-serif text-white font-bold mb-2">Bennett Élan</h1>
          <p className="text-pink-soft text-xs uppercase tracking-widest font-bold">Verification</p>
        </div>

        {error && (
          <div className="bg-burgundy/50 border border-pink-primary/50 text-pink-soft p-3 rounded-xl text-sm mb-6 text-center backdrop-blur-md">
            {error}
          </div>
        )}

        <div className="space-y-6">
          <p className="text-sm text-center text-white/70 mb-4 font-medium">Please sign in with your Google account to continue.</p>
          
          <button 
            type="button" 
            onClick={handleGoogleLogin}
            disabled={loading}
            className="w-full bg-white/5 border border-white/10 hover:bg-white/10 text-white font-bold py-5 rounded-xl disabled:opacity-50 transition-colors flex items-center justify-center gap-4 text-lg shadow-lg"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            {loading ? 'Connecting...' : 'Continue with Google'}
          </button>
        </div>
      </div>
    </div>
  )
}
'''

# Find the return ( block and replace the whole thing.
pattern = r'  return \(\n    <div className=\"min-h-screen.*?\n}\n'
new_content = re.sub(pattern, new_return, content, flags=re.DOTALL)

with open('frontend/src/app/login/page.tsx', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated UI')