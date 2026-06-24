import os, json, urllib.request, base64

def _get_key():
    with open('/tmp/openai_key.txt','rb') as f:
        return f.read().strip().decode()

def recognize_order_photo(photo_bytes: bytes):
    k = _get_key()
    img_b64 = base64.b64encode(photo_bytes).decode()
    prompt = 'Extract dimensions and quantities from this order. Answer in Russian, only data.'
    body = json.dumps({'model':'gpt-4o-mini','messages':[{'role':'user','content':[
        {'type':'text','text':prompt},
        {'type':'image_url','image_url':{'url':'data:image/jpeg;base64,'+img_b64}},
    ]}],'max_tokens':300}).encode()
    req = urllib.request.Request('https://api.openai.com/v1/chat/completions',data=body,
        headers={'Authorization':'Bearer '+k,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.loads(r.read())['choices'][0]['message']['content']
