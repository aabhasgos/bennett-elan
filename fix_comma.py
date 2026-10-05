lines = []
with open('frontend/src/app/matches/page.tsx', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'Authorization' in line and 'Bearer' in line and i == 66:
            line = '          \'Authorization\': `Bearer ${session.access_token}`\n        },\n'
        lines.append(line)
with open('frontend/src/app/matches/page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
