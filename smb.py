from pathlib import Path
import samba.utils as utils
from samba.smbhost import Host
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
writeable=Yes
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
        self.Hosts:Host = []
        self.loadConfigs()



    def loadConfigs(self):
        lines = utils.getLines(self.configFile.read_text())
        hostLine = utils.getConfigs(lines)

        for item in hostLine:
            self.Hosts.append(Host(configLines = item))


    def dispHostLists(self):
        print('List of Hosts\n-------------')
        for item in self.Hosts:
            print(f'{item.config.get("name")}\t[{item.config.get("path")}]')

    
    def pushIntoConf(self):
        RAW = self.configFile.read_text()

        pos1 = RAW.find('###SMBNAS###') + 14
        pos2 = RAW.rfind('###/SMBNAS###')

        preRAW = RAW[0 : pos1]
        postRAW = '\n' + RAW[pos2 : ]

        HOST_RAW = ''

        for item in self.Hosts:
            HOST_RAW += item.getRAW()

        self.configFile.write_text(preRAW + HOST_RAW + postRAW)

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
            self.CRITICAL_CMD.append(f'mkdir -p {self.Host.getConfigs("path")}')
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



    def addValidUser(self, hostName:str, userName:str):
        for item in self.Hosts:
            if hostName == item.config.get('name'):
                item.addValidUser(userName)
                return

        print('Host Name not found ...')

    
    def removeValidUser(self, hostName:str, userName:str):
        for item in self.Hosts:
            if hostName == item.config.get('name'):
                item.removeValidUser(userName)
                return

        print('Host Name not found ...')

        

            

    #SYSTEM Specific functions

    @staticmethod
    def addUser(self, userName):
        if utils.isUserName(userName) == False:
            return False

        exitCode = os.system(f'useradd {userName}')

        if exitCode == 0:
            print(f'Operation Successful  [{userName}] Added / Modified')
            return True
        else:
            print(f'Error Ocurred [{exitCode}]')
            return False

    @staticmethod
    def removeUser(self, userName):
        if utils.isUserName(userName) == False:
            return False

        exitCode = os.system(f'userdel {userName}')

        if exitCode == 0:
            print(f'Operation Successful  [{userName}] Added / Modified')
            return True
        else:
            print(f'Error Ocurred [{exitCode}]')
            return False
    


    @staticmethod
    def add_SMBUser(self, userName, password):
        exitCode = os.system(f'echo "{password}\n{password}" | sudo smbpasswd -s -a {userName}')

        if exitCode == 0:
            print(f'Operation Successful  [{userName}] Added / Modified')
            return True
        else:
            print(f'Error Ocurred [{exitCode}]')
            return False


    @staticmethod
    def remove_SMBUser(self, userName):
        exitCode = os.system(f'sudo smbpasswd -s -a {userName}')

        if exitCode == 0:
            print(f'{userName} Removed')
            return True
        else:
            print(f'Error Ocurred [{exitCode}]')
            return False

    @staticmethod
    def enable_SMBUser(self, userName):
        exitCode = os.system(f'sudo smbpasswd -s -e {userName}')

        if exitCode == 0:
            return True
        else:
            print(f'Error Ocurred while Enabling User [{exitCode}]')
            return False

    @staticmethod
    def disable_SMBUser(self, userName):
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

            




        
        
        

    


#sm = SMB('./etc/samba/smb.conf')

'''sm.createNewHost(Host(data = {
    "name" : "Vodai",
    "path" : "./Botai",
    "writeable" : "Why Not",
    "create mask" : "0777",
    "directory mask" : "0777",
    "public" : "Private",
    "valid users" : ['Bot','Vodai','Petrol_Swapon'],
}))'''


