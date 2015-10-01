# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:34:15 2015

@author: Celso

Objective: Crate a FreePlane (mindmap) file
"""
import pickle
from P2N_FreePlaneLib import LoadDescs, nodecolor, Ipc1Text, CalcSizeIpc1
from P2N_FreePlaneLib import Ipc3Text, CalcSizeIpc3, Ipc4Text,CalcSizeIpc4

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
        BrevetsTotal = str(len(DataBrevets1['brevets']))
except:
    print "Error: there are no data to generate de FreePlane file"
    Stop = True
# End of Load patent file
#
    
### ugly code to patch classification extraction inconsistency
for bre in DataBrevets1['brevets']:
    try:
        assert isinstance(bre['IPCR1'], list)
    except:
        #print bre['IPCR1']
        bre['IPCR1'] = [bre['IPCR1']]
        if not isinstance(bre['IPCR3'], list):
            bre['IPCR3'] = [bre['IPCR3']]
        if not isinstance(bre['IPCR4'], list):
            bre['IPCR4'] = [bre['IPCR4']]
        if not isinstance(bre['IPCR7'], list):
            bre['IPCR7'] = [bre['IPCR7']]
        if not isinstance(bre['IPCR11'], list):
            bre['IPCR11'] = [bre['IPCR11']]   
    try:
        assert isinstance(bre['classification'], list)
    except:
#        print bre['classification']
        bre['classification'] = [bre['classification']]
    lstIPC1 = [ipc1 for ipc1 in bre['IPCR1']]
    if '' in bre['classification']:
        bre['classification'].remove('')
    lstIPC = [ipc[0] for ipc in bre['classification']]
    for ipc in lstIPC:
        if ipc not in lstIPC1:
            #trying to repair this inconsistency
        # from down to up
            for ipc11 in bre['IPCR11']:
                for car, ipc in [(1, 'IPCR1'), (3, 'IPCR3'), (4, 'IPCR4'), (6, 'IPCR7')]:
                    if ipc11[0:car] not in bre[ipc]:
                        bre[ipc].append(ipc11[0:car].replace('/', ''))
## end of patch                    
#why that much copies????
DataBrevets3 = DataBrevets1
DataBrevets4 = DataBrevets1
DataBrevets7 = DataBrevets1            #print 'inconsistency'
            

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
                nsize, ncount1 = CalcSizeIpc1(nIpc1,DataBrevets1)
                nodetext = Ipc1Text(nIpc1) + " (" + ncount1 + ")"
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
                                nsize, ncount3 = CalcSizeIpc3(nIpc3,DataBrevets3,ncount1)
                                nodetext = Ipc3Text(nIpc3) + " (" + ncount3 + ")"
                                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#F9F4F4" STYLE="bubble" MAX_WIDTH="300">\n''')
                                fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
### BEFORE
                                ListIpc4 = []
                                for m in DataBrevets4['brevets']:
                                    if type(m['IPCR4']) == list:
                                        for n in m['IPCR4']:
                                            if ListIpc4.count(n) == 0 and n !='' and n.count(nIpc3,0,3) == 1:
                # Node level IPC4                               
                                                nIpc4 = n
                                                ListIpc4.append(nIpc4)
                                                nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                                nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                                fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                                fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                                fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                                fictemp.write('''</node> \n''')
                                    else:
                                        if ListIpc4.count(m['IPCR4']) == 0 and m['IPCR4'] != '' and m['IPCR4'].count(nIpc3,0,3) == 1:
                                            nIpc4 = m['IPCR4']
                                            ListIpc4.append(nIpc4)
                                            nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                            nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                            fictemp.write('''</node> \n''')
                # End node level IPC4
### AFTER
                                fictemp.write('''</node> \n''')
                    else:
                        if ListIpc3.count(k['IPCR3']) == 0 and k['IPCR3'] != '' and k['IPCR3'].count(nIpc1,0,1) == 1:
                            nIpc3 = k['IPCR3']
                            ListIpc3.append(nIpc3)
                            nsize, ncount3 = CalcSizeIpc3(nIpc3,DataBrevets3,ncount1)
                            nodetext = Ipc3Text(nIpc3) + " (" + ncount3 + ")"
                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#F9F4F4" STYLE="bubble" MAX_WIDTH="300">\n''')
                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
### BEFORE
                            ListIpc4 = []
                            for m in DataBrevets4['brevets']:
                                if type(m['IPCR4']) == list:
                                    for n in m['IPCR4']:
                                        if ListIpc4.count(n) == 0 and n !='' and n.count(nIpc3,0,3) == 1:
            # Node level IPC4                               
                                            nIpc4 = n
                                            ListIpc4.append(nIpc4)
                                            nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                            nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                            fictemp.write('''</node> \n''')
                                else:
                                    if ListIpc4.count(m['IPCR4']) == 0 and m['IPCR4'] != '' and m['IPCR4'].count(nIpc3,0,3) == 1:
                                        nIpc4 = m['IPCR4']
                                        ListIpc4.append(nIpc4)
                                        nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                        nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                        fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                        fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                        fictemp.write('''</node> \n''')
            # End node level IPC4
### AFTER                            
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
            nsize, ncount1  = CalcSizeIpc1(nIpc1,DataBrevets1)
            nodetext = Ipc1Text(nIpc1) + " (" + ncount1 + ")"
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
                            nsize, ncount3 = CalcSizeIpc3(nIpc3,DataBrevets3,ncount1)
                            nodetext = Ipc3Text(nIpc3) + " (" + ncount3 + ")"
                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#F9F4F4" STYLE="bubble" MAX_WIDTH="300"> \n''')
                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
### BEFORE
                            ListIpc4 = []
                            for m in DataBrevets4['brevets']:
                                if type(m['IPCR4']) == list:
                                    for n in m['IPCR4']:
                                        if ListIpc4.count(n) == 0 and n !='' and n.count(nIpc3,0,3) == 1:
            # Node level IPC4                               
                                            nIpc4 = n
                                            ListIpc4.append(nIpc4)
                                            nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                            nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                            fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                            fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                            fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                            fictemp.write('''</node> \n''')
                                else:
                                    if ListIpc4.count(m['IPCR4']) == 0 and m['IPCR4'] != '' and m['IPCR4'].count(nIpc3,0,3) == 1:
                                        nIpc4 = m['IPCR4']
                                        ListIpc4.append(nIpc4)
                                        nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                        nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                        fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                        fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                        fictemp.write('''</node> \n''')
            # End node level IPC4
### AFTER                            
                            fictemp.write('''</node> \n''')
                else:
                    if ListIpc3.count(i['IPCR3']) == 0 and i['IPCR3'] != '' and i['IPCR3'].count(nIpc1,0,1) == 1:
                        nIpc3 = i['IPCR3']
                        ListIpc3.append(nIpc3)
                        nsize, ncount3 = CalcSizeIpc3(nIpc3,DataBrevets3,ncount1)
                        nodetext = Ipc3Text(nIpc3) + " (" + ncount3 + ")"
                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#F9F4F4" STYLE="bubble" MAX_WIDTH="300"> \n''')
                        fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                        fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
### BEFORE
                        ListIpc4 = []
                        for m in DataBrevets4['brevets']:
                            if type(m['IPCR4']) == list:
                                for n in m['IPCR4']:
                                    if ListIpc4.count(n) == 0 and n !='' and n.count(nIpc3,0,3) == 1:
        # Node level IPC4                               
                                        nIpc4 = n
                                        ListIpc4.append(nIpc4)
                                        nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                        nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                        fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                        fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                        fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                        fictemp.write('''</node> \n''')
                            else:
                                if ListIpc4.count(m['IPCR4']) == 0 and m['IPCR4'] != '' and m['IPCR4'].count(nIpc3,0,3) == 1:
                                    nIpc4 = m['IPCR4']
                                    ListIpc4.append(nIpc4)
                                    nsize, ncount4 = CalcSizeIpc4(nIpc4,DataBrevets4,ncount3)
                                    nodetext = Ipc4Text(nIpc4) + " (" + ncount4 + ")"
                                    fictemp.write('''<node TEXT="'''+ nodetext + '''" POSITION="''' + nodeside + '''" BACKGROUND_COLOR="#FFFFFF" STYLE="bubble" MAX_WIDTH="300">\n''')
                                    fictemp.write('''<font SIZE="'''+ nsize + '''"/> \n''')
                                    fictemp.write('''<edge COLOR="''' + ecolor + '''"/> \n''')
                                    fictemp.write('''</node> \n''')
        # End node level IPC4
### AFTER                            
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




     
    


