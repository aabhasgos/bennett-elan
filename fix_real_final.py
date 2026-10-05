lines = []
with open('frontend/src/app/matches/page.tsx', 'r', encoding='utf-8') as f:
    for line in f:
        if 'matchesRes = await fetch' in line:
            line = '      const matchesRes = await fetch(`${API_URL}/matches`, {\n'
        elif 'likesRes = await fetch' in line:
            line = '      const likesRes = await fetch(`${API_URL}/likes`, {\n'
        elif 'res = await fetch' in line and 'swipe' in line:
            line = '      const res = await fetch(`${API_URL}/swipe`, {\n'
        elif 'Authorization' in line and 'Bearer' in line:
            if 'headers:' in line:
                line = '        headers: { \'Authorization\': `Bearer ${session.access_token}` }\n'
            else:
                line = '          \'Authorization\': `Bearer ${session.access_token}`\n'
        lines.append(line)
with open('frontend/src/app/matches/page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
