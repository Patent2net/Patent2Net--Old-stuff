# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:41:21 2014

@author: dreymond
"""

import networkx as nx

#from networkx_functs import *
import pickle
from OPS2NetUtils import *

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

def change(i):
    if i == 'classification':
        return 'IPCR'
    if i == 'pays':
        return 'country'
    if i == 'inventeur':
        return 'inventor'
    return i


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
                        
                    
        else:
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
            Brev['status']=(Brev['classification'][len(Brev['classification'])-2:])
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
    
    attr = dict() # dictionnaire des attributs des liens
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
                attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=IN:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=38&viewOption=All'
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
                attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=PA:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=123897&viewOption=All'
            elif noeud in IPCR1:
                attr['label'] = 'IPCR1'
                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud

            elif noeud in IPCR7:
                attr['label'] = 'IPCR7'
                attr['url'] = '' 
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
                
                
            G.add_node(ListeNoeuds.index(noeud))
            G.node[ListeNoeuds.index(noeud)]['label'] = noeud
            G.node[ListeNoeuds.index(noeud)]['category'] = attr['label']
            G.node[ListeNoeuds.index(noeud)]['url'] = attr['url']
            G.node[ListeNoeuds.index(noeud)]['weight'] = str(reseau).count(noeud)
            
    nx.write_gexf(G, ResultPathGephi+'\\'+ndf + ".gexf")
    

    print "Network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf + ".gexf"