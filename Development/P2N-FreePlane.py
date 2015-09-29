# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:34:15 2015

@author: Celso

Objective: Crate a FreePlane (mindmap) file
"""
import pickle
from P2N_FreePlaneLib import LoadDescs, nodecolor, Ipc1Text, Ipc3Text, CalcSizeIpc1

DataBrevets1 = []
DataBrevets3 = []
DataBrevets4 = []
DataBrevets7 = []

ListIpc1 = []
ListIpc3 = []
ListIpc4 = []
ListIpc7 = []

Stop  = False
nIpc1 = ''
nIpc3 = ''
nIpc4 = ''
nIpc7 = ''

nodeside = 'right'
nodetext = ''
ncolor = '#ff0000'
ecolor = '#0000ff'
nsize = '10'

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
        BrevetsTotal = str(len(DataBrevets1['brevets']))
except:
    print "Error: there are no data to generate de FreePlane file"
    Stop = True
# End of Load patent file

fictemp=open('..//DONNEES//'+rep+'//'+rep+'FP.mm', 'w')

fictemp.write('''<map version="freeplane 1.3.0"> \n''')
fictemp.write('''<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net --> \n''')
fictemp.write('''<node TEXT="Project: ''' + rep + '''" BACKGROUND_COLOR="#FFFF33"> \n''')
#fictemp.write('''<edge STYLE="sharp_bezier" COLOR="#808080" WIDTH="thin"/> \n''')
#fictemp.write('''<icon BUILTIN="info"/> \n''')
fictemp.write('''<hook NAME="MapStyle"> \n''')
fictemp.write('''   <properties show_note_icons="true"/>\n''')
fictemp.write('''</hook> \n''')

# New hook
fictemp.write('''<hook NAME="AutomaticEdgeColor" COUNTER="5"/> \n''')
fictemp.write('''<richcontent TYPE="NOTE"> \n''')
fictemp.write('''<html> \n''')
fictemp.write('''  <head> \n''')
fictemp.write('''  </head> \n''')
fictemp.write('''  <body> \n''')
fictemp.write('''    <p> \n''')
fictemp.write('''      Chave de pesquisa: ''' + requete + ''' \n''')
fictemp.write('''    </p> \n''')
fictemp.write('''    <p> \n''')
fictemp.write('''      Total de patentes encontradas: ''' + BrevetsTotal + ''' \n''')
fictemp.write('''    </p> \n''')
fictemp.write('''  </body> \n''')
fictemp.write('''</html> \n''')
fictemp.write('''</richcontent> \n''')

# New node


for i in DataBrevets1['brevets']:
    if type(i['IPCR1']) == list:
        for j in i['IPCR1']:
            if ListIpc1.count(j) == 0 and j !='':
# Node level IPC1
                nIpc1 = j
                ListIpc1.append(nIpc1)
                if nodeside == 'right':
                    nodeside = 'left'
                else:
                    nodeside = 'right'
                ncolor = nodecolor(ncolor)
                nsize, ncount = CalcSizeIpc1(nIpc1,DataBrevets1)
                nodetext = Ipc1Text(nIpc1) + " (" + ncount + ")"
                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''"  BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" MAX_WIDTH="200"> \n''')
                fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                ListIpc3 = []
                for k in DataBrevets3['brevets']:
                    if type(k['IPCR3']) == list:
                        for l in k['IPCR3']:
                            if ListIpc3.count(l) == 0 and l !='' and l.count(nIpc1,0,1) == 1:
# Node level IPC3                               
                                nIpc3 = l
                                ListIpc3.append(nIpc3)
                                nodetext = Ipc3Text(nIpc3)
                                nsize = '10'
                                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="bubble" MAX_WIDTH="200"> \n''')
                                fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                fictemp.write('''</node> \n''')
                    else:
                        if ListIpc3.count(k['IPCR3']) == 0 and k['IPCR3'] != '' and k['IPCR3'].count(nIpc1,0,1) == 1:
                            nIpc3 = k['IPCR3']
                            ListIpc3.append(nIpc3)
                            nodetext = Ipc3Text(nIpc3)
                            nsize = '10'
                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="bubble" MAX_WIDTH="200"> \n''')
                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                            fictemp.write('''</node> \n''')
# End node level IPC3
                fictemp.write('''</node> \n''')
# End node level IPC1
    else:
        if ListIpc1.count(i['IPCR1']) == 0 and i['IPCR1'] != '':
# Node level IPC1
            nIpc1 = i['IPCR1']
            ListIpc1.append(nIpc1)
            if nodeside == 'right':
                nodeside = 'left'
            else:
                nodeside = 'right'
            ncolor = nodecolor(ncolor)
            nsize, ncount  = CalcSizeIpc1(nIpc1,DataBrevets1)
            nodetext = Ipc1Text(nIpc1) + " (" + ncount + ")"
            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="''' + ncolor + '''" STYLE="bubble" MAX_WIDTH="200"> \n''')
            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
            ListIpc3 = []
            for i in DataBrevets3['brevets']:
                if type(i['IPCR3']) == list:
                    for j in i['IPCR3']:
                        if ListIpc3.count(j) == 0 and j !='' and j.count(nIpc1,0,1) == 1:
# Node level IPC3
                            nIpc3 = j
                            ListIpc3.append(nIpc3)
                            nodetext = Ipc3Text(nIpc3)
                            nsize = '10'
                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="bubble" MAX_WIDTH="200"> \n''')
                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                            fictemp.write('''</node> \n''')
                else:
                    if ListIpc3.count(i['IPCR3']) == 0 and i['IPCR3'] != '' and i['IPCR3'].count(nIpc1,0,1) == 1:
                        nIpc3 = i['IPCR3']
                        ListIpc3.append(nIpc3)
                        nodetext = Ipc3Text(nIpc3)
                        nsize = '10'
                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" STYLE="bubble" MAX_WIDTH="200"> \n''')
                        fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                        fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                        fictemp.write('''</node> \n''')
# End node level IPC3
            fictemp.write('''</node> \n''')
# End node level IPC1

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




     
    


