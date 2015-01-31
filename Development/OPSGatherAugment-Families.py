# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
After loading patent list (created from 
OPSGather-BiblioPatent), the script will proceed a check for each patent
if it is orphan or has a family. In the last case, family patents are added to
the initial list (may be some are already in it), and a hierarchic within
the priority patent (selected as the oldest representative) and its brothers is created.  
"""


#import networkx as nx

#from networkx_functs import *
import pickle
from OPS2NetUtils2 import *
from Ops2 import *

import epo_ops, os

global key
global secret

# put your credential from epo client in this file...

fic = open('..//cles-epo.txt', 'r')
key, secret = fic.read().split(',')
fic.close()

os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme
import sys, datetime


ListeBrevet = []
#ouverture fichier de travail
with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()

ResultPath = '..//DONNEES//PatentBiblios'
ResultPathFamilies = '..//DONNEES//PatentBiblios'
temporPath = '..//DONNEES//tempo'

try:
    os.makedirs(temporPath)
except:
    pass
try:
    fic = open(ResultPath+ '//' + ndf, 'r')
    print "loading data file ", ndf+' from ', ResultPath, " directory."
    ListeBrevet = pickle.load(fic)
    fic.close()
    
    print len(ListeBrevet), " patents loaded from file."
    print "Augmenting list with families."
    ficOk = True
except:
    print "file ", ResultPath +"/"+ndf,"  missing."
    ficOk = False

ndf2 = "Complete"+ndf


#import requests, time, pprint
def GetFamilly(client, brev):
    lstres = []
    comptExcept = 0
    
#    try:
#        url ='http://ops.epo.org/3.1/rest-services/family/publication/docdb/' +brev['label'] +'/biblio'
#        
#        data = requests.get(url, headers = headers)
    try:
        data = client.family('publication', epo_ops.models.Epodoc(brev['label']), 'biblio')
        data = data.json()
        dico = data[u'ops:world-patent-data'][u'ops:patent-family'][u'ops:family-member']
        #PatentDataFam[brev['label']] = dict()
        if type(dico) == type(dict()):
            dico=[dico]
        cpt = 1
        for donnee in dico:
            Go =True
            Brevet=dict(dict(dict(dict())))
            Brevet[u'ops:world-patent-data'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'] = donnee
            PatentData = dict()
            Req = Brevet
               
            try:
                PatentData['label'] = donnee[u'exchange-document'][u'bibliographic-data'][u'publication-reference'][u'document-id'][1][u'doc-number'][u'$']
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
                
                PatentData['portee'] = ExtraitKind(Req)
                
                PatentData['classification'] = ExtraitIPCR2(Req)
                print "Level :", PatentData['portee']
                print "Country:", PatentData['pays'] 
                
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
                    PatentData['citations'] = 0
                print " *********************************   "
                
                #if cpt == 1:#not the first one !!!!
                try:
                    if donnee[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
                        PatentData['priority-active-indicator'] = 1
                except:
                    PatentData['priority-active-indicator'] = 0
                     ## should check what is "active indicator" for patent
                try:
                    if donnee[u'application-reference'][u'@is-representative'] == u'YES':
                        PatentData['representative'] = 1                            
#                            PatentData['representative'] = True
                except:
                    PatentData['representative'] = 0
                        # should check what is reprensentativeness for patent
                    
                                     
                
                PatentData['family lenght'] = len(dico)
                cpt += 1
                if None not in PatentData.values():
                    lstres.append(PatentData)
                   
#    except:
       # lstres.append(brev)
#        comptExcept += 1
    #first representative selection
        datemin = datetime.date(3000, 1, 1)
        
        for brevet in lstres:
            if brevet.has_key('representative'):
                if brevet['date'] < datemin:
                    datemin = brevet['date']
                    prior = brevet['label']
        if 'prior' not in locals():
            prior = brev['label']
        for brevet in lstres:
            brevet['prior'] = prior
        print "exceptions ", comptExcept
        return lstres
    except:
        print "nothing found for ", brev
        print "ignoring"
        return None
	####
# Familly check

try:
    DoneLstBrev = open(temporPath+'//DoneTempo'+ ndf, 'r')
    Done = pickle.load(DoneLstBrev)
except:
    Done = []
if len(Done) > 1:
    tempoList = []
    ndfLstBrev = open(ResultPathFamilies+'//Families'+ ndf, 'r')
    ListeBrevetAug = pickle.load(ndfLstBrev)
    print len(ListeBrevetAug), " patents loaded from augmented list"
    print len(Done), ' patents treated yet... doing others : ', len(ListeBrevet) - len(Done)
    for k in ListeBrevet:
        if k not in Done:
            tempoList.append(k)
    ListeBrevet = tempoList
else: 
    ListeBrevetAug = []
if ficOk:
    registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
    registered_client.accept_type = 'application/json'
    for Brev in ListeBrevet:
        if Brev is not None and Brev != '' and Brev not in Done:
            temp = GetFamilly(registered_client, Brev)
            if temp is not None:
                for u in temp:
                    if u not in ListeBrevetAug and u != '':
                        ListeBrevetAug.append(u)
#            time.sleep(7)
        Done.append(Brev)
        ndfLstBrev = open(ResultPathFamilies+'//Families'+ ndf, 'w')
        DoneLstBrev = open(temporPath+'//DoneTempo'+ ndf, 'w')
        pickle.dump(ListeBrevetAug, ndfLstBrev)
        pickle.dump(Done, DoneLstBrev)

print "before", len(ListeBrevet)
print "now", len(ListeBrevetAug)

#####



print len(ListeBrevetAug), ' patents found and saved in file: '+ ResultPathFamilies+'//Families'+ ndf
print "Formating results"
os.system("FormateExportFamilies.exe Families"+ndf)