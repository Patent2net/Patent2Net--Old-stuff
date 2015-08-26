# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:34:15 2015

@author: Celso

Objective: Crate a FreePlane (mindmap) file
"""
import pickle

ListeBrevet = []  
DataBrevets = []
Stop = False

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

''' The following liner are for testing only '''
for i in {1,2,3,4,5}:
    print DataBrevets['brevets'][i]['applicant']

''' End of tesing lines '''

fictemp=open('..//DONNEES//'+rep+'//FP'+rep+'.mm', 'w')

fictemp.write('''<map version="freeplane 1.3.0"> \n''')
fictemp.write('''<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net --> \n''')
fictemp.write('''<node TEXT="''' + rep + '''" > \n''')
fictemp.write('''<icon BUILTIN="clock2"/> \n''')
fictemp.write('''<hook NAME="MapStyle"> \n''')
fictemp.write(''' a \n''')



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

        
    


