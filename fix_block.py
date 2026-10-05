lines = []
with open('frontend/src/app/matches/page.tsx', 'r', encoding='utf-8') as f:
    for line in f:
        lines.append(line)

new_lines = []
skip = False
for i, line in enumerate(lines):
    if 'const res = await fetch(`${API_URL}/swipe`, {' in line:
        new_lines.append(line)
        new_lines.append("        method: 'POST',\n")
        new_lines.append("        headers: {\n")
        new_lines.append("          'Content-Type': 'application/json',\n")
        new_lines.append("          'Authorization': `Bearer ${session.access_token}`\n")
        new_lines.append("        },\n")
        new_lines.append("        body: JSON.stringify({\n")
        new_lines.append("          swipee_id: currentProfile.id,\n")
        new_lines.append("          action: action\n")
        new_lines.append("        })\n")
        new_lines.append("      })\n")
        skip = True
    elif skip:
        if '      if (res.ok) {' in line:
            new_lines.append(line)
            skip = False
    else:
        new_lines.append(line)

with open('frontend/src/app/matches/page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
