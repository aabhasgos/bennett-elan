with open('frontend/src/app/profile/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("router.push('/onboarding')", "router.push('/onboarding?edit=true')")

with open('frontend/src/app/profile/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
