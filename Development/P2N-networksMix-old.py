# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
"""
import networkx as nx
#import copy

#dicot = copy.deepcopy(dict)

import os, datetime, pydot, copy
import numpy as np
import matplotlib.cm
from collections import OrderedDict 
from networkx_functs import calculate_degree, calculate_betweenness, calculate_degree_centrality
import cPickle as pickle
from P2N_Lib import ReturnBoolean, UrlPatent,UrlApplicantBuild,UrlInventorBuild,UrlIPCRBuild, cmap_discretize, ApparieListe2, flatten, DecoupeOnTheFly
#from P2N_Lib import getStatus2, getClassif,getCitations, getFamilyLenght, isMaj, quote, GenereDateLiens
#from P2N_Lib import  symbole, ReturnBoolean, FormateGephi, GenereListeSansDate, GenereReseaux3, cmap_discretize
#from Ops3 import UnNest2List


DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme

Networks =dict()


Networks["_CountryCrossTech"] =  [False, [ 'IPCR7', "country"]]
Networks["_CrossTech"] =  [False, ['IPCR7']]
Networks["_InventorsCrossTech"] =  [False, ['IPCR7', "inventor-nice"]]
Networks["_Applicants_CrossTech"] =  [False, ['IPCR7', "applicant-nice"]]
Networks["_InventorsApplicants"] = [False, ["applicant-nice", "inventor-nice"]]
Networks["_Applicants"] =  [False, ["applicant-nice"]]
Networks["_Inventors"] =  [False, ["inventor-nice"]]
ListeBrevet = []

class OrderedNodeGraph(nx.DiGraph):
     node_dict_factory=OrderedDict
     edge_dict_factory=OrderedDict


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
            if lig.count('ApplicantInventorNet')>0:
                Networks["_InventorsApplicants"] [0] = ReturnBoolean(lig.split(':')[1].strip())
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

BiblioPath = '..//DONNEES//'+ndf+'//PatentBiblios'

NeededInfo = ['label', 'date', 'dateDate']
Category =dict()
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
        G1 = OrderedNodeGraph()        # dynamic network for Gephi 
        attr_dict = dict()       # attributes for the net
        G2 = OrderedNodeGraph()        # flat net for gexf.js may be it is possible to use previous instead of this one...
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

                for noeud, cat in temp:
                    if noeud != '':
                        Category[noeud] = cat
                    
        appars = []
        for lst, date in Appariement:  
                    
            appars.extend([(couple, date) for couple in ApparieListe2(lst) if couple[0] !='' and couple[1] !=''])
        
        Pondere = OrderedDict ()
        for link, dat in appars:
            if tuple(link) in Pondere.keys():
                Pondere[tuple(link)]['weight'] +=1
                Pondere[tuple(link)]['date'].append(dat)
                Pondere[tuple(link)]['date'].sort()
            else:
                Pondere[tuple(link)] = OrderedDict ()
                Pondere[tuple(link)]['weight'] = 1
                Pondere[tuple(link)]['date'] = [dat]# [x for x in Nodes[link[0]]['date'] if x in Nodes[link[1]]['date']]
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
        AtribDynLab = dict()
        WeightDyn = dict()
        for (source, target), datum in appars: 
            if (source, target) not in WeightDyn.keys():
                WeightDyn[(source, target)] = dict()
            for dat in datum:
                fin = datetime.date(dat.year+20, dat.month, dat.day) #setting endtime collaboration to 20 year after starting date....
                if int(fin.year) - int(datetime.date.today().year)>2:
                    fin = datetime.date(int(datetime.date.today().year)+2, int(datetime.date.today().month), int(datetime.date.today().day))
                if 'weight' not in WeightDyn[(source, target)].keys():
                    WeightDyn[(source, target)]['weight'] = []
                    tempo = dict()
                    tempo['value'] = 1
                    tempo['start'] = dat.isoformat()
                    tempo['end'] = fin.isoformat()
                    WeightDyn[(source, target)]['weight'].append(tempo)
                    
                else:
                    tempo = dict()
                    tempo['value'] = WeightDyn[(source, target)]['weight'][len(WeightDyn[(source, target)]['weight'])-1]['value']+1
                    tempo['start'] = dat.isoformat()
                    tempo['end'] = fin.isoformat()
                    WeightDyn[(source, target)]['weight'].append(tempo)
                    WeightDyn[(source, target)]['weight'].sort()
                    cpt=1
                    for iterat in WeightDyn[(source, target)]['weight']:
                        iterat['value'] = cpt
                        cpt+=1
                
#            else:WeightDyn[(source, target)]['weight']
#                for dat in datum:
#                    if 'weight' not in WeightDyn[(source, target)].keys():
#                        WeightDyn[(source, target)]['weight'] = [1]
#                    else:
#                        WeightDyn[(source, target)]['weight'].append(WeightDyn[(source, target)]['weight'][len(WeightDyn[(source, target)]['weight'])-1]+1)
#                    if 'start' not in WeightDyn[(source, target)].keys():
#                        WeightDyn[(source, target)]['start'] = [dat.isoformat()]
#                    else:
#                        WeightDyn[(source, target)]['start'].append(dat.isoformat())
#                    fin = datetime.date(dat.year+20, dat.month, dat.day) #setting endtime collaboration to 20 year after starting date....
#                    if int(fin.year) - int(datetime.date.today().year)>2:
#                        fin = datetime.date(int(datetime.date.today().year)+2, int(datetime.date.today().month), int(datetime.date.today().day))
#
#                    if 'end' not in WeightDyn[(source, target)].keys():
#                        WeightDyn[(source, target)]['end'] = [fin.isoformat()]
#                    else:
#                        WeightDyn[(source, target)]['end'].append(fin.isoformat())

                
            if source not in Nodes.keys() and source != '':
                Nodes[source] = OrderedDict ()
                Nodes[source]['date'] = Dates
                Nodes[source]['category'] = Category[source]
                Nodes[source]['label'] = source
            else:
                pass
            if target not in Nodes.keys() and target != '':
                Nodes[target] = OrderedDict ()
                Nodes[target]['date'] = Dates
                Nodes[target]['category'] = Category[target]
                Nodes[target]['label'] = target
            else:
                pass
            for dat in datum:
                fin = datetime.date(dat.year+20, dat.month, dat.day)
                if int(fin.year) - int(datetime.date.today().year)>2:
                    fin = datetime.date(int(datetime.date.today().year)+2, int(datetime.date.today().month), int(datetime.date.today().day))
                attr_dict_lab = dict()
                attr_dict_weight = dict()
                if Nodes.keys().index(source) in AtribDynLab.keys():
                    existant =  AtribDynLab[Nodes.keys().index(source)] ['label']['start'].split('-')
                    dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                    G1deb= min(dat, dateActu).isoformat()
                    existant =  AtribDynLab[Nodes.keys().index(source)] ['label']['end'].split('-')
                    dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                    G1fin = max(fin, dateActu ).isoformat()
                    G1poids = int(AtribDynLab[Nodes.keys().index(source)] ['weight']['value']) +1
                    attr_dict_lab['label'] = Nodes[source]['label']
                    attr_dict_lab['start'] = G1deb
                    attr_dict_lab['end'] = G1fin
                    attr_dict_weight['value'] =str(G1poids)
                    attr_dict_weight['start'] = G1deb
                    attr_dict_weight['end'] = G1fin
                    AtribDynLab[Nodes.keys().index(source)] ['label'] = copy.copy(attr_dict_lab)
                    AtribDynLab[Nodes.keys().index(source)] ['weight'] = copy.copy(attr_dict_weight)
                else:
                    G1deb=dat.isoformat()
                    G1fin = fin.isoformat()
                    G1poids = 1
                    attr_dict_lab['label'] = Nodes[source]['label']
                    attr_dict_lab['start'] = G1deb
                    attr_dict_lab['end'] = G1fin
                    attr_dict_weight['value'] =str(G1poids)
                    attr_dict_weight['start'] = G1deb
                    attr_dict_weight['end'] = G1fin
                    AtribDynLab[Nodes.keys().index(source)] = dict()
                    AtribDynLab[Nodes.keys().index(source)] ['label'] = copy.copy(attr_dict_lab)
                    AtribDynLab[Nodes.keys().index(source)] ['weight'] = copy.copy(attr_dict_weight)
                #setting node properties (target)
                if Nodes.keys().index(target) in AtribDynLab.keys():
                    existant =  AtribDynLab[Nodes.keys().index(target)] ['label']['start'].split('-')
                    dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                    G1deb= min(dat, dateActu).isoformat()
                    existant =  AtribDynLab[Nodes.keys().index(target)] ['label']['end'].split('-')
                    dateActu = datetime.date (int(existant[0]), int(existant[1]), int(existant[2]))
                    G1fin = max(fin, dateActu ).isoformat()
                    G1poids = int(AtribDynLab[Nodes.keys().index(target)] ['weight']['value']) +1
                    attr_dict_lab['label'] = Nodes[target]['label']
                    attr_dict_lab['start'] = G1deb
                    attr_dict_lab['end'] = G1fin
                    attr_dict_weight['value'] =str(G1poids)
                    attr_dict_weight['start'] = G1deb
                    attr_dict_weight['end'] = G1fin
                    AtribDynLab[Nodes.keys().index(target)] ['label'] =copy.copy( attr_dict_lab)
                    AtribDynLab[Nodes.keys().index(target)] ['weight'] = copy.copy(attr_dict_weight)
                else:
                    G1deb=dat.isoformat()
                    G1fin = fin.isoformat()
                    G1poids = 1
                    attr_dict_lab['label'] = Nodes[target]['label']
                    attr_dict_lab['start'] = G1deb
                    attr_dict_lab['end'] = G1fin
                    attr_dict_weight['value'] =str(G1poids)
                    attr_dict_weight['start'] = G1deb
                    attr_dict_weight['end'] = G1fin
                    AtribDynLab[Nodes.keys().index(target)] = dict()
                    AtribDynLab[Nodes.keys().index(target)] ['label'] = copy.copy(attr_dict_lab)
                    AtribDynLab[Nodes.keys().index(target)] ['weight'] = copy.copy(attr_dict_weight)

                G1.add_edge(Nodes.keys().index(source), Nodes.keys().index(target), {'weight' : Pondere[(source, target)]['weight']})
                G2.add_edge(Nodes.keys().index(source), Nodes.keys().index(target), {'weight' : Pondere[(source, target)]['weight']})
                AtribDyn=OrderedDict()
        Atrib = OrderedDict()
        for noeud in AtribDynLab.keys():
            AtribDyn[noeud] = dict()
            AtribDyn[noeud]['id']= AtribDynLab.keys().index(noeud)
            AtribDyn[noeud]['start']= AtribDynLab[noeud]['label']['start']
            AtribDyn[noeud]['end']= AtribDynLab[noeud]['label']['end']
       #     AtribDyn[noeud]['label']= AtribDynLab[noeud]['label']['label']
            Atrib[noeud] = AtribDynLab[noeud]['label']['label']
            
#        nx.set_node_attributes(G1, 'id' , AtribDyn)
        WeightDynIndexed = dict()
        for src, tgt in WeightDyn.keys():
            WeightDynIndexed[(Nodes.keys().index(src), Nodes.keys().index(tgt))] = WeightDyn[(src, tgt)]['weight']
            
            
#        nx.set_node_attributes(G1,  'id', AtribDyn)
#        nx.set_node_attributes(G1,  'label', Atrib)
#        nx.set_node_attributes(G2,  'label', Atrib)
#        AtribDyn=dict()
        Atrib = dict()
        for noeud in AtribDynLab.keys():
            AtribDyn[noeud] = AtribDynLab[noeud]['weight']
            Atrib [noeud] = AtribDynLab[noeud]['weight']['value']
        nx.set_node_attributes(G1,  'id', AtribDyn)
        nx.set_node_attributes(G2,  'weight', Atrib)
        
        for G in [G1]:#, G2]:
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
            for k in G.nodes():
                G.node[k]['label'] =  Nodes.keys()[k]
                G.node[k]['category'] = Nodes[Nodes.keys()[k]]['category']
                if G.node[k]['category'] == 'applicant-nice':
                     G.node[k]['category'] = 'applicant'
                     G.node[k]['url'] = UrlApplicantBuild(Nodes.keys()[k])[0]
                elif G.node[k]['category'] == 'IPCR1' or G.node[k]['category'] == 'IPCR3' or G.node[k]['category'] == 'IPCR4' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'IPCR7' or G.node[k]['category'] == 'CPC':
                     G.node[k]['url'] = UrlIPCRBuild(Nodes.keys()[k])[0]
                elif G.node[k]['category'] == 'inventor-nice':
                    G.node[k]['category'] = 'inventor'
                    G.node[k]['url'] = UrlInventorBuild(Nodes.keys()[k])[0]
                elif G.node[k]['category'] == 'label':
                    G.node[k]['url'] =UrlPatent(Nodes.keys()[k])[0]
                    #G.node[k]['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&locale=en_EP&DB=EPODOC&PA='+quote('"'+ComputeTempoNom(Nodes.keys()[k])+'"')
                MaxWeight = -1
                tutu = [G.node[tt]['degree'] for tt in G.nodes()]
                Maxdegs = max(tutu)
                zoom = len(G)/Maxdegs # should be function of network...
                #pos = nx.spring_layout(G, dim=2, k=2, scale =1)
                if G == G1:
                    G.node[k]['weight']={'value' : len(Nodes[Nodes.keys()[k]]['date']), 
                        'start' : Nodes[Nodes.keys()[k]]['date'][0].isoformat(),
                        'end': datetime.date(Nodes[Nodes.keys()[k]]['date'][0].year + 20,Nodes[Nodes.keys()[k]]['date'][0].month, Nodes[Nodes.keys()[k]]['date'][0].day ).isoformat()
                                        }
                    pos = nx.spring_layout(G, dim=3, k=2, scale =1, iterations = 50)
                    
                if G==G2:
                    argu='-Goverlap="9:prism" -Gsize="1000,800" -GLT=550 -GKsep='+str(zoom)
                    #pos=nx.graphviz_layout(G,prog='sfdp', args = argu )
                    pos = nx.graphviz_layout(G,prog='dot', args = argu )

        #                    pos = nx.spring_layout(G, dim=2, k=2, scale =1, iterations = 5000) 
                    
        #                newCoord = project_points(pos[k][0], pos[k][1], pos[k][2], 0, 0, 1)
        #                Visu['position']= {'x':newCoord[0][0], 'y':newCoord[0][1], 'z':0}
        #                norme = np.linalg.norm(pos[k])
                cmpe = cmap_discretize(matplotlib.cm.jet, int(size))
        #        x = resize(arange(100), (5,100))
                if size>6:
                    colors = [cmpe(i*1024/(int(size))) for i in range(int(size))]      
                else:
                    colors = [[1,0,0], [0,1,0], [0,0,1], [1,1,0], [0,1,1], [1,0,1]]
                    
                if len(pos[k])>2:
                    z = pos[k][2] *400
                    factx, facty = 500, 400
                    posx, posy = -250, -200
                else:
                    z = 0.0
                    factx, facty = 1, 1
                    posx, posy = 0, 0
                Visu = dict()
                count = mixNet.index(Nodes[Nodes.keys()[k]]['category']) #one color for one kind of node
                Visu['position']= {'x':((pos[k][0])*facty+posx), 'y':((pos[k][1])*facty+posy), 'z':z}
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
        
#        nx.set_edge_attributes(G1, 'weight', WeightDynIndexed)

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
        			<attribute id="4" title="time" type="integer" />
        			</attributes>
            <attributes class="node" mode="static">
        	<attribute id="5" title="betweeness" type="double" />
        	<attribute id="1" title="degree_cent" type="float" />
        
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

        data = data.replace('value="{', '')
        data = data.replace("'start': ", "start=")
        data = data.replace("'end': ", "end=")
        data = data.replace("'value': ", 'value=')
        data = data.replace("',", "'")        
        data = data.replace("}", "")   
        for lig in data.split('\n'):
            if lig.count('<nodes>'):
                ecrit = True
            if ecrit:
                if lig.count('<node')>0:
                    
                    lig = lig.replace('id="{', '')
                    lig = lig.replace("'id': ", 'id="')
                if lig.count('attvalue')>0 and lig.count('for="4"')>0:
                    lig = lig.replace('value=', 'value="')
                if lig.count('<edge')>0 and lig.count('<edges>')==0:
                    try:
                        lig = lig.replace('source="{',"")
                        lig = lig.replace("'id': ", 'source="', 1)
                        ind1 = lig.index('target="{start=')
                        ind2 = lig[ind1:].index("'id': ")+ind1
                        lig = lig.replace(lig[ind1:ind2+6], 'target="')
                    except:
                        pass
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
            print "Dynamic Gexf network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf+network+'.gexf'
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
        
            </attributes>
        	<attributes class="edge" mode="dynamic">
              <attribute id="6" title="time" type="integer" />
            </attributes>
        	<attributes class="node" mode="dynamic">
        			<attribute id="4" title="weight" type="integer" />
        			</attributes>
            <attributes class="node" mode="static">
        	<attribute id="5" title="betweeness" type="double" />
        	<attribute id="2" title="degree_cent" type="float" />
        
             <attribute id="1" title="degree" type="integer" />
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
        with open("config.js", 'r') as fic:
            with open(ResultPathGephi + '\\'+FicRezo.replace('.gexf','') +'Conf.js', 'w') as ficRes:
                fichierJS = fic.read()
                ficRes.write(fichierJS.replace('FicRezo', FicRezo))
        #
