import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import servicemanager
import socket
import time
import logging
from multiprocessing import Process
import os, sys
import subprocess, platform

sys.path.append(os.path.dirname(__name__))

logging.basicConfig(
    filename = 'c:/nbackup/windows/service_log.log',
    level = logging.DEBUG,
    format = '[nbackup] - %(asctime) - %(levelname) - %(message)'
)

class WindowsService(win32serviceutil.ServiceFramework):
    _svc_name = 'Serviço nBackup'
    _svc_display_name_ = 'Servidor nBackup'

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(5)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.setEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        logging.info('Parar serviço')

        self.desligar()

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )
        logging.info('Iniciando serviço')
        self.iniciar()

    def iniciar(self):
        comando = ['python','c:/nbackup/app/app.py']
        subprocess.call(comando)

    def desligar(self):
        comando = ['python', 'c:/nbackup/app/desligar_app.py']
        subprocess.call(comando)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WindowsService)
