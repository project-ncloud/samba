from pathlib import Path
import samba.utils as utils
from samba.smbhost import Host
from serviceHandler import *
import os

'''
Methods,

addSMBUser [UserName, Pass]
removeUserFromSMB [UserName, Pass]
changePass [UserName, Pass]
RestartSMB service [special KEY]
Stop SMB service [special KEY]
Start SMB service [special KEY]

createNewHost [special KEY, CONFIG struct]
RemoveHost [special KEY]
ChangeHostName [special KEY, Name]
ChangeHostPath [special KEY, Name]

add valid User into specific host
remove valid user from specific host
changeHostConfig [special KEY, HostName, configVar, configVal]

[pimylifeupshare]
path = /home/pi/shared
writable=Yes
create mask=0777
directory mask=0777
public=no

'''
#sudo smbpasswd -a pi
#sudo systemctl restart smbd
class SMB:
    CRITICAL_CMD:list = [] #for pending critical command until final push

    def __init__(self, conf:str):
        self.configFile = Path(conf)
        self.normalizeConfig()
        self.Hosts:Host = []
        self.loadConfigs()


    def normalizeConfig(self):
        lines = utils.getLines(self.configFile.read_text())
        normalized:bool = False
        for line in lines:
            if "###SMBNAS###" in line:
                normalized = True
                break
        
        if not normalized:
            lines.append("\n###SMBNAS###\n\n")
            lines.append("###/SMBNAS###\n")

            STR:str = ""
            for line in lines:
                STR += line + "\n"

            self.configFile.write_text(STR)


    def loadConfigs(self):
        self.Hosts.clear()
        lines = utils.getLines(self.configFile.read_text())
        hostLine = utils.getConfigs(lines)

        for item in hostLine:
            self.Hosts.append(Host(configLines = item))


    
    def forceUser(self, mainUser):
        for host in self.Hosts:
            host.set_value("force user", mainUser)
        




    def dispHostLists(self):
        print('List of Hosts\n-------------')
        for item in self.Hosts:
            print(f'{item.config.get("name")}\t[{item.config.get("path")}]')

    
    def pushIntoConf(self):
        RAW = self.configFile.read_text()

        pos1 = RAW.find('###SMBNAS###') + 14
        pos2 = RAW.rfind('###/SMBNAS###')

        preRAW = RAW[0 : pos1]
        postRAW = RAW[pos2 : ]

        HOST_RAW = ''

        for item in self.Hosts:
            HOST_RAW += item.getRAW()

        #self.configFile.write_text(preRAW + HOST_RAW + postRAW)
        print(f'Pushing config into {self.configFile.__str__()}')
        print(os.system(f'sudo cat > {self.configFile.__str__().strip()} << EOF\n{preRAW + HOST_RAW + postRAW}EOF'))

        for item in self.CRITICAL_CMD:
            os.system(item)

        self.CRITICAL_CMD.clear()


    def createNewHost(self, host:Host):
        hostName = host.config.get('name')
        isHostExists = False
        for item in self.Hosts:
            if hostName == item.get('name'):
                isHostExists = True
                break

        if isHostExists == True:
            print(f'{hostName} Already Exists')
        else:
            self.CRITICAL_CMD.append(f'mkdir -p {host.get("path")}')
            self.CRITICAL_CMD.append(f'chown {getCurrentUser()} {host.config.get("path")}')
            self.Hosts.append(host)
            return True

        return False



    def removeHost(self, hostName:str, removeData = False):
        for item in self.Hosts:
            if hostName == item.config.get('name'):
                print(f'{hostName} removed')
                if removeData == True:
                    self.CRITICAL_CMD.append(f'rm -rf {item.config.get("path")}')
                self.Hosts.remove(item)
                return True

        print(f'{hostName} not found')
        return False


    def updateHost(self, name = None, path = None, writable = None, create_mask = None, directory_mask = None, public = None, wipeData = False, hostname = None):
        hostFound = False
        for host in self.Hosts:
            if host.get('name') == hostname:
                host.changeConfig(name = name, path = path, writable = writable, create_mask = create_mask, directory_mask = directory_mask, public = public)
                
                if host.get('path') != host.currentPath:
                    if wipeData == True:
                        self.CRITICAL_CMD.append(f'sudo rm -rf {host.currentPath}')

                    self.CRITICAL_CMD.append(f'sudo mkdir -p {host.get("path")}')
                    self.CRITICAL_CMD.append(f'chown {getCurrentUser()} {host.config.get("path")}')
                hostFound = True
                break

        return hostFound



    def addValidUser(self, hostName:str, userName:str):
        for item in self.Hosts:
            if hostName == item.config.get('name'):
                return item.addValidUser(userName)

        print('Host Name not found ...')
        return False

    
    def removeValidUser(self, hostName:str, userName:str):
        for item in self.Hosts:
            if hostName == item.config.get('name'):
                return item.removeValidUser(userName)

        print('Host Name not found ...')
        return False
        

            

    #SYSTEM Specific functions

    @staticmethod
    def addUser(userName):
        if utils.isUserName(userName) == False:
            return False

        exitCode = os.system(f'sudo useradd {userName}')

        if exitCode == 0:
            print(f'Operation Successful  [{userName}] Added / Modified')
        
        return True

    @staticmethod
    def removeUser(userName):
        if utils.isUserName(userName) == False:
            return False

        exitCode = os.system(f'sudo userdel {userName}')

        if exitCode == 0:
            print(f'Operation Successful  [{userName}] Added / Modified')
            
            
        return True
    


    @staticmethod
    def add_SMBUser(userName, password):
        exitCode = os.system(f'echo "{password}\n{password}" | sudo smbpasswd -s -a {userName}')

        if exitCode == 0:
            print(f'Operation Successful  [{userName}] Added / Modified')
            return True
        else:
            print(f'Error Ocurred [{exitCode}]')
            return False


    @staticmethod
    def remove_SMBUser(userName):
        exitCode = os.system(f'sudo smbpasswd -s -a {userName}')

        if exitCode == 0:
            print(f'{userName} Removed')
            return True
        else:
            print(f'Error Ocurred [{exitCode}]')
            return False

    @staticmethod
    def enable_SMBUser(userName):
        exitCode = os.system(f'sudo smbpasswd -s -e {userName}')

        if exitCode == 0:
            return True
        else:
            print(f'Error Ocurred while Enabling User [{exitCode}]')
            return False

    @staticmethod
    def disable_SMBUser(userName):
        exitCode = os.system(f'sudo smbpasswd -s -d {userName}')

        if exitCode == 0:
            return True
        else:
            print(f'Error Ocurred while Disabling User [{exitCode}]')
            return False


    @staticmethod
    def startSMBD():
        exitCode = os.system('sudo systemctl start smbd')
        if exitCode == 0:
            print('smbd started\t[SAMBA]')
            return True
        else:
            print(f'Error occurred while starting smbd service\t[{exitCode}]')
            return False


    
    @staticmethod
    def restartSMBD():
        exitCode = os.system('sudo systemctl restart smbd')
        if exitCode == 0:
            print('smbd restarted\t[SAMBA]')
            return True
        else:
            print(f'Error occurred while restarting smbd service\t[{exitCode}]')
            return False

    
    @staticmethod
    def stopSMBD():
        exitCode = os.system('sudo systemctl stop smbd')
        if exitCode == 0:
            print('smbd stopped\t[SAMBA]')
            return True
        else:
            print(f'Error occurred while stopping smbd service\t[{exitCode}]')
            return False



    @staticmethod
    def reloadSMBD():
        exitCode = os.system('sudo smbcontrol all reload-config')
        if exitCode == 0:
            print('smbd configuration reloaded\t[SAMBA]')
            return True
        else:
            print(f'Error occurred while reloading SAMBA\t[{exitCode}]')
            return False
            




        
        
        

    


#sm = SMB('./etc/samba/smb.conf')

'''sm.createNewHost(Host(data = {
    "name" : "Vodai",
    "path" : "./Botai",
    "writable" : "Why Not",
    "create mask" : "0777",
    "directory mask" : "0777",
    "public" : "Private",
    "valid users" : ['Bot','Vodai','Petrol_Swapon'],
}))'''


