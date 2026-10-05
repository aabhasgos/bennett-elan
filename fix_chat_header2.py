import re

with open('frontend/src/app/chat/[id]/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

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

content = re.sub(r'        <div className="flex items-center gap-3">.*?</div>\n        </div>', header_new, content, flags=re.DOTALL)

with open('frontend/src/app/chat/[id]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
