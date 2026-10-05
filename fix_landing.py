import re

with open('frontend/src/app/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Enter with Bennett Email', 'Enter with Google')

with open('frontend/src/app/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
