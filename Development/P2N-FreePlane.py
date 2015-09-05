# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:34:15 2015

@author: Celso

Objective: Crate a FreePlane (mindmap) file
"""
import pickle

DataBrevets = []

ListIpc1 = []
ListIpc3 = []
ListIpc7 = []

Stop = False

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

try:
    with open(ResultPathBiblio+'//'+ndf, 'r') as fic:
        DataBrevets= pickle.load(fic)
except:
    print "Error: there are no data to generate de FreePlane file"
    Stop = True
# End of Load patent file


for i in DataBrevets['brevets']:
    if ListIpc1.count(i['IPCR1']) == 0:
        if type(i['IPCR1']) <> list:
            ListIpc1.append(i['IPCR1'])
        print i['IPCR1']
        print type(i['IPCR1'])
#    print DataBrevets['brevets'][i]['IPCR1'][0]


fictemp=open('..//DONNEES//'+rep+'//FP'+rep+'.mm', 'w')

fictemp.write('''<map version="freeplane 1.3.0"> \n''')
fictemp.write('''<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net --> \n''')
fictemp.write('''<node TEXT="''' + rep + '''" > \n''')
fictemp.write('''<icon BUILTIN="clock2"/> \n''')
fictemp.write('''<hook NAME="MapStyle"> \n''')
fictemp.write('''   <properties show_note_icons="true"/>\n''')
fictemp.write('''</hook> \n''')

# New hook
fictemp.write('''<hook NAME="AutomaticEdgeColor" COUNTER="5"/> \n''')

# New node
fictemp.write('''<node TEXT="A: HUMAN NECESSITIES" POSITION="left" > \n''')
fictemp.write('''<edge COLOR="#ff0000"/> \n''')
# New sub-nodes
fictemp.write('''<node TEXT="A01: AGRICULTURE; FORESTRY; ANIMAL HUSBANDRY; HUNTING; TRAPPING; FISHING"/> \n''')
fictemp.write('''<node TEXT="A21: BAKING; EQUIPMENT FOR MAKING OR PROCESSING DOUGHS; DOUGHS FOR BAKING [2006.01]"/> \n''')
# Close new node
fictemp.write('''</node> \n''')

# New node
fictemp.write('''<node TEXT="B: PERFORMING OPERATIONS; TRANSPORTING" POSITION="right" > \n''')
fictemp.write('''<edge COLOR="#00ff00"/> \n''')
# New sub-nodes
fictemp.write('''<node TEXT="B01: PHYSICAL OR CHEMICAL PROCESSES OR APPARATUS IN GENERAL"/> \n''')
fictemp.write('''<node TEXT="B02: CRUSHING, PULVERISING, OR DISINTEGRATING; PREPARATORY TREATMENT OF GRAIN FOR MILLING"/> \n''')
fictemp.write('''<node TEXT="B04: CENTRIFUGAL APPARATUS OR MACHINES FOR CARRYING-OUT PHYSICAL OR CHEMICAL PROCESSES"/> \n''')
# Close new node
fictemp.write('''</node> \n''')

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



'''
ecrit  = False
for lig in fic.readlines():
    if lig.count('<nodes>'):
        ecrit = True
        if ecrit:
            fictemp.write(lig)
'''
fictemp.close()


print "Mindmap file writen in " + '..//DONNEES//'+rep 

        
    


