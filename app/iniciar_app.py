import platform
import subprocess


if platform.system() == 'Windows':
    print('Plataforma Windows')
    comando = ['python','c:/nbackup/app/app.py']
else:
    print('Plataforma Linux')
    comando = ['python3','/home/marcelo/python/nbackup_2/app/app.py']


processo = subprocess.call(comando)
print('Status: {}'.format(processo))
