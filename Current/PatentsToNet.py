# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:41:21 2014

@author: dreymond
"""
IPCRCodes = {'A':'HUMAN NECESSITIES', 'B':'PERFORMING OPERATIONS; TRANSPORTING', 'C':'CHEMISTRY; METALLURGY',
'D':'TEXTILES; PAPER', 'E':'FIXED CONSTRUCTIONS', 'F':'MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING',
'G':' PHYSICS', 'H':'ELECTRICITY'}
Status = ['A', 'B', 'C', 'U', 'Y', 'Z', 'M', 'P', 'S', 'L', 'R', 'T', 'W', 'E', 'F', 'G', 'H', 'I', 'N', 'X']
#    A – First publication level
#    B – Second publication level
#    C – Third publication level
#Group 2 – Use for utility model documents having a numbering series other than the documents of Group 1:
#    U – First publication level
#    Y – Second publication level
#    Z – Third publication level
#Group 3 – Use for special series of patent documents as specified below:
#    M – Medicament patent documents (e.g., documents previously published by FR)
#    P – Plant patent documents (e.g., published by US)
#    S – Design patent documents (e.g., published by US)
#Group 4 – Use for special types of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 3, above, as specified below:
#    L – Documents, not covered by the letter code W, relating to patent documents and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
#    R – Separately published search reports
#    T – Publication, for information or other purposes, of the translation of the whole or part of a patent document already published by another office or organization
#    W – Documents relating to utility model documents falling in Group 2 and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
#Group 5 – Use for series of patent documents not covered by Groups 1 to 4, above:
#    E – First publication level
#    F – Second publication level
#    G – Third publication level
#Group 6 – Use for series of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 5, above, according to the special requirements of each industrial property office:
#    H
#    I
#Group 7 – Other (see paragraph 2, above):
#    N – Non-patent literature documents
#    X ]
import networkx as nx

#from networkx_functs import *
import pickle
from OPS2NetUtils import *

DureeBrevet = 25
SchemeVersion = '20140101' #for the url to the classification scheme
import os, sys, datetime, urllib



def quote(string):
    string=string.replace(u'\x80', '')
    string=string.replace(u'\x82', '')

    return urllib.quote(string.replace(u'\u2002', ''), safe='/\\())')

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

def change(NomDeNoeud):
    if NomDeNoeud == 'classification':
        return 'IPCR'
    if NomDeNoeud == 'pays':
        return 'country'
    if NomDeNoeud == 'inventeur':
        return 'inventor'
    return NomDeNoeud


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

if ficOk:
    #TableCor = dict()
    dynamic = True # spécifie la date des brevets
    
    ListeBrevet = NettoiePays(ListeBrevet)   
    ListeBrevet = NettoieProprietes(ListeBrevet, "inventeur")
    ListeBrevet = NettoieProprietes(ListeBrevet, "applicant")
    lstTemp = []
    for Brev in ListeBrevet:
        if type(Brev['classification']) == type ([]):
            temp = dict()
            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
                temp[key] = []
            for classif in Brev['classification']:
                temp['classification'].append(classif.replace(' ', '', classif.count(' ')))
                temp['IPCR1'].append(classif[0])
                if len(classif) > 2:
                    temp['IPCR3'].append(classif[0:3])
                else:
                    temp['IPCR3'].append('')
                if len(classif) > 4:
                    temp['IPCR4'].append(classif[0:4])
                else:
                    temp['IPCR4'].append('')
                if classif.count('/') > 0:
                    temp['IPCR7'].append(classif.split('/')[0])
                else:
                    temp['IPCR7'].append('')
                temp['IPCR11'].append(classif[0:len(classif)-2])
                
                temp['status'].append(classif[len(classif)-2:])
            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:    
                if type(temp[key]) == type([]):
                    Brev[key] = list(set(temp[key]))
                else:
                    Brev[key] = temp[key]
                        
                    
        elif Brev['classification'] is not None:
            Brev['classification'] = Brev['classification'].replace(' ', '', Brev['classification'].count(' '))
                        
            Brev['IPCR1']=(Brev['classification'][0])
            if len(Brev['classification']) > 2:
                Brev['IPCR3']=(Brev['classification'][0:3])
            else:
                Brev['IPCR3'] = ''
            if len(Brev['classification']) > 4:            
                Brev['IPCR4']=(Brev['classification'][0:4])
            else:
                Brev['IPCR4'] = ''
            if Brev['classification'].count('/') >0:
                Brev['IPCR7']=(Brev['classification'].split('/')[0])
            else:
                Brev['IPCR7'] = ''
            Brev['IPCR11']=(Brev['classification'][0:len(Brev['classification'])-2])
            Brev['status']=(Brev['classification'][len(Brev['classification'])-1:])
            if Brev['status'] not in Status:
                Brev['status'] = 'N/A'
        else:
            for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
                Brev[ipc] = 'N/A'
            
        lstTemp.append(Brev)
    ListeBrevet = lstTemp
    
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
    
    G = nx.DiGraph() 
    
    appariement = dict() # dictionnaires des appariements selon les propriétés des brevets
    # sera envoyé en paramètres à la fonction GenereReseau3
    # un/comment hereafter for desired network creation
#    appariement['Nation'] = ['label', 'pays']
#    appariement['inventeur-label'] = ['inventeur', 'label']
#    appariement['applicant-label'] = ['applicant', 'label']
#    appariement['inventeur-inventeur'] = ['inventeur', 'inventeur']
#    appariement['applicant-applicant'] = ['applicant', 'applicant']
#    appariement['inventeur-applicant'] = ['inventeur', 'applicant']
#    appariement['label-classification'] = ['label', 'classification']
#    appariement[''] = ['','']
#    appariement[''] = ['','']
    
    #appariement['IPCR-IPCR'] = ['classification', 'classification']
    lstCrit= ['inventeur', 'label', 'applicant', 'pays', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']
    for i in lstCrit:
        for j in lstCrit:
            
            appariement[change(i)+'-'+change(j)] = [i,j]
            
    #G= nx.DiGraph()
    for Brev in ListeBrevet:
        if 'date' not in Brev.keys():
            print Brev
            Brev['date'] = datetime.date(3000, 1, 1)
            
    G, reseau = GenereReseaux3(G, ListeNoeuds, ListeBrevet, appariement, dynamic)
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
    for noeud in ListeNoeuds:
    
        if noeud is not None:
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
                attr['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN='+quote(noeud)+'&locale=en_EP&DB=EPODOC'
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
                attr['url'] ='http://worldwide.espacenet.com/searchResuldengue-grupos.jsonts?compact=false&ST=advanced&locale=en_EP&DB=EPODOC&PA='+quote(noeud)
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
                attr['url'] =  'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
        
            elif noeud in IPCR3:
                attr['label'] = 'IPCR3'
                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
            elif noeud in IPCR4:
                attr['label'] = 'IPCR4'
                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud

            elif noeud in IPCR11:
                attr['label'] = 'IPCR11'
                attr['url'] = ''
            elif noeud in status:
                attr['label'] = 'status'
                
            if noeud in ListeNoeuds:
                G.add_node(ListeNoeuds.index(noeud))
    
                G.node[ListeNoeuds.index(noeud)]['label'] = noeud
                
                G.node[ListeNoeuds.index(noeud)]['category'] = attr['label']
                G.node[ListeNoeuds.index(noeud)]['url'] = attr['url']
                G.node[ListeNoeuds.index(noeud)]['weight'] = str(reseau).count(noeud)
                G.node[ListeNoeuds.index(noeud)]['start'] = min(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
                G.node[ListeNoeuds.index(noeud)]['end'] = max(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
                if dateMini > G.node[ListeNoeuds.index(noeud)]['start']:
                    dateMini = G.node[ListeNoeuds.index(noeud)]['start']
                if dateMax < G.node[ListeNoeuds.index(noeud)]['end']:
                    dateMax = G.node[ListeNoeuds.index(noeud)]['end']
                
                if len(G.node[ListeNoeuds.index(noeud)]['time']) >1:
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
                                    lsttemp.append(G.node[ListeNoeuds.index(noeud)]['time'][nb])
                                    cpt+=1
                    G.node[ListeNoeuds.index(noeud)]['time'] = lsttemp         
                G.node[ListeNoeuds.index(noeud)]['deb'] = G.node[ListeNoeuds.index(noeud)]['start']
                G.node[ListeNoeuds.index(noeud)]['fin']= dateMax#G.node[ListeNoeuds.index(noeud)]['end']
                G.node[ListeNoeuds.index(noeud)]['val'] = sum([u[0] for u in G.node[ListeNoeuds.index(noeud)]['time']])
                del(G.node[ListeNoeuds.index(noeud)]['end'])
                del(G.node[ListeNoeuds.index(noeud)]['start'])
                del(G.node[ListeNoeuds.index(noeud)]['weight'])               
                if noeud not in IPCR1:
                    pass
                else:
                    G.node[ListeNoeuds.index(noeud)]['label'] = noeud + '-' +attr['name']
                #G.node[ListeNoeuds.index(noeud)]['end'] = ExtraitMinDate(G.node[ListeNoeuds.index(noeud)]) + DureeBrevet
                #G.node[ListeNoeuds.index(noeud)]['start'] = 
            G.graph['defaultedgetype'] = "directed"
            G.graph['timeformat'] = "date"
            G.graph['mode'] = "dynamic"
            G.graph['start'] = dateMini
            G.graph['end'] = dateMax

            
    nx.write_gexf(G, ResultPathGephi+'\\'+ndf + ".gexf", version='1.2draft')
    fic = open(ResultPathGephi+'\\'+ndf+'.gexf', 'r')
    #
    # Next is a hack to correct the bad writing of the header of the gexf file
    # with dynamics properties
    fictemp=open(ResultPathGephi+'\\'+"Good"+ndf+'.gexf', 'w')
    fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">
  <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
    <attributes class="edge" mode="static">
      <attribute id="6" title="deb" type="string" />
      <attribute id="7" title="fin" type="string" />
      <attribute id="8" title="rel" type="string" />
	</attributes>
	<attributes class="edge" mode="dynamic">
      <attribute id="9" title="time" type="integer" />
    </attributes>
    <attributes class="node" mode="static">
      <attribute id="0" title="category" type="string" />
      <attribute id="1" title="val" type="integer" />
      <attribute id="3" title="url" type="string" />
      <attribute id="4" title="deb" type="string" />
      <attribute id="5" title="fin" type="string" />
    </attributes>
	<attributes class="node" mode="dynamic">
		<attribute id="2" title="time" type="integer" />
	</attributes>
""")
    ecrit  =False
    for lig in fic.readlines():
        if lig.count('<nodes>'):
            ecrit = True
        if ecrit:
            fictemp.write(lig)
    fictemp.close()
    fic.close()
    os.remove(ResultPathGephi+'\\'+ndf+'.gexf')
    
    os.rename(ResultPathGephi+'\\'+"Good"+ndf+'.gexf', ResultPathGephi+'\\'+ndf+'.gexf')
    print "Network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf + ".gexf"