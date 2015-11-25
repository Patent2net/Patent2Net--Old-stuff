# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
"""
import networkx as nx
#import copy

#dicot = copy.deepcopy(dict)

import os, datetime
import numpy as np
import matplotlib.cm
from collections import OrderedDict 
from networkx_functs import calculate_degree, calculate_betweenness, calculate_degree_centrality
import cPickle as pickle
from P2N_Lib import ReturnBoolean, quote,cmap_discretize, ApparieListe2, ComputeTempoNom, flatten, DecoupeOnTheFly
#from P2N_Lib import getStatus2, getClassif,getCitations, getFamilyLenght, isMaj, quote, GenereDateLiens
#from P2N_Lib import  symbole, ReturnBoolean, FormateGephi, GenereListeSansDate, GenereReseaux3, cmap_discretize
#from Ops3 import UnNest2List


DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme

Networks =dict()

Networks["_CountryCrossTech"] =  [False, [ 'IPCR7', "country"]]
Networks["_CrossTech"] =  [False, ['IPCR7']]
Networks["_InventorCrossTech"] =  [False, ['IPCR7', "inventor-nice"]]
Networks["_ApplicantCrossTech"] =  [False, ['IPCR7', "applicant-nice"]]
Networks["_ApplicantInventor"] = [False, ["applicant-nice", "inventor-nice"]]
Networks["_Applicant"] =  [False, ["applicant-nice"]]
Networks["_Inventor"] =  [False, ["inventor-nice"]]

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
                Networks["_Inventor"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('ApplicantNetwork')>0:
                Networks["_Applicant"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('ApplicantInventorNetwork')>0:
                Networks["_ApplicantInventor"] [0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('InventorCrossTechNetwork')>0:
                Networks["_InventorCrossTech"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('ApplicantCrossTechNetwork')>0:
                Networks["_ApplicantCrossTech"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('CountryCrossTechNetwork')>0:
                Networks["_CountryCrossTech"][0] = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('CompleteNetwork')>0:
                P2NComp = ReturnBoolean(lig.split(':')[1].strip())    
            if lig.count('FamiliesNetwork')>0:
                P2NFamilly = ReturnBoolean(lig.split(':')[1].strip())    
            if lig.count('FamiliesHierarchicNetwork')>0:
                P2NHieracFamilly = ReturnBoolean(lig.split(':')[1].strip())    

BiblioPath = '..//DONNEES//'+ndf+'//PatentBiblios'

NeededInfo = ['label', 'date', 'dateDate']

for network in Networks.keys():
    mixNet = Networks[network][1]
    if Networks[network][0]:
        ListeBrevet =[]         # patentList
        Patents = set()         # Patents labels
        Nodes = OrderedDict()   # Nodes of the Graph
        Appariement = [] # collaborations for each patent
        dateMini = datetime.date(3000,1,1)
        dateMaxi =  datetime.date(1000,1,1)
        NeededInfo .extend(mixNet)  # list of needed field for building the net
        G1 = nx.DiGraph()        # dynamic network for Gephi 
        attr_dict = dict()       # attributes for the net
        G2 = nx.DiGraph()        # flat net for gexf.js may be it is possible to use previous instead of this one...
        print network, ": loading data with ", " and ".join(mixNet), " fields."
        with open (BiblioPath+'//'+ndf, 'r') as fic:    
            DataBrevet = pickle.load(fic)
        
        for brev in DataBrevet["brevets"]:
                #tempo = pickle.load(fic) # we only memorize needed nfo
            pat = OrderedDict ()
            for key in NeededInfo:
                if isinstance(brev[key], list):
                    brev[key]= flatten(brev[key])
                    brev[key]= [cont for cont in brev[key] if (cont !='empty' or cont != 'Empty' or cont !='')]

                elif isinstance (brev[key], unicode) or isinstance (brev[key], str):
                    brev[key].replace('empty', '')
                pat[key] = brev[key]
                
            for flatPat in DecoupeOnTheFly(pat, []):
                if flatPat not in ListeBrevet:
                    ListeBrevet.append(flatPat)
            if pat['label'] not in Patents:
                Patents.add(pat['label'])     
        for lab in Patents:
            temp = []
            for bre in [brev for brev in ListeBrevet if brev['label']==lab]:
                for cat in mixNet:
                    if  (bre[cat],  cat) not in temp:
                        temp.append((bre[cat],  cat))
                        Dates = [] 
                        tempo = bre['date'].split('-')
                        Dates.append(datetime.date(int(tempo[0]), int(tempo[1]), int(tempo[2] )))                     
                         
                    elif bre['dateDate'] not in Dates:
                        Dates.append(bre['dateDate'])#.split('-')[0])
                    else:
                        pass
            #tempo = [tt for tt in set(temp)]
            
            if len(temp)>1: # only collaborators in the net
                Appariement.append(([noeud[0] for noeud in temp], Dates))
                #Building nodes properties
                for noeud in temp:
                    if noeud[0] not in Nodes.keys():
                        Nodes[noeud[0]] = OrderedDict ()
                        Nodes[noeud[0]]['date'] = Dates
                        Nodes[noeud[0]]['category'] = noeud[1]
                        Nodes[noeud[0]]['label'] = noeud[0]
                    else:
                        pass
                    
        appars = []
        for lst, date in Appariement:  
                    
            appars.extend([(couple, date) for couple in ApparieListe2(lst)])
        
        Pondere = OrderedDict ()
        for link, dat in appars:
            if tuple(link) in Pondere.keys():
                Pondere[tuple(link)]['weight'] +=1
                
            else:
                Pondere[tuple(link)] = OrderedDict ()
                Pondere[tuple(link)]['weight'] = 1
                Pondere[tuple(link)]['date'] = dat# [x for x in Nodes[link[0]]['date'] if x in Nodes[link[1]]['date']]
                Pondere[tuple(link)]['date'].sort()
                
                if dat[len(dat)-1] > dateMaxi: # compute period network
                        dateMaxi = dat[len(dat)-1]
                if dat[0] < dateMini:
                    dateMini = dat[0]
        
        
        rep = ndf.replace('Families', '')
        BiblioPath = '..//DONNEES//'+ndf+'//PatentBiblios'
        ResultPathGephi = '..//DONNEES//'+ndf+'//GephiFiles'
        ResultPathContent = '..//DONNEES//'+ndf  #+'//PatentContentsHTML'
        try:
            os.mkdir(ResultPathGephi)
        except:
            pass
            #listeDates = []
        
        #       V2 : Brev contaains field applicant-nice that is fully Gephi compatible

           # ListeNoeuds = Nodes

        # CREATING THE WEIGHTED GRAPH   
        for (source, target), datum in appars: 
            for dat in datum:
                fin = datetime.date(dat.year+20, dat.month, dat.day)
                attr_dict={'weight' : Pondere[(source, target)]['weight'], 
                'start' : dat.isoformat(),
                'end': fin.isoformat()}
                G1.add_edge(Nodes.keys().index(source), Nodes.keys().index(target), attr_dict)
                G2.add_edge(Nodes.keys().index(source), Nodes.keys().index(target), {'weight' : Pondere[(source, target)]['weight']})
        for G in [G1, G2]:
            G.graph['defaultedgetype'] = "directed"
            if G==G1:
                G.graph['timeformat'] = "date"
                G.graph['mode'] = "dynamic"
                G.graph['start'] = dateMini
                
                G.graph['end'] = dateMaxi
            G, deg = calculate_degree(G)
            G, bet = calculate_betweenness(G)
            #g, eigen = calculate_eigenvector_centrality(g)
            G, degcent = calculate_degree_centrality(G)
            size = len(mixNet)
            count = -1
            if G==G2:                
                MaxWeight = -1
                cmpe = cmap_discretize(matplotlib.cm.jet, int(size))
        #        x = resize(arange(100), (5,100))
                if size>6:
                    colors = [cmpe(i*1024/(int(size))) for i in range(int(size))]      
                else:
                    colors = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1]]
                tutu = [G.node[tt]['degree'] for tt in G.nodes()]
                Maxdegs = max(tutu)
                zoom = len(G)/Maxdegs # should be function of network...
        
            for k in G.nodes():
                G.node[k]['label'] =  Nodes.keys()[k]
                G.node[k]['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&locale=en_EP&DB=EPODOC&PA='+quote('"'+ComputeTempoNom(Nodes.keys()[k])+'"')
                G.node[k]['category'] = Nodes[Nodes.keys()[k]]['category']
                if G == G1:
                    G.node[k]['weight']={'value' : len(Nodes[Nodes.keys()[k]]['date']), 
                        'start' : Nodes[Nodes.keys()[k]]['date'][0].isoformat(),
                        'end': datetime.date(Nodes[Nodes.keys()[k]]['date'][0].year + 20,Nodes[Nodes.keys()[k]]['date'][0].month, Nodes[Nodes.keys()[k]]['date'][0].day ).isoformat()
                                        }
                if G==G2:
                    #pos = pos=nx.graphviz_layout(G,prog='sfdp', args='-Goverlap="scale" -Gsize="1000,800" -GK=.05' )
        #                    pos = nx.spring_layout(G, dim=2, k=2, scale =1, iterations = 5000) 
                    Visu = dict()
        #                newCoord = project_points(pos[k][0], pos[k][1], pos[k][2], 0, 0, 1)
        #                Visu['position']= {'x':newCoord[0][0], 'y':newCoord[0][1], 'z':0}
        #                norme = np.linalg.norm(pos[k])
                    count = mixNet.index(Nodes[Nodes.keys()[k]]['category']) #one color for one kind of node
        #                Visu['position']= {'x':((pos[k][0])*800+400), 'y':((pos[k][1])*700+350), 'z':0.0}
                    Visu['color'] = dict()
                    Visu['color']['r']= int(colors[count][0]*254) 
                    Visu['color']['g']= int(colors[count][1]*254)
                    Visu['color']['b']= int(colors[count][2]*254)
                    #Visu['color']['a']= count
                    #Visu['color']['a']= count
                    
        #                Visu['size'] = (G.node[k]["degree"]*1.0)#(G.node[k]["degree"]*1.0/Maxdegs)*150#(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
        #                Visu['size'] = (G.node[k]["degree"]*zoom/Maxdegs) +1 #(G.node[k]["weight"]) /MaxWeight #addd 1 for viewiong all...
                    Visu['size'] = np.log(G.node[k]["degree"]+1)*zoom+1#
                    G.node[k]['viz'] =dict()
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
        nx.write_gexf(G1, ResultPathGephi+'\\'+ndf+network + ".gexf", version='1.2draft')
        fic = open(ResultPathGephi+'\\'+ndf+network+'.gexf', 'r')
        
        # Next is a hack to correct the bad writing of the header of the gexf file
        # with dynamics properties
        fictemp=open(ResultPathGephi+'\\'+"Good"+network+ndf+'.gexf', 'w')
        fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">
        <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
            <attributes class="edge" mode="static">
        
            </attributes>
        	<attributes class="edge" mode="dynamic">
              <attribute id="6" title="time" type="integer" />
            </attributes>
        	<attributes class="node" mode="dynamic">
        			<attribute id="5" title="time" type="integer" />
        			</attributes>
            <attributes class="node" mode="static">
        	<attribute id="1" title="unkkown" type="integer" />
        	<attribute id="2" title="degree_cent" type="integer" />
        
             <attribute id="3" title="degree" type="integer" />
             <attribute id="4" title="url" type="string" />
             <attribute id="0" title="category" type="string" />
         	</attributes>
          
         """)
        
        ecrit  =False
        data = fic.read()
        # VERY UGLY Hack here !!!!
        data = data.replace('ns0:', 'viz:') # may be someone knows how to set namespace in networkx...
        data = data.replace('a="None"', '') # may be someone knows why network set the "a" attribute... 
        data = data.replace('value="{', '')
        data = data.replace("'start': ", "start=")
        data = data.replace("'end': ", "end=")
        data = data.replace("'value': ", 'value="')
        data = data.replace("',", "'")        
        data = data.replace("}", "")   
        for lig in data.split('\n'):
            if lig.count('<nodes>'):
                ecrit = True
            if ecrit:
                fictemp.write(lig+'\n')
        fictemp.close()
        fic.close()
        try:
            try:
                os.remove(ResultPathGephi+'\\'+ndf+network+'.gexf')
            except:
                pass
            os.rename(ResultPathGephi+'\\'+"Good"+network+ndf+'.gexf', ResultPathGephi+'\\'+ndf+network+'.gexf')
            print "Network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf+network+'.gexf'
            os.remove(ResultPathGephi+'\\Good'+ndf+network+'.gexf')
        except:
            pass
        
        nx.write_gexf(G2, ResultPathGephi+'\\'+ndf +network+ "JS.gexf", version='1.2draft')
        fic = open(ResultPathGephi+'\\'+ndf+network+'JS.gexf', 'r')
        
        # Next is a hack to correct the bad writing of the header of the gexf file
        # with dynamics properties
        fictemp=open(ResultPathGephi+'\\'+"Good"+ndf+network+'JS.gexf', 'w')
        fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">
        <graph defaultedgetype="directed" mode="static">
            <attributes class="edge" mode="static">
                <attribute id="5" title="weight" type="integer" />
            </attributes>
        
            <attributes class="node" mode="static">
             <attribute id="1" title="degree_cent" type="integer" />
             <attribute id="2" title="degree" type="integer" />
             <attribute id="3" title="url" type="string" />
             <attribute id="0" title="category" type="string" />
         	</attributes>
          
         """)
        ecrit  =False
        data = fic.read()
        # VERY UGLY Hack here !!!!
        data = data.replace('ns0:', 'viz:') # may be someone knows how to set namespace in networkx...
        data = data.replace('a="None"', '') # may be someone knows why network set the "a" attribute... 
        #                data = data.replace('value="{', '')
        #                data = data.replace("'start': ", "start=")
        #                data = data.replace("'end': ", "end=")
        #                data = data.replace("'value': ", 'value="')
        #                data = data.replace("',", "'")        
        #                data = data.replace("}", "")   
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
        with open("config.js", 'r') as fic:
            with open(ResultPathGephi + '\\'+FicRezo.replace('.gexf','') +'Conf.js', 'w') as ficRes:
                fichierJS = fic.read()
                ficRes.write(fichierJS.replace('FicRezo', FicRezo))
        #
