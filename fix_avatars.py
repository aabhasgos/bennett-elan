import re

with open('frontend/src/app/matches/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

old_avatar = '''                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-pink-primary to-burgundy p-0.5">
                    <div className="w-full h-full rounded-full bg-rose-dark flex items-center justify-center border-2 border-transparent group-hover:border-white/20 transition-all">
                       <span className="text-2xl font-serif text-pink-soft font-bold">
                         {match.profile.first_name[0]}
                       </span>
                    </div>
                  </div>'''

new_avatar = '''                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-pink-primary to-burgundy p-0.5 shrink-0">
                    <div className="w-full h-full rounded-full bg-rose-dark flex items-center justify-center border-2 border-transparent group-hover:border-white/20 transition-all overflow-hidden">
                       {match.profile.photo_urls && match.profile.photo_urls.length > 0 ? (
                         <img src={match.profile.photo_urls[0]} alt={match.profile.first_name} className="w-full h-full object-cover" />
                       ) : (
                         <span className="text-2xl font-serif text-pink-soft font-bold">
                           {match.profile.first_name[0]}
                         </span>
                       )}
                    </div>
                  </div>'''

content = content.replace(old_avatar, new_avatar)

with open('frontend/src/app/matches/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)