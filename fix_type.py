import re

with open('frontend/src/app/onboarding/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('profilePrompts.forEach(pp => {', 'profilePrompts.forEach((pp: any) => {')

with open('frontend/src/app/onboarding/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
