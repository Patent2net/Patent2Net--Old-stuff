# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
"""
import networkx as nx
#import copy

#dicot = copy.deepcopy(dict)

import os
import datetime
import pydot
import ctypes # pydot needed for pyinstaller !!! seems that ctype also I should learn making hooks....
from urllib import quote as quot
import numpy as np
import matplotlib.cm
from collections import OrderedDict 
#from networkx_functs import calculate_degree, calculate_betweenness, calculate_degree_centrality
import cPickle as pickle
import copy
from P2N_Lib import ReturnBoolean, UrlPatent,UrlApplicantBuild,UrlInventorBuild,UrlIPCRBuild, cmap_discretize, flatten, DecoupeOnTheFly
#from P2N_Lib import getStatus2, getClassif,getCitations, getFamilyLenght, isMaj, quote, GenereDateLiens
#from P2N_Lib import  symbole, ReturnBoolean, FormateGephi, GenereListeSansDate, GenereReseaux3, cmap_discretize
#from Ops3 import UnNest2List


DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme

Networks =dict()
#next lines are here to avoid the changing scheme lecture of requete.cql
Networks["_CountryCrossTech"] =  [False, [ 'IPCR7', "country"]]
Networks["_CrossTech"] =  [False, ['IPCR7']]
Networks["_InventorsCrossTech"] =  [False, ['IPCR7', "inventor-nice"]]
Networks["_Applicants_CrossTech"] =  [False, ['IPCR7', "applicant-nice"]]
Networks["_ApplicantInventor"] = [False, ["applicant-nice", "inventor-nice"]]
Networks["_Applicants"] =  [False, ["applicant-nice"]]
Networks["_Inventors"] =  [False, ["inventor-nice"]]
#here we start
Networks["_References"] =  [True, [ 'label', 'CitP', "CitO"]]
Networks["_Citations"] =  [True, [ 'label', "CitedBy"]]
Networks["_Equivalents"] =  [True, [ 'label', "equivalents"]]
ListeBrevet = []
#ouverture fichier de travail
#On récupère la requête et les noms des fichiers de travail
with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()
            if lig.count('GatherContent')>0:
                Gather = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherBiblio')>0:
                GatherBiblio = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherPatent')>0:
                GatherPatent = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherFamilly')>0:
                GatherFamilly = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('InventorNetwork')>0:
                Networks["_Inventors"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('ApplicantNetwork')>0:
                Networks["_Applicants"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('ApplicantInventorNetwork')>0:
                Networks["_ApplicantInventor"] [0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('InventorCrossTechNetwork')>0:
                Networks["_InventorsCrossTech"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('ApplicantCrossTechNetwork')>0:
                Networks["_Applicants_CrossTech"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('CountryCrossTechNetwork')>0:
                Networks["_CountryCrossTech"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('CrossTechNetwork')>0:
                Networks["_CrossTech"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('CompleteNetwork')>0:
                P2NComp = ReturnBoolean(lig.split(':')[1].strip())    
            if lig.count('FamiliesNetwork')>0:
                P2NFamilly = ReturnBoolean(lig.split(':')[1].strip())    
            if lig.count('FamiliesHierarchicNetwork')>0:
                P2NHieracFamilly = ReturnBoolean(lig.split(':')[1].strip())    
            if lig.count('References')>0:
                Networks["_References"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('Citations')>0:
                Networks["_Citations"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('Equivalents')>0:
                Networks["_Equivalents"][0] = ReturnBoolean(lig.split(':')[1].strip())

ResultPathGephi = '..//DONNEES//'+ndf+'//GephiFiles'
BiblioPath = '..//DONNEES//'+ndf+'//PatentBiblios'
temporPath = '..//DONNEES//'+ndf+'//tempo'
print "bibliographic data of ", ndf, " patent universe found."

NeededInfo = ['label', 'date', 'prior-dateDate']
#overloading toi False network creation, these are processed through p2n-NetworkMix script
Networks["_CountryCrossTech"] =  [False, [ 'IPCR7', "country"]]
Networks["_CrossTech"] =  [False, ['IPCR7']]
Networks["_InventorsCrossTech"] =  [False, ['IPCR7', "inventor-nice"]]
Networks["_Applicants_CrossTech"] =  [False, ['IPCR7', "applicant-nice"]]
Networks["_ApplicantInventor"] = [False, ["applicant-nice", "inventor-nice"]]
Networks["_Applicants"] =  [False, ["applicant-nice"]]
Networks["_Inventors"] =  [False, ["inventor-nice"]]
Category =dict()
appars = []
somme =  0
network = "_Equivalents"
mixNet = ['label', "equivalents"]

if Networks[network][0]:
 
#        nx.set_node_attributes(G1,  'weight', AtribDynLab[Nodes.keys().index(source)] ['weight'])
    G = nx.read_gpickle(temporPath+network)
    
    G.graph['defaultedgetype'] = "directed"
    G.graph['timeformat'] = "date"
    G.graph['mode'] = "dynamic"
#    G.graph['start'] = dateMini
#    G.graph['end'] = dateMaxi

#            G, deg = calculate_degree(G)
#            G, bet = calculate_betweenness(G)
#            #g, eigen = calculate_eigenvector_centrality(g)
#            G, degcent = calculate_degree_centrality(G)
    size = len(mixNet)
    count = -1
    

            
    MaxWeight = -1

    tutu = [int(G.node[tt]['weight']['value']) for tt in G.nodes()]
    for k in G.nodes():     
        #G.node[k]['label'] =  Nodes.keys()[k]
        #G.node[k]['category'] = Nodes[Nodes.keys()[k]]['category']
        

        if G.node[k]['category'] == 'label' or G.node[k]['category'] =='CitP' :
            G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
        elif G.node[k]['category'] == 'CitedBy':
            G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
            
        elif G.node[k]['category'] == "equivalents":
            G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
        else:
             G.node[k]['url'] =""

    Maxdegs = max(tutu)
    zoom = len(G)/Maxdegs # should be function of network...

    try:
        os.remove(ResultPathGephi+'\\'+ndf+network+'.gexf')
    except:
        pass
    nx.write_gexf(G, ResultPathGephi+'\\'+ndf+network + ".gexf", version='1.2draft')
    fic = open(ResultPathGephi+'\\'+ndf+network+'.gexf', 'r')
    
    # Next is a hack to correct the bad writing of the header of the gexf file
    # with dynamics properties
    fictemp=open(ResultPathGephi+'\\'+"Good"+network+ndf+'.gexf', 'w')
    fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">
  <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
  <attributes class="node" mode="static">
  <attribute id="0" title="category" type="string" />
   <attribute id="1" title="url" type="string" />
   </attributes>
	<attributes class="node" mode="dynamic">
		<attribute id="2" title="weight" type="integer" />
	</attributes>
	<attributes class="edge" mode="static">
		<attribute id="3" title="weight" type="integer" />
	</attributes>
	<attributes class="edge" mode="dynamic">
	</attributes>
      
     """)
    
    ecrit  =False
    data = fic.read()
    # VERY VERY VERY UGLY Hack here !!!!
    data = data.replace('ns0:', 'viz:') # may be someone knows how to set namespace in networkx...
    data = data.replace('a="None"', '') # may be someone knows why network set the "a" attribute... 

    data = data.replace('value="{', '')
    data = data.replace("'start': ", "start=")
    data = data.replace("'end': ", "end=")
    data = data.replace("'value': ", 'value=')
    data = data.replace("',", "'")        
    data = data.replace("}", "")   
    for lig in data.split('\n'): # in french we call that bricolage...
    # mistakes have been done in data associations... bugssssss
        if lig.count('<nodes>'):
            ecrit = True
        if ecrit:
            if lig.count('<node ')>0:
                
                lig = lig.replace('id="{', '')
                lig = lig.replace("'id': ", 'id="')
                ind1 = lig.index(", 'label'")
                ind2 = lig[ind1:].index(" label")+ind1
                memo = lig[ind1:ind2]
                lig = lig.replace(memo, '"')
#                if lig.count('attvalue')>0 and lig.count('for="1"')>0:
#                    lig = lig.replace('" />', " />")
            if lig.count('<edge')>0 and lig.count('<edges>')==0:
                ind1 = lig.index('start=')
                ind2 = lig[ind1:].index(" 'id': ")+ind1
                memo = lig[ind1:ind2]
                lig = lig.replace(lig[ind1:ind2+7], '')
                lig = lig.replace('target="{', 'target="')
                lig = lig.replace('source="{', 'source="')

                ind = lig.index(", 'label")
                ind2 = lig[ind:].index('target') + ind
                lig = lig.replace(lig[ind:ind2], '" ')
                ind = lig.index(", 'label")
                ind2 = lig[ind:].index('">') + ind+2
                lig = lig.replace(lig[ind:ind2], '" '+ memo +' >')
                if lig.count('start') ==2:
                    ind= lig.index('target')
                    ind2= lig[ind+14:].index(": ")
                    lig = lig.replace(lig[ind: 14+len(lig[:ind])+ind2+2], 'target="')
            if lig.count('attvalue')>0 and lig.count('for="2"')>0:
                lig = lig.replace("""'\" />""", "' />")
#                    lig = lig.replace("'id': ", 'source="', 1)
#                    lig = lig.replace("id': ", 'target="',1)
#                    ind1 = lig.index("end='")
#                    ind2 = lig.index("source")
#                    lig = lig.replace(lig[ind1:ind2], '')
#                    lig = lig.replace("'", '"')
            fictemp.write(lig+'\n')
    fictemp.close()
    fic.close()
    try:
        try:
            os.remove(ResultPathGephi+'\\'+ndf+network+'.gexf')
        except:
            pass
        os.rename(ResultPathGephi+'\\'+"Good"+network+ndf+'.gexf', ResultPathGephi+'\\'+ndf+network+'.gexf')
        print "Dynamic Gexf network file writen into ",  ResultPathGephi+' directory.\n See file: '+ndf+network+'.gexf'
        os.remove(ResultPathGephi+'\\Good'+ndf+network+'.gexf')
    except:
        pass
    
