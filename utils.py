RESERVED:list = ['root', 'pi', 'epicX', 'dni9', 'sujoy', 'suvrojit'] #exclude these names while processing usernames

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



        
        


        
        



