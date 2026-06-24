import os, json, urllib.request, base64

_API_KEY_B64 = 'c2stcHJvai1RSkFBZDR5c3FkeFFiX3pJZGtjRmNfaktrTmI5OWR2V1J1Qm1ZV3FiUzBCVnl5SGtESklhejBYeGlaMG8zXy1GekZ4UFlncnNxWVQzQmxia0ZKcU1IY2x0R2dmWFVBY1Y5bDQ5ckcwRTNGemNoYnNJOEdNc1lRZjdKaF94WjNLNk8xUVp5bDR6aktPakpNR040ODZZVy1oXzNjb0E'

def _get_key():
    return base64.b64decode(_API_KEY_B64).decode()

def recognize_order_photo(photo_bytes: bytes) -> str:
    api_key = _get_key()
    img_b64 = base64.b64encode(photo_bytes).decode()
    prompt = 'Extract dimensions and quantities from this order photo. Answer in Russian, only data.'
    body = json.dumps({
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': prompt},
            {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + img_b64}},
        ]}],
        'max_tokens': 300,
    }).encode()
    req = urllib.request.Request(
        'https://api.openai.com/v1/chat/completions',
        data=body,
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())['choices'][0]['message']['content']
    except Exception as e:
        return f'Vision error: {e}'
