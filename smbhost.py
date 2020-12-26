from samba import utils

'''
Methods,

def __init__(self, configLines = None, data = None)
def get_HostData(self)
def get(self, key)
def set_value(self, key, val)
def changeConfig(self, name = None, path = None, writeable = None, create_mask = None, directory_mask = None, public = None)
def userExists(self, userName)
def addValidUser(self, userName)
def removeValidUser(self, userName)
def dispValidUsers(self)
def getRAW(self)


[pimylifeupshare]
path = /home/pi/shared
writeable=Yes
create mask=0777
directory mask=0777
public=no

'''

class Host:

    def __init__(self, configLines = None, data = None):
        if configLines != None:
            self.config = {
                "name" : "",
                "path" : "",
                "writeable" : "",
                "create mask" : "",
                "directory mask" : "",
                "public" : "No",
                "valid users" : [],
            }
            for line in configLines:
                if '[' in line:
                    self.config.__setitem__("name", line[line.find('[') + 1 : line.find(']')])
                

                if 'path' in line:
                    self.config.__setitem__('path', line[line.find('=') + 1 : ].strip())

                if 'writeable' in line:
                    self.config.__setitem__('writeable', line[line.find('=') + 1 : ].strip())

                if 'create mask' in line:
                    self.config.__setitem__('create mask', line[line.find('=') + 1 : ].strip())

                if 'directory mask' in line:
                    self.config.__setitem__('directory mask', line[line.find('=') + 1 : ].strip())


                if 'public' in line:
                    self.config.__setitem__('public', line[line.find('=') + 1 : ].strip())

                
                if 'valid users' in line:
                    tmp = line[line.find('=') + 1 : ].strip()
                    arr = tmp.split(',')
                    arr2 = []
                    for item in arr:
                        if item.strip() != '': arr2.append(item.strip())
                    
                    self.config.__setitem__('valid users', arr2)

        elif data != None:
            self.config = data

        print('SMB initialized')

    

    def get_HostData(self):
        return self.config

    def get(self, key):
        return self.config.get(key)

    def set_value(self, key, val):
        self.config.__setitem__(key, val)

    
    def changeConfig(self, name = None, path = None, writeable = None, create_mask = None, directory_mask = None, public = None):
        if name != None : self.set_value('name', name)
        if path != None : self.set_value('path', path)
        if writeable != None : self.set_value('writeable', writeable)
        if create_mask != None : self.set_value('create mask', create_mask)
        if directory_mask != None : self.set_value('directory mask', directory_mask)
        if public != None : self.set_value('public', public)



        
        
    def userExists(self, userName):
        for item in self.config.get('valid users'):
            if item == userName:
                return True
            
        return False
        

    
    def addValidUser(self, userName):
        if utils.isUserName(userName) == True:
            userName = userName.strip()
            if self.userExists(userName):
                print('User already exists in this host')
            else:
                x = self.config.get('valid users')
                x.append(userName) 
                self.config.setdefault('valid users', x)
        else:
            print('Invalid User')
            return False
        
        return True

    def removeValidUser(self, userName):
        if utils.isUserName(userName) == True:
            if userName not in self.config.get('valid users'):
                print('User not exists in this host')
            else:
                x = self.config.get('valid users')
                userName = userName.strip()
                for user in x:
                    if userName == user:
                        x.remove(user)
                        break

                self.config.__setitem__('valid users', x)
        else:
            print('Invalid User')
            return False
        
        return True


    def dispValidUsers(self):
        x = self.config.get('valid users')
        print(f'\nValid Users\t[{self.config.get("name")}]\n-------')
        for item in x:
            print(item)


    def getRAW(self):
        x = self.config.get('valid users')
        users = ""
        flag = False
        for item in x:
            if flag == True:
                users += ', '
            users += f'{item}'
            flag = True

        return f'''

#START#
[{self.config.get('name')}]
path = {self.config.get('path')}
writeable = {self.config.get('writeable')}
create mask = {self.config.get('create mask')}
directory mask = {self.config.get('directory mask')}
public = {self.config.get('public')}
valid users = {users}
#END#

'''


                

          


