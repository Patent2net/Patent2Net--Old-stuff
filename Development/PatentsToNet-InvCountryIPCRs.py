# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
"""


import networkx as nx

#from networkx_functs import *
import pickle
from OPS2NetUtils2 import *

DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme
import os, sys, datetime


ListeBrevet = []
#ouverture fichier de travail
ndf = sys.argv[1]
if not ndf.endswith(".dump"):
    print "Incorrect file"
    print "GatherOPS nom_de_fichier.dump keyword OPERATOR keyword..."


ResultPath = 'BiblioPatents'
ResultPathGephi = 'GephiFiles'

if os.listdir('.').count(ResultPathGephi) ==0:
    os.mkdir(ResultPathGephi)

try:
    fic = open(ResultPath+ '//' + ndf, 'r')
    print "loading data file ", ndf+' from ', ResultPath, " directory."
    ListeBrevet = pickle.load(fic)
    fic.close()
    
    print len(ListeBrevet), " patents loaded from file."
    print "Generating network."
    ficOk = True
except:
    print "file ", ResultPath +"/"+ndf,"  missing."
    ficOk = False

inventeur = dict()
applicant = dict()

if ficOk:
    #TableCor = dict()
    dynamic = True # spécifie la date des brevets
    
#    ListeBrevet = NettoiePays(ListeBrevet)   
#    ListeBrevet = NettoieProprietes(ListeBrevet, "inventeur")
#    ListeBrevet = NettoieProprietes(ListeBrevet, "applicant")
    lstTemp = []
    listeDates = []
    for Brev in ListeBrevet:
        listeDates.append(Brev['date'])
        for classif in ExtractClassification(Brev['classification']):
            if type(classif) == type(dict()):
                for cle in classif.keys():
                    Brev[cle] = classif[cle]
            else:
                print classif
                    
        memo = Brev['applicant']
        # remember applicant original writing form to reuse in the url property of the node
        # hope that copied list is in the sameorder than the original... else there might be some mixing data 
        Brev['applicant'] = Formate(Brev['applicant'], Brev['pays'])
        if type(Brev['applicant']) == type(list()):
            for inv in range(len(Brev['applicant'])):
                applicant[Brev['applicant'][inv]] = Formate2(memo[inv], Brev['pays'])
        else:
            applicant[Brev['applicant']] = Formate2(memo, Brev['pays'])
        
        # remember inventor original writing form to reuse in the url property of the node
        memo = Brev['inventeur']
        Brev['inventeur'] = Formate(Brev['inventeur'], Brev['pays'])
        if type(Brev['inventeur']) == type(list()):
            for inv in range(len(Brev['inventeur'])):
                inventeur[Brev['inventeur'][inv]] = Formate2(memo[inv], Brev['pays'])
        else:
            inventeur[Brev['inventeur']] = Formate2(memo, Brev['pays'])
        
        lstTemp.append(Brev)
    ListeBrevet = lstTemp
    Norm = dict()
    for Brev in ListeBrevet:
        norm = 0
        for cle in Brev.keys():
            if type(Brev[cle]) == type([]):
                norm += len(Brev[cle])
            else:
                norm += 1
        Brev['Norm'] = norm
        Norm[Brev['label']] = norm
        
    Pays = set([(u) for u in GenereListeSansDate(ListeBrevet, 'pays')])
    Inventeurs = set([(u) for u in GenereListeSansDate(ListeBrevet, 'inventeur')])
    LabelBrevet = set([(u) for u in GenereListeSansDate(ListeBrevet, 'label')])
    Applicant = set([(u) for u in GenereListeSansDate(ListeBrevet, 'applicant')])
    Classification = set([(u) for u in GenereListeSansDate(ListeBrevet, 'classification')])
    IPCR1 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR1')])
    IPCR3 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR3')])
    IPCR4 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR4')])
    IPCR7 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR7')])
    IPCR11 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR11')])
    status = set([(u) for u in GenereListeSansDate(ListeBrevet, 'status')])
    listelistes = []
    listelistes.append(Pays)
    listelistes.append(Inventeurs)
    listelistes.append(LabelBrevet)
    listelistes.append(Applicant)
    #listelistes.append(Classification)
    listelistes.append(IPCR1)
    listelistes.append(IPCR3)
    listelistes.append(IPCR4)
    listelistes.append(IPCR7)
    listelistes.append(IPCR11)
    listelistes.append(status)
    
    def ExtraitMinDate(noeud):
        if noeud.has_key('time'):
            for i in noeud['time']:
                mini = 3000
                if i[1] < mini:
                    mini = i[1]
        else:
            mini = dateDujour
        return mini
    
    
    def getClassif(noeud, listeBrevet):
        for Brev in listeBrevet:
            if Brev['label'] == noeud:
                return Brev['classification']
        return 'NA'
    
    ListeNoeuds =[]
    for liste in listelistes:
        ListeNoeuds += [u for u in liste if u not in ListeNoeuds]
    try:
        ListeNoeuds.remove('N/A')
        ListeNoeuds.remove('')
    except:
        pass
    G = nx.DiGraph() 
    
    appariement = dict() # dictionnaires des appariements selon les propriétés des brevets
    # sera envoyé en paramètres à la fonction GenereReseau3
    #list set of biblio contents
    #uncomment for the whole network
    #lstCrit= ['inventeur', 'label', 'applicant', 'pays', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']
#    for i in lstCrit:
#        for j in lstCrit:
#            appariement[change(i)+'-'+change(j)] = [i,j]
#    # un/comment hereafter for desired network creation
#    
    lstCrit = ['inventeur', 'applicant']
    lstCat = ['IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11']  
    for i in lstCat:
        for j in lstCat:
			if i==j: # only same technology level networks
				appariement[change(i)+'-'+change(j)] = [i,j]
        for k in lstCrit:
			appariement[change(i)+'-'+change(k)] = [i,k]
	for i in lstCrit:
		for j in lstCrit:
			appariement[change(i)+'-'+change(j)] = [i,j]
			
   #appariement['Nation'] = ['label', 'pays']
#    appariement['inventeur-label'] = ['inventeur', 'label']
#    appariement['applicant-label'] = ['applicant', 'label']
#    appariement['inventor-inventeur'] = ['inventeur', 'inventeur']
#    appariement['inventor-country'] = ['inventeur', 'pays']
    #appariement['inventeur-IPCR4'] = ['inventeur','IPCR4']
#    appariement['IPCR4-IPCR4'] = ['IPCR4','IPCR4']
#    appariement['IPCR1-IPCR4'] = ['IPCR1','IPCR4']
#    appariement['IPCR4-IPCR1'] = ['IPCR4','IPCR1']
#    appariement['IPCR1-IPCR1'] = ['IPCR1','IPCR1']
#    appariement['IPCR1-IPCR3'] = ['IPCR1','IPCR3']
#    appariement['IPCR3-IPCR3'] = ['IPCR3','IPCR3']
#    
#    appariement['inventeur-IPCR1'] = ['inventeur','IPCR1']
#    appariement['inventeur-IPCR1'] = ['inventeur','IPCR4']
   # appariement['label-inventeur'] = ['label', 'inventeur']
#    appariement['applicant-applicant'] = ['applicant', 'applicant']
#    appariement['inventeur-applicant'] = ['inventeur', 'applicant']
#    appariement['label-classification'] = ['label', 'classification']
#    appariement[''] = ['','']
#    appariement[''] = ['','']
    
    #appariement['IPCR-IPCR'] = ['classification', 'classification']    
#    appariement['inventor-inventor'] = ['inventeur','inventeur']
#    appariement['applicant-inventor'] = ['applicant','inventeur']
#    appariement['applicant-'+change('pays')] = ['applicant','pays']
#    appariement['applicant-label'] = ['applicant','label']
#    appariement['label-IPCR1'] = ['label','IPCR1']
#    appariement['IPCR1-IPCR3'] = ['IPCR1','IPCR3']
#    appariement['IPCR3-IPCR4'] = ['IPCR3','IPCR4']
#    appariement['IPCR4-IPCR7'] = ['IPCR4','IPCR7']
#    
#    appariement['IPCR7-IPCR11'] = ['IPCR7','IPCR11']
#    appariement['applicant-IPCR1'] = ['applicant','IPCR1']
#    appariement['label-status'] = ['label','status']
#    appariement['applicant-IPCR11'] = ['applicant','IPCR11']
#    appariement['inventor-IPCR11'] = ['inventor','IPCR11']

    
        
            
    #G= nx.DiGraph()
    for Brev in ListeBrevet:
        if 'date' not in Brev.keys():
            print Brev
            Brev['date'] = datetime.date(datetime.date.today()+2, 1, 1)
            
    G, reseau, Prop = GenereReseaux3(G, ListeNoeuds, ListeBrevet, appariement, dynamic)
    #
    DateNoeud = dict()
    for lien in reseau:
        n1, n2, dat, pipo = lien
        if DateNoeud.has_key(n1):
            DateNoeud[n1].append(dat)
        else:
            DateNoeud[n1] = [dat]
        if DateNoeud.has_key(n2):
            DateNoeud[n2].append(dat)
        else:
            DateNoeud[n2] = [dat]
    
    attr = dict() # dictionnaire des attributs des liens
    import datetime
    today = datetime.datetime.now().date().isoformat()
    dateMini = today
    dateMax = datetime.datetime(1700, 1, 1).isoformat()
    
    
    liendureseau = [(u, v) for u,v,b ,z in reseau]
    LinkedNodes = []
    for k in liendureseau:
        LinkedNodes.append(k[0])
        LinkedNodes.append(k[1])
        
    for noeud in set(LinkedNodes):
    
        if noeud is not None and noeud !='':
            if noeud in Pays:
                attr['label'] = 'pays'
                attr['url'] = ''
    #            elif noeud in Classification:
    #                attr['label'] = 'IPCR'
    #                if noeud.count('/') > 0:
    #                    ind = noeud[4:].index('/')
    #                    mask = 4 - ind
    #                    mask2 = len(noeud[5+ind:len(noeud)-2])
    #                
    #                    attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]+str(0)*mask+noeud[4:4+ind]+noeud[5+ind:len(noeud)-2]+'000' + (3-mask2)*str('0')
    #                else:
    #                    attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]
            elif noeud in Inventeurs:
                
                attr['label'] = 'Inventeur'
                attr['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN='+quote('"'+inventeur[noeud]+'"')+'&locale=en_EP&DB=EPODOC'
                #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=IN:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=38&viewOption=All'
            elif noeud in LabelBrevet:
                attr['label'] = 'Brevet'
                attr['Class'] = getClassif(noeud, ListeBrevet)
                if attr['Class'] is not None:
                    attr['ReductedClass'] = getClassif(noeud, ListeBrevet)[0:4]
                    tempotemp = "http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query="+noeud+"&locale=en_EP&DB=EPODOC"
                
                    attr['url'] = tempotemp
                else:
                    attr['ReductedClass'] = ""
            elif noeud in Applicant:
                attr['label'] = 'Applicant'
                attr['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&locale=en_EP&DB=EPODOC&PA='+quote('"'+applicant[noeud]+'"')
                #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=PA:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=123897&viewOption=All'
            elif noeud in IPCR1:
                if noeud in IPCRCodes.keys():
                    attr['label'] = 'IPCR1'
                    attr['name'] = IPCRCodes[noeud]
                    attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
                else:
                    pass #node is may be a status node
            elif noeud in IPCR7:
                attr['label'] = 'IPCR7'
                attr['url'] =  'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +symbole(noeud)

            elif noeud in IPCR3:
                attr['label'] = 'IPCR3'
                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
            elif noeud in IPCR4:
                attr['label'] = 'IPCR4'
                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
    
            elif noeud in IPCR11:
                attr['label'] = 'IPCR11'
                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +symbole(noeud)

            elif noeud in status:
                attr['label'] = 'status'
            
            if noeud in ListeNoeuds:
                G.add_node(ListeNoeuds.index(noeud))
    
                G.node[ListeNoeuds.index(noeud)]['label'] = noeud
                
                G.node[ListeNoeuds.index(noeud)]['category'] = attr['label']
                G.node[ListeNoeuds.index(noeud)]['url'] = attr['url']
                G.node[ListeNoeuds.index(noeud)]['weight'] = LinkedNodes.count(noeud)
                G.node[ListeNoeuds.index(noeud)]['start'] = min(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
                G.node[ListeNoeuds.index(noeud)]['end'] = max(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
                G.node[ListeNoeuds.index(noeud)]['time'] = []
                dateNodes = [u for u in listeDates if u in set(DateNoeud[noeud])] # filtered againts patent dates
                for d in dateNodes:
                    lsttemp = (dateNodes.count(d), d, today)                        
                    #lstAppear = [u for u in Prop.keys() if u[0] == noeud or u[1] == noeud and Prop[u][0] == datenode]
#                   
#            #counting those relative to same kind of relation
#                        numAppear = len([u for u in lstAppear if Prop[u][1] == Prop[(node, ListeNode[ed[1]])][1]]) +1 #adding 1 for current occur
#               
                    
                    if lsttemp not in G.node[ListeNoeuds.index(noeud)]['time']:
                        G.node[ListeNoeuds.index(noeud)]['time'].append(lsttemp)
                    else:
                        if len(G.node[ListeNoeuds.index(noeud)]['time']) ==0:
                            G.node[ListeNoeuds.index(noeud)]['time'] = [lsttemp]
                        else:
                            pass
                    #print dat
                
                lst = [u[1] for u in G.node[ListeNoeuds.index(noeud)]['time']]
                lst.sort()
                lsttemp = []
                cpt=0
                for kk in range(len(lst)):
                    for nb in range(len(G.node[ListeNoeuds.index(noeud)]['time'])):                 
                        if G.node[ListeNoeuds.index(noeud)]['time'][nb][1] == lst[kk]:
                            if G.node[ListeNoeuds.index(noeud)]['time'][nb] not in lsttemp:
                                if cpt>0:
                                    
                                    lsttemp[cpt-1] = (lsttemp[cpt-1][0], lsttemp[cpt-1][1], G.node[ListeNoeuds.index(noeud)]['time'][nb][1] )#enddate is startdate of current datetime
                                if len(lsttemp) ==0:
                                    lsttemp.append(G.node[ListeNoeuds.index(noeud)]['time'][nb])
                                else:
                                    temporair = (G.node[ListeNoeuds.index(noeud)]['time'][nb][0] + lsttemp[len(lsttemp)-1][0],G.node[ListeNoeuds.index(noeud)]['time'][nb][1], G.node[ListeNoeuds.index(noeud)]['time'][nb][2])
                                    lsttemp.append(temporair)
                                cpt+=1
                G.node[ListeNoeuds.index(noeud)]['time'] = lsttemp 
                
                G.node[ListeNoeuds.index(noeud)]['deb'] = lst[0].isoformat()
                G.node[ListeNoeuds.index(noeud)]['fin']= today
                #G.node[ListeNoeuds.index(noeud)]['val'] = int(sum([u[0] for u in G.node[ListeNoeuds.index(noeud)]['time']]))
                del(G.node[ListeNoeuds.index(noeud)]['end'])
                del(G.node[ListeNoeuds.index(noeud)]['start'])
                #del(G.node[ListeNoeuds.index(noeud)]['weight'])               
                if noeud not in IPCR1:
                    pass
                else:
                    G.node[ListeNoeuds.index(noeud)]['label'] = noeud + '-' +attr['name']
            else:
                print "on devrait pas être là, never", noeud
                #G.node[ListeNoeuds.index(noeud)]['end'] = ExtraitMinDate(G.node[ListeNoeuds.index(noeud)]) + DureeBrevet
                #G.node[ListeNoeuds.index(noeud)]['start'] = 
    G.graph['defaultedgetype'] = "directed"
    G.graph['timeformat'] = "date"
    G.graph['mode'] = "dynamic"
    G.graph['start'] = dateMini
        
    G.graph['end'] = dateMax

            
    nx.write_gexf(G, ResultPathGephi+'\\'+ndf + "temp.gexf", version='1.2draft')
    fic = open(ResultPathGephi+'\\'+ndf+'temp.gexf', 'r')
    #
    # Next is a hack to correct the bad writing of the header of the gexf file
    # with dynamics properties
    fictemp=open(ResultPathGephi+'\\'+"Good"+ndf+'InvCountryIPCR.gexf', 'w')
    fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">
  <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
    <attributes class="edge" mode="static">
      <attribute id="6" title="NormedWeight" type="double" />
      <attribute id="8" title="deb" type="string" />
      <attribute id="9" title="fin" type="string" />
      <attribute id="10" title="rel" type="string" />
    </attributes>
	<attributes class="edge" mode="dynamic">
      <attribute id="7" title="time" type="integer" />
    </attributes>
    <attributes class="node" mode="static">
      <attribute id="0" title="category" type="string" />
      <attribute id="1" title="weight" type="integer" />
      
      <attribute id="3" title="url" type="string" />
      <attribute id="4" title="deb" type="string" />
      <attribute id="5" title="fin" type="string" />
    </attributes>
	<attributes class="node" mode="dynamic">
		<attribute id="2" title="time" type="integer" />
	</attributes>
#""")
    ecrit  =False
    for lig in fic.readlines():
        if lig.count('<nodes>'):
            ecrit = True
        if ecrit:
            fictemp.write(lig)
    fictemp.close()
    fic.close()
    os.remove(ResultPathGephi+'\\'+ndf+'temp.gexf')
    
    os.rename(ResultPathGephi+'\\'+"Good"+ndf+'InvCountryIPCR.gexf', ResultPathGephi+'\\'+ndf+'InvCountryIPCR.gexf')
    print "Network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf + "InvCountryIPCR.gexf"