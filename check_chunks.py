import urllib.request, re
req = urllib.request.Request('https://bennett-elan-6o8stptqe-aabhasgos-projects.vercel.app/onboarding', headers={'User-Agent': 'Mozilla'})
html = urllib.request.urlopen(req).read().decode('utf-8')
for js in set(re.findall(r'src=\"(/_next/static/chunks/app/onboarding/page-[a-f0-9]+\.js)\"', html)):
    print(js)
    js_url = 'https://bennett-elan-6o8stptqe-aabhasgos-projects.vercel.app' + js
    js_content = urllib.request.urlopen(urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla'})).read().decode('utf-8')
    print('Found localhost:' + str('127.0.0.1:8000' in js_content))
    print('Found onrender:' + str('onrender' in js_content))
