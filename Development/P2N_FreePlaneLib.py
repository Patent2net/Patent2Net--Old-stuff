# -*- coding: utf-8 -*-
"""
Created on Sat Sep 05 16:29:11 2015

@author: Celso

Objective: General funcions to create a mindmap file

"""
#import pickle

listdescA = []
listdescB = []
listdescC = []
listdescD = []
listdescE = []
listdescF = []
listdescG = []
listdescH = []

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

def LoadDescs():

    global listdescA
    global listdescB
    global listdescC
    global listdescD
    global listdescE
    global listdescF
    global listdescG
    global listdescH

    with open (".//extensions//IPC-Ressources//EN_ipc_section_A.csv","r") as fidesc:
        listdescA = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//EN_ipc_section_B.csv","r") as fidesc:
        listdescB = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//EN_ipc_section_C.csv","r") as fidesc:
        listdescC = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//EN_ipc_section_D.csv","r") as fidesc:
        listdescD = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//EN_ipc_section_E.csv","r") as fidesc:
        listdescE = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//EN_ipc_section_F.csv","r") as fidesc:
        listdescF = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//EN_ipc_section_G.csv","r") as fidesc:
        listdescG = fidesc.readlines()    
    with open (".//extensions//IPC-Ressources//EN_ipc_section_H.csv","r") as fidesc:
        listdescH = fidesc.readlines()    
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

    global listdescA
    global listdescB
    global listdescC
    global listdescD
    global listdescE
    global listdescF
    global listdescG
    global listdescH
    
    if ipc3.count('A',0,1) == 1:
        for lines in listdescA:
            try:
                if lines.count(ipc3+";")>0:
                    return ipc3+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc3.count('B',0,1) == 1:
        for lines in listdescB:
            try:
                if lines.count(ipc3+";")>0:
                    return  ipc3+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc3.count('C',0,1) == 1:
        for lines in listdescC:
            try:
                if lines.count(ipc3+";")>0:
                    return  ipc3+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc3.count('D',0,1) == 1:
        for lines in listdescD:
            try:
                if lines.count(ipc3+";")>0:
                    return  ipc3+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc3.count('E',0,1) == 1:
        for lines in listdescE:
            try:
                if lines.count(ipc3+";")>0:
                    return  ipc3+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc3.count('F',0,1) == 1:
        for lines in listdescF:
            try:
                if lines.count(ipc3+";")>0:
                    return  ipc3+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc3.count('G',0,1) == 1:
        for lines in listdescG:
            try:
                if lines.count(ipc3+";")>0:
                    return  ipc3+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc3.count('H',0,1) == 1:
        for lines in listdescH:
            try:
                if lines.count(ipc3+";")>0:
                    return  ipc3+": "+lines.split(';')[1].strip()
            except:
                pass

    return ipc3            
# end Ipc3Text
    
def Ipc4Text(ipc4):

    global listdescA
    global listdescB
    global listdescC
    global listdescD
    global listdescE
    global listdescF
    global listdescG
    global listdescH
    
    if ipc4.count('A',0,1) == 1:
        for lines in listdescA:
            try:
                if lines.count(ipc4+";")>0:
                    return ipc4+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc4.count('B',0,1) == 1:
        for lines in listdescB:
            try:
                if lines.count(ipc4+";")>0:
                    return  ipc4+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc4.count('C',0,1) == 1:
        for lines in listdescC:
            try:
                if lines.count(ipc4+";")>0:
                    return  ipc4+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc4.count('D',0,1) == 1:
        for lines in listdescD:
            try:
                if lines.count(ipc4+";")>0:
                    return  ipc4+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc4.count('E',0,1) == 1:
        for lines in listdescE:
            try:
                if lines.count(ipc4+";")>0:
                    return  ipc4+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc4.count('F',0,1) == 1:
        for lines in listdescF:
            try:
                if lines.count(ipc4+";")>0:
                    return  ipc4+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc4.count('G',0,1) == 1:
        for lines in listdescG:
            try:
                if lines.count(ipc4+";")>0:
                    return  ipc4+": "+lines.split(';')[1].strip()
            except:
                pass
    elif ipc4.count('H',0,1) == 1:
        for lines in listdescH:
            try:
                if lines.count(ipc4+";")>0:
                    return  ipc4+": "+lines.split(';')[1].strip()
            except:
                pass

    return ipc4            
# end Ipc4Text

