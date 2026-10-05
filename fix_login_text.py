import re

with open('frontend/src/app/login/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_text = '''        <div className="space-y-6">
          <p className="text-sm text-center text-white/70 mb-4 font-medium">Please sign in with your Google account to continue.</p>
          
          <button 
            type="button" 
            onClick={handleGoogleLogin}'''

new_text = '''        <div className="space-y-6">
          <p className="text-sm text-center text-white/70 mb-4 font-medium">Welcome! Please sign in to continue.</p>
          
          <button 
            type="button" 
            onClick={handleGoogleLogin}'''

content = content.replace(old_text, new_text)

old_bottom = '''          </button>
        </div>
      </div>
    </div>
  )
}'''

new_bottom = '''          </button>
          
          <p className="text-center text-xs text-white/40 mt-6 px-2">
            By continuing, you agree to our <a href="#" className="underline hover:text-white/80">Terms of Service</a> and <a href="#" className="underline hover:text-white/80">Privacy Policy</a>.
          </p>
        </div>
      </div>
    </div>
  )
}'''

content = content.replace(old_bottom, new_bottom)

with open('frontend/src/app/login/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
