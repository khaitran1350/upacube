import os
p = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'upacube.log')
print('path=', p)
if os.path.exists(p):
    with open(p, 'r', encoding='utf-8') as f:
        data = f.read()
    print('len=', len(data))
    print('last_line:', data.splitlines()[-1] if data.splitlines() else '')
else:
    print('no log file found')

