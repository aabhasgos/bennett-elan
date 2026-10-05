with open('frontend/src/app/matches/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("headers: { 'Authorization': Bearer  }", "headers: { 'Authorization': \Bearer \\ }")
content = content.replace("\", "\\\")

with open('frontend/src/app/matches/page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed backticks')