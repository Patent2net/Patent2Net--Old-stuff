# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:34:15 2015

@author: Celso

Objective: Crate a FreePlane (mindmap) file
"""
import pickle
from P2N_FreePlaneLib import LoadDescs, nodecolor, Ipc1Text, Ipc3Text

DataBrevets1 = []
DataBrevets3 = []
DataBrevets7 = []

ListIpc1 = []
ListIpc3 = []
ListIpc7 = []

Stop  = False
nIpc1 = ''
nIpc3 = ''

nodeside = 'right'
nodetext = ''
ncolor = '#ff0000'
    
# Load the patent file
with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()
rep = ndf
ListPatentPath   = '..//DONNEES//'+rep+'//PatentLists'
ResultPathBiblio = '..//DONNEES//'+rep+'//PatentBiblios'

LoadDescs()

try:
    with open(ResultPathBiblio+'//'+ndf, 'r') as fic:
        DataBrevets1 = pickle.load(fic)
        DataBrevets3 = DataBrevets1
        DataBrevets7 = DataBrevets1
except:
    print "Error: there are no data to generate de FreePlane file"
    Stop = True
# End of Load patent file

fictemp=open('..//DONNEES//'+rep+'//FP'+rep+'.mm', 'w')

fictemp.write('''<map version="freeplane 1.3.0"> \n''')
fictemp.write('''<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net --> \n''')
fictemp.write('''<node TEXT="Project: ''' + rep + '''" > \n''')
#fictemp.write('''<edge STYLE="sharp_bezier" COLOR="#808080" WIDTH="thin"/> \n''')
fictemp.write('''<icon BUILTIN="info"/> \n''')
fictemp.write('''<hook NAME="MapStyle"> \n''')
#fictemp.write('''   <properties show_note_icons="false"/>\n''')
fictemp.write('''</hook> \n''')

# New hook
fictemp.write('''<hook NAME="AutomaticEdgeColor" COUNTER="5"/> \n''')

# New node
for i in DataBrevets1['brevets']:
    if type(i['IPCR1']) == list:
        for j in i['IPCR1']:
            if ListIpc1.count(j) == 0 and j !='':
                nIpc1 = j
                ListIpc1.append(nIpc1)
                if nodeside == 'right':
                    nodeside = 'left'
                else:
                    nodeside = 'right'
                nodetext = Ipc1Text(nIpc1)
                ncolor = nodecolor(ncolor)
                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''"  BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" > \n''')
                fictemp.write('''<edge COLOR="''' + ncolor + '''"/> \n''')
                ListIpc3 = []
                for k in DataBrevets3['brevets']:
                    if type(k['IPCR3']) == list:
                        for l in k['IPCR3']:
                            if ListIpc3.count(l) == 0 and l !='' and l.count(nIpc1,0,1) == 1:
                                nIpc3 = l
                                ListIpc3.append(nIpc3)
                                nodetext = Ipc3Text(nIpc3)
#                                ncolor = nodecolor(ncolor)
                                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="fork" > \n''')
                                fictemp.write('''<edge COLOR="''' + ncolor + '''"/> \n''')
                                fictemp.write('''</node> \n''')
                            # End nodes level 2 - IPC3
                    else:
                        if ListIpc3.count(k['IPCR3']) == 0 and k['IPCR3'] != '' and k['IPCR3'].count(nIpc1,0,1) == 1:
                            nIpc3 = k['IPCR3']
                            ListIpc3.append(nIpc3)
                            nodetext = Ipc3Text(nIpc3)
#                            ncolor = nodecolor(ncolor)
                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="fork" > \n''')
                            fictemp.write('''<edge COLOR="''' + ncolor + '''"/> \n''')
                            fictemp.write('''</node> \n''')
                        # End nodes level 2 - IPC3
                fictemp.write('''</node> \n''')
            # End nodes level 1 - IPC1
    else:
        if ListIpc1.count(i['IPCR1']) == 0 and i['IPCR1'] != '':
            nIpc1 = i['IPCR1']
            ListIpc1.append(nIpc1)
            if nodeside == 'right':
                nodeside = 'left'
            else:
                nodeside = 'right'
            nodetext = Ipc1Text(nIpc1)
            ncolor = nodecolor(ncolor)
            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" > \n''')
            fictemp.write('''<edge COLOR="''' + ncolor + '''"/> \n''')
            ListIpc3 = []
            for i in DataBrevets3['brevets']:
                if type(i['IPCR3']) == list:
                    for j in i['IPCR3']:
                        if ListIpc3.count(j) == 0 and j !='' and j.count(nIpc1,0,1) == 1:
                            nIpc3 = j
                            ListIpc3.append(nIpc3)
                            nodetext = Ipc3Text(nIpc3)
#                                ncolor = nodecolor(ncolor)
                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="fork" > \n''')
                            fictemp.write('''<edge COLOR="''' + ncolor + '''"/> \n''')
                            fictemp.write('''</node> \n''')
                        # End nodes level 2 - IPC3
                else:
                    if ListIpc3.count(i['IPCR3']) == 0 and i['IPCR3'] != '' and i['IPCR3'].count(nIpc1,0,1) == 1:
                        nIpc3 = i['IPCR3']
                        ListIpc3.append(nIpc3)
                        nodetext = Ipc3Text(nIpc3)
#                            ncolor = nodecolor(ncolor)
                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="fork" > \n''')
                        fictemp.write('''<edge COLOR="''' + ncolor + '''"/> \n''')
                        fictemp.write('''</node> \n''')
                    # End nodes level 2 - IPC3
            fictemp.write('''</node> \n''')
        # End nodes level 1 - IPC1


# Close ORIGINAL node
fictemp.write('''</node> \n''')

#Clsoe map
fictemp.write('''</map> \n''')

fictemp.write(''' \n''')
fictemp.write(''' \n''')
fictemp.write(''' \n''')
fictemp.write(''' \n''')
fictemp.write(''' \n''')
fictemp.write(''' \n''')
fictemp.write(''' \n''')

fictemp.close()

print "Mindmap file writen in " + '..//DONNEES//'+rep 




     
    


