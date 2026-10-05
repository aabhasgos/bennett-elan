import re

with open('frontend/src/app/discover/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<div className=\"grid grid-cols-3 gap-2\">.*?</div\>\n                  \)\)}\n                </div>'
replacement = '''<div className=\"grid grid-cols-2 gap-4\">\n                  {(profile.photo_urls || []).slice(1, 3).map((url: string, i: number) => (\n                     <div key={i} className=\"aspect-square bg-white/5 rounded-xl border border-white/10 overflow-hidden shadow-lg\">\n                        <img src={url} alt=\"Photo\" className=\"w-full h-full object-cover hover:scale-105 transition-transform duration-500\" />\n                     </div>\n                  ))}\n                </div>'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
if new_content != content:
    with open('frontend/src/app/discover/page.tsx', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Replaced')
else:
    print('No match')