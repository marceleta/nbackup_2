from configuracao.config import Configuracao

class Ftp():

    OS_LINUX = 'Linux'
    OS_WINDOWS = 'Windows'

    def __init__(self):
        config_server = Configuracao().get_server_config()
        self._os = Configuracao.os_system()
        self.config = config_server.config_ftp()


    def iniciar(self):

        if self._os == self.OS_LINUX:
            import os
            str_comando = "service "+self.config.servico+" start"
            os.system(str_comando)
        elif self._os == self.OS_WINDOWS:
            import win32serviceutil
            import win32service

            status = win32serviceutil.QueryServiceStatus(self.config.servico, None)
            if status[1] != win32service.SERVICE_RUNNING:
                pass
#                win32serviceutil.StartService(self.config.servico)

    
    def parar(self):

        if self._os == self.OS_LINUX:
            import os
            str_comando = "service "+self.config.service+" stop"
            os.system(str_comando)

        elif self._os == self.OS_WINDOWS:
            import win32service
            import win32serviceutil
            
            status = win32serviceutil.QueryServiceStatus(self.config.servico, None)
            if status[1] != win32service.SERVICE_STOPPED:
                pass
#                win32serviceutil.StopService(self.config.servico)

