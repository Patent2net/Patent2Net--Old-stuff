# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
"""
import networkx as nx
#import copy

#dicot = copy.deepcopy(dict)

import os
import sys
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
Nets = ["CountryCrossTech", "CrossTech", "InventorsCrossTech", "Applicants_CrossTech", "Inventors",
 "ApplicantInventor", "Applicants", "References", "Citations", "Equivalents"]

if len(sys.argv)<2 or sys.argv[1] not in Nets:
    print "give me a net as parameter, one from this list: ", Nets
    sys.exit()
else:
    Nets.remove(sys.argv[1]) 
screenX = 1800
screenY = 1600 #big screen for Gephi Idont know how to set Z...
screenZ = 1200

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
Networks["_References"] =  [False, [ "label", 'CitP', "CitO"]]
Networks["_Citations"] =  [False, [  "label", "CitedBy"]]
Networks["_Equivalents"] =  [False, [  "label", "equivalents"]]
Networks["_"+sys.argv[1]][0] = True #setting net to true but reading parameter file can reverse this
ListeBrevet = []
#ouverture fichier de travail
#On récupère la requête et les noms des fichiers de travail
with open("../Requete.cql", "r") as fic:
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

ResultPathGephi = '../DONNEES/'+ndf+'/GephiFiles'
BiblioPath = '../DONNEES/'+ndf+'/PatentBiblios'
temporPath = '../DONNEES/'+ndf+'/tempo'
print "bibliographic data of ", ndf, " patent universe found."

NeededInfo = ['label', 'date', 'prior-dateDate'] # mandatory

#overloading to False network creation, these are processed through p2n-NetworkMix script
for net in Nets: #passing other to false, but the script can be called
    Networks["_"+net][0] = False     # and the switch setted to false: the script won't process

Category =dict()
appars = []
somme =  0
network = "_" +sys.argv[1]
mixNet = Networks[network][1]
if Networks[network][0]:
 
#        nx.set_node_attributes(G1,  'weight', AtribDynLab[Nodes.keys().index(source)] ['weight'])
    G = nx.read_gpickle(temporPath+ '/'+network)
    
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
    
    
    
    pos = nx.spring_layout( G, dim=3,  scale =10, iterations = 100)
    factx, facty = 1, 1 # neatto
    tutu = [int(G.node[tt]['weight']['value']) for tt in G.nodes()]
    Maxdegs = max(tutu)        
    MaxWeight = -1
    MaxPosX = max([pos[k][0] for k in pos.keys()])
    MaxPosY = max([pos[k][1] for k in pos.keys()])
    MaxPosZ = max([pos[k][2] for k in pos.keys()])
    MinPosX = min([pos[k][0] for k in pos.keys()])
    MinPosY = min([pos[k][1] for k in pos.keys()])
    MinPosZ = min([pos[k][2] for k in pos.keys()])
    
    GvScreenX = MaxPosX-MinPosX
    GvScreenY = MaxPosY-MinPosY
    GvScreenZ = MaxPosZ-MinPosZ
    factx = screenX/GvScreenX
    factz = screenZ/GvScreenZ
    facty = screenX/GvScreenY
    zoom = len(G)/Maxdegs # should be function of network...
    if MinPosY>0:
        posx, posy = 0, -800
    else:
        posx, posy = 0, 0
    if MinPosZ > 0:
        posz = -600
    else:
        posz = 0
        
    for k in G.nodes():     
        Visu= dict()
        Visu['color'] = dict()
        Visu['position']= {'x':(int(pos[k][0])*factx+posx), 'y':(int(pos[k][1])*facty+posy), 'z':(int(pos[k][2])*factz+posz)}

        if G.node[k]['category'] == 'label':
            G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(254) 
            Visu['color']['g']= int(0)
            Visu['color']['b']= int(0)
            Visu['shape'] ="diamond"
        elif G.node[k]['category'] =='CitP': 
                Visu['color']['a'] = 1 
                Visu['color']['r']= int(0) 
                Visu['color']['g']= int(254)
                Visu['color']['b']= int(0)
                Visu['shape'] ="ellipse"

        elif G.node[k]['category'] == 'CitO':
            # a hack here, trying to find out content in scholar
            #https://scholar.google.fr/scholar?hl=fr&q=pipo+test&btnG=&lr=
            Visu['color']['r']= int(0) 
            Visu['color']['g']= int(0)
            Visu['color']['b']= int(254)
            Visu['color']['a'] =1 
            Visu['shape'] ="disc"
            #UrlTemp = "https://scholar.google.com/scholar?q=" + quot(Nodes.keys()[k])
            #G.node[k]['url'] = UrlTemp
        elif G.node[k]['category'] == 'CitedBy':
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(0) 
            Visu['color']['g']= int(127)
            Visu['color']['b']= int(127)
            Visu['shape'] ="square"
            G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
            
        elif G.node[k]['category'] == "equivalents":
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(127) 
            Visu['color']['g']= int(127)
            Visu['color']['b']= int(0)
            Visu['shape'] ="ellipse"
            G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
        elif G.node[k]['category'] == 'applicant-nice':
            G.node[k]['category'] = 'applicant'# for readable facility
            G.node[k]['url'] = UrlApplicantBuild(G.node[k]['label'])[0]
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(127) 
            Visu['color']['g']= int(0)
            Visu['color']['b']= int(127)
            Visu['shape'] ="star"
        elif G.node[k]['category'] == 'IPCR1' or G.node[k]['category'] == 'IPCR3' or G.node[k]['category'] == 'IPCR4' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'CPC':
            G.node[k]['url'] = UrlIPCRBuild(G.node[k]['label'])[0]
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(127) 
            Visu['color']['g']= int(254)
            Visu['color']['b']= int(127)
            Visu['shape'] ="database"
        elif G.node[k]['category'] == 'inventor-nice':
            G.node[k]['category'] = 'inventor'# for readable facility
            G.node[k]['url'] = UrlInventorBuild(G.node[k]['label'])[0]
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(127) 
            Visu['color']['g']= int(127)
            Visu['color']['b']= int(254)
            Visu['shape'] ="triangleDown"
        else:
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(254) 
            Visu['color']['g']= int(254)
            Visu['color']['b']= int(254)
            Visu['shape'] ="box"
        if "label" not in mixNet:
            mixNet.append('label')
        #factx, facty = 500, 400
        G.node[k]['viz'] =dict()
        for cle in Visu.keys():
            G.node[k]['viz'][cle] = Visu[cle]


    
    

    try:
        os.remove(ResultPathGephi+'/'+ndf+network+'.gexf')
    except:
        pass
    nx.write_gexf(G, ResultPathGephi+'/'+ndf+network + ".gexf", version='1.2draft')
    fic = open(ResultPathGephi+'/'+ndf+network+'.gexf', 'r')
    
    # Next is a hack to correct the bad writing of the header of the gexf file
    # with dynamics properties
    fictemp=open(ResultPathGephi+'/'+"Good"+network+ndf+'.gexf', 'w')
    fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">
  <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
  <attributes class="node" mode="static">
  <attribute id="0" title="category" type="string" />
   <attribute id="2" title="url" type="string" />
   </attributes>
	<attributes class="node" mode="dynamic">
		<attribute id="1" title="weight" type="integer" />
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
            if lig.count('attvalue')>0 and lig.count('for="1"')>0:
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
            os.remove(ResultPathGephi+'/'+ndf+network+'.gexf')
        except:
            pass
        os.rename(ResultPathGephi+'/'+"Good"+network+ndf+'.gexf', ResultPathGephi+'/'+ndf+network+'.gexf')
        print "Dynamic Gexf network file writen into ",  ResultPathGephi+' directory.\n See file: '+ndf+network+'.gexf'
        os.remove(ResultPathGephi+'/Good'+ndf+network+'.gexf')
    except:
        pass
    
