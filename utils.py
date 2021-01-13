import subprocess
import os
from serviceHandler import getCurrentUser

RESERVED:list = ['root', os.getenv('ADMIN_USER'), getCurrentUser()] #exclude these names while processing usernames

def getLines(RAW):
    return RAW.split('\n')


def getConfigs(lines):
    tmpLines = []
    flag = None
    for line in lines:
        if flag == False:
            break

        if flag == True:
            tmpLines.append(line)

        if "###SMBNAS###" in line:
            flag = True

        if "###/SMBNAS###" in line:
            flag = False

    

    tmpConfigLines = []
    tmp = ""

    for line in tmpLines:
        tmp += line + '\n'
    
    while "#END#" in tmp:
        tmpConfigLines.append(tmp[tmp.find('#START#\n')+8: tmp.find('#END#')])
        tmp = tmp[tmp.find('#END#\n')+6: ]

    
    hostLine = []
    for config in tmpConfigLines:
        hostLine.append(config.split('\n'))

    return hostLine



def parseHost(hosts):
    hostConfig = {
        "name": "HOST",
        "comment" : "SAMPLE COMMENT"
    }



def isUserName(name):
    name = name.strip()

    for keyword in RESERVED:
        if keyword.lower() == name.lower():
            return False

    return False if name == '' else True



def getCurrentUser():
    p =  subprocess.Popen("whoami", stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    return output.decode()
        


        
#To check if all the required data available or not
def isRequiredDataAvailable(data, keys):
    if data == None:
        return None

    length = len(keys)
    operationCounter = 0

    for item in data:
        for key in keys:
            if item.__str__() == key:
                if item != None:
                    operationCounter += 1
                
                break
        
    return True if operationCounter == length else False