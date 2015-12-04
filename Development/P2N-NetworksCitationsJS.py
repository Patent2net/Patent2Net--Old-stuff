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
from networkx_functs import calculate_degree, calculate_betweenness, calculate_degree_centrality
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
network = "_Citations"
mixNet = ['label', "CitedBy"]
if Networks[network][0]:

    G = nx.read_gpickle(temporPath+network)

    G.graph['mode'] = "static"
    G, deg = calculate_degree(G)
#            G, bet = calculate_betweenness(G)
#            #g, eigen = calculate_eigenvector_centrality(g)
#            G, degcent = calculate_degree_centrality(G)
    size = len(mixNet)
    count = -1

    MaxWeight = -1
  #  if G == G1:
    tutu = [int(G.node[tt]['weight']['value']) for tt in G.nodes()]
    Maxdegs = max(tutu)
    zoom = len(G)/Maxdegs # should be function of network...
#                #pos = nx.spring_layout(G, dim=2, k=2, scale =1)
 #                                        }
    pos = nx.spring_layout(G, dim=3, k=2, scale =1, iterations = 50)
            
        
            
 #                   argu='-Goverlap="9:prism" -Gsize="1000,800" -Gdim=3 -Gdimen=2 -GLT=550 -GKsep='+str(zoom)
 #                   pos=nx.graphviz_layout(G,prog='sfdp', args = argu )
            #pos = nx.graphviz_layout(G, prog='dot', args = arguDot )

 #               pos = nx.spring_layout(G, dim=2, k=3, scale =1, iterations = 800) 
           # pos = nx.spectral_layout(G, dim=2,scale =1) 
#                newCoord = project_points(pos[k][0], pos[k][1], pos[k][2], 0, 0, 1)
#                Visu['position']= {'x':newCoord[0][0], 'y':newCoord[0][1], 'z':0}
#                norme = np.linalg.norm(pos[k])
    cmpe = cmap_discretize(matplotlib.cm.jet, int(size))
    for k in G.nodes():     
        G.node[k]["weight"] = G.node[k]["weight"]['value'] # static net
        G.node[k]["id"] = G.node[k]["id"]['id']
        Visu = dict()
        Visu['color'] = dict()
        #G.node[k]['label'] =  Nodes.keys()[k]
        #G.node[k]['category'] = Nodes[Nodes.keys()[k]]['category']
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
            Visu['shape'] ="circle"
            G.node[k]['url'] =UrlPatent(G.node[k]['label'])[0]
        else:
            Visu['color']['a'] = 1 
            Visu['color']['r']= int(0) 
            Visu['color']['g']= int(0)
            Visu['color']['b']= int(0)
        
        #factx, facty = 500, 400
        posx, posy = 0, -400
        factx, facty = 1, 1 # neatto
        #pos = nx.spring_layout( G, dim=2,  scale =10, iterations = 50)
        arguDot='-Goverlap="0:prism" -Gsize="1000,800" -GLT=550 -GKsep='+str(zoom)
        pos = nx.graphviz_layout(G,prog='neato', args = arguDot )
        count = mixNet.index(G.node[k]['category']) #one color for one kind of node
        Visu['position']= {'x':((pos[k][0])*factx+posx), 'y':((pos[k][1])*facty+posy), 'z':0.0}
        Visu['size'] = np.log(int(G.node[k]["weight"])+1)+1#
        Visu['color']['a']= count
        G.node[k]['viz'] =dict()
       
            
#            Visu['color']['a']= count

#        Visu['size'] = (G.node[k]["degree"]*1.0)#(G.node[k]["degree"]*1.0/Maxdegs)*150#(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
        Visu['size'] = (G.node[k]["degree"]*zoom/Maxdegs) +1 #(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
#        Visu['size'] = np.log(int(G.node[k]["weight"])+1)*zoom+1#
        for cle in Visu.keys():
            G.node[k]['viz'][cle] = Visu[cle]
                
     #               print G.node[k]
     #       nx.set_node_attributes(G, 'weight', attr_dict)
    try:
        os.remove(ResultPathGephi+'\\'+ndf+network+'.gexf')
    except:
        try:
            os.remove(ResultPathGephi+'\\'+ndf+network+'JS.gexf')
        except:
            pass
#    
    nx.write_gexf(G, ResultPathGephi+'\\'+ndf +network+ "JS.gexf", version='1.2draft')
    fic = open(ResultPathGephi+'\\'+ndf+network+'JS.gexf', 'r')
    
    # Next is a hack to correct the bad writing of the header of the gexf file
    # with dynamics properties
    fictemp=open(ResultPathGephi+'\\'+"Good"+ndf+network+'JS.gexf', 'w')


    ecrit = True
    data = fic.read()
    # VERY UGLY Hack here !!!!
    data = data.replace('ns0:', 'viz:') # may be someone knows how to set namespace in networkx...
    data = data.replace('a="None"', '') # may be someone knows why network set the "a" attribute... 
  
    for lig in data.split('\n'):
        if lig.count('<nodes>'):
            ecrit = True
        if ecrit:
            fictemp.write(lig+'\n')
    fictemp.close()
    fic.close()
    try:
        #os.remove(ResultPathGephi+'\\'+ndf+'.gexf')
        os.remove(ResultPathGephi+'\\'+ndf+network+"JS"+'.gexf')
    except:
        pass
    
    os.rename(ResultPathGephi+'\\'+"Good"+ndf+network+'JS.gexf', ResultPathGephi+'\\'+ndf+network+"JS"+'.gexf')
    print "Network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf+network+"JS"+'.gexf'
    print
    print 
    #making the html from model
    FicRezo = ndf+network+'JS.gexf'
    with open('Graphe.html', 'r') as  fic:
        contHtml = fic.read()
        contHtml = contHtml.replace('***TitleNet***', network[1:]+' Network for ' + requete)
        #contHtml = contHtml.replace('***fichier***','../../../GephiFiles/'+FicRezo)
        contHtml = contHtml.replace('media/styles', '../../../Patent2Net/media/styles', contHtml.count('media/styles'))
        contHtml = contHtml.replace('media/js', '../../../Patent2Net/media/js', contHtml.count('media/js'))
        contHtml = contHtml.replace('***fichierConfigJS***', FicRezo.replace('.gexf','') +'Conf.js')
        with open( ResultPathGephi + '\\'+FicRezo.replace('.gexf','.html'), 'w') as FicRes:
            FicRes.write(contHtml)
    # making the js from model
            # maybe we could adjust node size and other parameters here
    with open("config.js", 'r') as fic:
        with open(ResultPathGephi + '\\'+FicRezo.replace('.gexf','') +'Conf.js', 'w') as ficRes:
            fichierJS = fic.read()
            ficRes.write(fichierJS.replace('FicRezo', FicRezo))
    #
