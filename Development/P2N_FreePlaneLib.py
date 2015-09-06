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


def LoadDescs():

    global listdescA
    global listdescB
    global listdescC
    global listdescD
    global listdescE
    global listdescF
    global listdescG
    global listdescH

    with open ("..//EN_ipc_section_A.csv","r") as fidesc:
        listdescA = fidesc.readlines()    
    with open ("..//EN_ipc_section_B.csv","r") as fidesc:
        listdescB = fidesc.readlines()    
    with open ("..//EN_ipc_section_C.csv","r") as fidesc:
        listdescC = fidesc.readlines()    
    with open ("..//EN_ipc_section_D.csv","r") as fidesc:
        listdescD = fidesc.readlines()    
    with open ("..//EN_ipc_section_E.csv","r") as fidesc:
        listdescE = fidesc.readlines()    
    with open ("..//EN_ipc_section_F.csv","r") as fidesc:
        listdescF = fidesc.readlines()    
    with open ("..//EN_ipc_section_G.csv","r") as fidesc:
        listdescG = fidesc.readlines()    
    with open ("..//EN_ipc_section_H.csv","r") as fidesc:
        listdescH = fidesc.readlines()    

 
def nodecolor(thiscolor):
    if thiscolor == '#ff0000':
        return '#00ff00'
    if thiscolor == '#00ff00':
        return '#0000ff'
    if thiscolor == '#0000ff':
        return '#ffff00'
    if thiscolor == '#ffff00':
        return '#00ffff'
    if thiscolor == '#00ffff':
        return '#ff00ff'
    if thiscolor == '#ff00ff':
        return '#888800'
    if thiscolor == '#888800':
        return '#880088'
    if thiscolor == '#880088':
        return '#008888'
    if thiscolor == '#008888':
        return '#ff0000'
# end nodecolor        

def Ipc1Text(ipc1):
    if ipc1 == 'A':
        return 'A: HUMAN NECESSITIES'
    elif ipc1 == 'B':
        return 'B: PERFORMING OPERATIONS; TRANSPORTING'
    elif ipc1 == 'C':
        return 'C: CHEMISTRY; METALLURGY'
    elif ipc1 == 'D':
        return 'D: TEXTILES; PAPER'
    elif ipc1 == 'E':
        return 'E:  FIXED CONSTRUCTIONS'
    elif ipc1 == 'F':
        return 'F: MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING'
    elif ipc1 == 'G':
        return 'G: PHYSICS'
    elif ipc1 == 'H':
        return 'H:  ELECTRICITY'
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
    

