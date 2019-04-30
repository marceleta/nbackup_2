import platform
import subprocess

if platform.system() == 'Windows':
    comando = ['python','c:/nbackup/app/comando_desligar_app.py']
else:
    comando = ['python3','/home/marcelo/python/nbackup_2/app/comando_desligar_app.py']

processo = subprocess.call(comando)
