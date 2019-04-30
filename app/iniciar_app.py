import platform
from subprocess import Popen


if platform.system() == 'Windows':
    print('Plataforma Windows')
    processo = Popen('c:/nbackup/iniciar_windows.bat')
else:
    print('Plataforma Linux')
    #processo = Popen('python3 c:/nbackup/app.py')
