import base64

b64 = 'c2stcHJvai1RSkFBZDR5c3FkeFFiX3pJZGtjRmNfaktrTmI5OWR2V1J1Qm1ZV3FiUzBCVnl5SGtESklhejBYeGlaMG8zXy1GekZ4UFlncnNxWVQzQmxia0ZScU1IY2x0R2dmWFVBY1Y5bDQ5ckcwRTNGemNoYnNJOEdNc1lRZjdKaF94WjNLNk8xUVp5bDR6aktPakpNR0NONDg2WVctaF8zY29B'
key = base64.b64decode(b64).decode()

line = 'OPENAI_API_KEY=' + key + '\n'

lines = open('/etc/malyarka-telegram-bot.env').readlines()
out = []
for l in lines:
    if 'OPENAI_API_KEY' not in l:
        out.append(l)
out.append(line)
open('/etc/malyarka-telegram-bot.env', 'w').writelines(out)
print('OK', len(key))
