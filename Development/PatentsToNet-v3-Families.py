# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
Same as Patent2NetV3 but, after loading patent list (created from 
OPSGather-BiblioPatent), the script will proceed a check for each patent
if it is orphan or has a family. In the last case, family patents are added to
the initial list (may be some are already in it), and a hierarchic within
the priority patent and its brothers is created.  
"""


import networkx as nx

#from networkx_functs import *
import pickle
from OPS2NetUtils2 import *
from Ops2 import *

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
ResultPathFamilies = 'FamilyPatents'



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

ndf2 = "Complete"+ndf


import requests, time, pprint
def GetFamilly(brev):
    lstres = []
    comptExcept = 0
    
    try:
        url ='http://ops.epo.org/3.1/rest-services/family/publication/docdb/' +brev['label'] +'/biblio'
        headers = {'Accept': 'application/json',}
        data = requests.get(url, headers = headers)
        time.sleep(6)
        data = data.json()
        dico = data[u'ops:world-patent-data'][u'ops:patent-family'][u'ops:family-member']
        #PatentDataFam[brev['label']] = dict()
        if type(dico) == type(dict()):
            dico=[dico]
        for donnee in dico:
            Go =True
            Brevet=dict(dict(dict(dict())))
            Brevet[u'ops:world-patent-data'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'] = donnee
            PatentData = dict()
            Req = Brevet
            cpt = 1   
            try:
                PatentData['label'] = donnee[u'exchange-document'][u'bibliographic-data'][u'publication-reference'][u'document-id'][1][u'doc-number']
            except:
                try:
                    PatentData['label'] = donnee[u'publication-reference'][u'document-id'][1][u'doc-number']['$']
                except:
                    print "no label ?"
                    Go = False
                print pprint.pprint(donnee)
            if Go:
                #PatentDataFam[PatentData['label']] = dict()
                PatentData['titre'] = Clean(ExtraitTitleEn(Req))                  
                print "Patent title(s)", PatentData['titre']
              
                PatentData['inventeur'] = Clean(ExtraitParties(Req, 'inventor', 'epodoc'))
                print "Inventors : ",  PatentData['inventeur']
                PatentData['applicant'] = Clean(ExtraitParties(Req, 'applicant','epodoc'))
                print "Applicants : ", PatentData['applicant']
                PatentData['pays'] = ExtraitCountry(Req)
                print "Country:", PatentData['pays'] 
                PatentData['portee'] = ExtraitKind(Req)
                print "Level :", PatentData['portee']
                PatentData['classification'] = ExtraitIPCR2(Req)
                    
                if PatentData["classification"] is not None:
                    if type(PatentData['classification']) == type ([]):
                        temp = []
                        for classif in PatentData['classification']:
                            temp.append(classif.replace(' ', '', classif.count(' ')))
                        PatentData['classification'] = []
                        for ipc in temp:
                            PatentData['classification'].append(ipc)
        #                temp = []                
        #                for ipcr in PatentData['classification']:
        #                    temp.append(ipcr[0:4])
        #                PatentData["ClassifReduite"] = list(set(temp))
                    else:
                        PatentData['classification'] = PatentData['classification'].replace(' ', '', PatentData['classification'].count(' '))
                       #PatentData["ClassifReduite"] = PatentData['classification'][0:4]
                    
                else:
                    PatentData["ClassifReduite"] = None
                print "Classification (not always) IPCR : ", PatentData['classification']
                #print "Classification Reduced: ", PatentData['ClassifReduite']
                date = ExtractionDate(Req) #priority claim first date time
                if date is not None:
                    
                    PatentData['date'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
                    print "patent date", PatentData['date']
                else:
                    PatentData['date'] = datetime.date(datetime.date.today().year+2, 1, 1)
                try:
                    PatentData['citations'] = len(donnee[u'exchange-document'][u'bibliographic-data'][u'references-cited']['citation'])
                except:
                    pass
                print " *********************************   "
                
                if cpt == 1:
                    try:
                        if donnee[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
                            PatentData['priority-active-indicator'] = 1
                    except:
                        PatentData['priority-active-indicator'] = 0
                        pass ## should check what is "active indicator" for patent
                    try:
                        if donnee[u'application-reference'][u'@is-representative'] == u'YES':
                            PatentData['representative'] = 1                            
#                            PatentData['representative'] = True
                    except:
                        PatentData['representative'] = 0
                        pass # should check what is reprensentativeness for patent
                    PatentData['prior'] = PatentData['label']
                    prior = PatentData['label']
                    PatentData['family lenght'] = len(dico)
                else:
                    try:
                        if donnee[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
                            print ' pas du tout bingo'
                    except:
                        pass
                    try:
                        if donnee[u'application-reference'][u'@is-representative'] == u'YES':
                            print ' pas du tout bingo 2'
                    except:
                        pass
                    PatentData['prior'] = prior 
                cpt += 1
                if None not in PatentData.values():
                    lstres.append(PatentData)
                   
    except:
        lstres.append(brev)
        comptExcept += 1
    print "exceptions ", comptExcept
    return lstres
####
# Familly check
ListeBrevetAug = []
if ficOk:
    for Brev in ListeBrevet:
        if Brev is not None and Brev != '':
            temp = GetFamilly(Brev)
            for u in temp:
                if u not in ListeBrevetAug:
                    ListeBrevetAug.append(u)
            time.sleep(7)

print "before", len(ListeBrevet)
print "now", len(ListeBrevetAug)

#####

ndfLstBrev = open(ResultPathFamilies+'//Families'+ ndf, 'w')

pickle.dump(ListeBrevetAug, ndfLstBrev)

print len(ListeBrevetAug), ' patents found and saved in file: '+ ResultPathFamilies+'//Families'+ ndf
