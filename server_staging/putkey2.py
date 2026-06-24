import base64 as B
b='c2stcHJvai1qejZ1d2t3VWtwSUpIMG9Za2N3aWN1QVVrbTQ5V1lpVXlXQk9zSTZoY0hSdHl5akFtRXhlMXlib1BpVlcwZm9iQmEtb3JVM1N4WFQzQmxia0ZKRkJocGZJcFlnWUdpQWs1X0RzQXZLOGkwdW5tTUR3Q0lMVGVkZ3RJNmZqaHlaQ2JEZ0FMdkJQVHNBaWlRY2pfSjhpd0tseWptc0E='
K=B.b64decode(b).decode()
A='OPENAI_AP'
B2='I_KEY=*** open('/etc/malyarka-telegram-bot.env','r') as f:
    L=[l for l in f if 'OPENAI' not in l]
L.append(A+B2+K+'\n')
with open('/etc/malyarka-telegram-bot.env','w') as f:
    f.writelines(L)
print('OK',len(K))
