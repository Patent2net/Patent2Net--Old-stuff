# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 16:29:11 2015

@author: Celso

Objective: General funcions to create a mindmap file

"""
#import pickle

listdesc3 = []
listdesc4 = []
listdesc7 = []
listdesc11 = []

def CalcSizeIpc1(ipcName, ipcList):
    ipc1total = float(len(ipcList['brevets']))
    ipc1count = float(0)
    ipc1weight = float(0)
    for i in ipcList['brevets']:
#        if type(i['IPCR1']) == list:
            ipc1count = ipc1count + i['IPCR1'].count(ipcName)
    ipc1weight = (ipc1count / ipc1total) * 100
    if ipc1weight > 50:
        ntsize = '16'
    elif ipc1weight > 25:
        ntsize = '14'
    elif ipc1weight > 15:
        ntsize = '12'
    elif ipc1weight >= 10:
        ntsize = '10'
    else:
      ntsize = '8'
  
    return ntsize, str(int(ipc1count))
# End CalcSizeIpc1 

def CalcSizeIpc3(ipcName, ipcList, ipc1total):
    ipc1total = float(ipc1total)
    ipc3count = float(0)
    ipc3weight = float(0)
    for i in ipcList['brevets']:
#        if type(i['IPCR1']) == list:
            ipc3count = ipc3count + i['IPCR3'].count(ipcName)
    ipc3weight = (ipc3count / ipc1total) * 100
    if ipc3weight > 50:
        ntsize = '12'
    elif ipc3weight > 25:
        ntsize = '10'
    elif ipc3weight > 15:
        ntsize = '8'
    elif ipc3weight >= 10:
        ntsize = '8'
    else:
      ntsize = '8'
  
    return ntsize, str(int(ipc3count))
# End CalcSizeIpc3 

def CalcSizeIpc4(ipcName, ipcList, ipc3total):
    ipc3total = float(ipc3total)
    ipc4count = float(0)
    ipc4weight = float(0)
    for i in ipcList['brevets']:
#        if type(i['IPCR1']) == list:
            ipc4count = ipc4count + i['IPCR4'].count(ipcName)
    ipc4weight = (ipc4count / ipc3total) * 100
    if ipc4weight > 50:
        ntsize = '12'
    elif ipc4weight > 25:
        ntsize = '10'
    elif ipc4weight > 15:
        ntsize = '8'
    elif ipc4weight >= 10:
        ntsize = '8'
    else:
      ntsize = '8'
  
    return ntsize, str(int(ipc4count))
# End CalcSizeIpc4 

def CalcSizeIpc7(ipcName, ipcList, ipc4total):
    ipc4total = float(ipc4total)
    ipc7count = float(0)
    ipc7weight = float(0)
    for i in ipcList['brevets']:
#        if type(i['IPCR1']) == list:
            ipc7count = ipc7count + i['IPCR7'].count(ipcName)
    ipc7weight = (ipc7count / ipc4total) * 100
    if ipc7weight > 50:
        ntsize = '12'
    elif ipc7weight > 25:
        ntsize = '10'
    elif ipc7weight > 15:
        ntsize = '8'
    elif ipc7weight >= 10:
        ntsize = '8'
    else:
      ntsize = '8'
  
    return ntsize, str(int(ipc7count))
# End CalcSizeIpc7 

def CalcSizeIpc11(ipcName, ipcList, ipc7total):
    ipc7total = float(ipc7total)
    ipc11count = float(0)
    ipc11weight = float(0)
    for i in ipcList['brevets']:
#        if type(i['IPCR1']) == list:
            ipc11count = ipc11count + i['IPCR11'].count(ipcName)
    ipc11weight = (ipc11count / ipc7total) * 100
    if ipc11weight > 50:
        ntsize = '12'
    elif ipc11weight > 25:
        ntsize = '10'
    elif ipc11weight > 15:
        ntsize = '8'
    elif ipc11weight >= 10:
        ntsize = '8'
    else:
      ntsize = '8'
  
    return ntsize, str(int(ipc11count))
# End CalcSizeIpc11 

def LoadDescs():

    global listdesc3
    global listdesc4
    global listdesc7
    global listdesc11

    with open (".//extensions//IPC-Ressources//IPC_3.txt","r") as fidesc:
        listdesc3 = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//IPC_4.txt","r") as fidesc:
        listdesc4 = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//IPC_8.txt","r") as fidesc:
        listdesc7 = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//IPC_11.txt","r") as fidesc:
        listdesc11 = fidesc.readlines()    

# end LoadDescs
 
def nodecolor(thiscolor):
    if thiscolor == '#ff0000':
        return '#CCFFFF'
    if thiscolor == '#CCFFFF':
        return '#CCFF99'
    if thiscolor == '#CCFF99':
        return '#FFFF99'
    if thiscolor == '#FFFF99':
        return '#FF9966'
    if thiscolor == '#FF9966':
        return '#FF6666'
    if thiscolor == '#FF6666':
        return '#FFCC00'
    if thiscolor == '#FFCC00':
        return '#33FF33'
    if thiscolor == '#33FF33':
        return '#33FFCC'
    if thiscolor == '#33FFCC':
        return '#ff0000'
# end nodecolor        

def Ipc1Text(ipc1):
    if ipc1 == 'A':
        return 'A: Human necessities'
    elif ipc1 == 'B':
        return 'B: Performing operations; Trasnsporting'
    elif ipc1 == 'C':
        return 'C: Chemistry; Metallurgy'
    elif ipc1 == 'D':
        return 'D: Testiles; Paper'
    elif ipc1 == 'E':
        return 'E:  Fixed constructions'
    elif ipc1 == 'F':
        return 'F: Mechanical engineering; Lighting; Heating; Weapons; Blasting'
    elif ipc1 == 'G':
        return 'G: Physics'
    elif ipc1 == 'H':
        return 'H:  Electricity'
# end Ipc1Text
        
def Ipc3Text(ipc3):

    global listdesc3
    for lines in listdesc3:
        try:
            if lines.count(ipc3)>0:
                return lines
        except:
            pass
    return ipc3  
          
# end Ipc3Text
    
def Ipc4Text(ipc4):

    global listdesc4
    for lines in listdesc4:
        try:
            if lines.count(ipc4)>0:
                return lines
        except:
            pass
    return ipc4            
    
# end Ipc4Text

def Ipc7Text(ipc7):

    global listdesc7
    for lines in listdesc7:
        try:
            if lines.count(ipc7)>0:
                return lines
        except:
            pass

    return ipc7            
    
def Ipc11Text(ipc11):

    global listdesc11
    for lines in listdesc11:
        try:
            if lines.count(ipc11)>0:
                return lines
        except:
            pass

    return ipc11            

# end Ipc7Text
