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

BiblioProperties = ['publication-ref', 'priority-active-indicator', 'classification', 
u'resume', 'IPCR1', 'portee', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'label', 'IPCR11', 
'date', 'citations', 'application-ref', 'pays', u'abstract', 'titre', 'inventeur', 
'representative'] 

#from networkx_functs import *
import pickle
from OPS2NetUtils2 import *
from Ops3 import *

import epo_ops
from epo_ops.models import Docdb

global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('../../../cles-epo.txt', 'r')
key, secret = fic.read().split(',')
fic.close()

 
DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme
import os, sys, datetime


ListeBrevet = [] # LA iste de brevets
#ouverture fichier de travail
ndf = sys.argv[1]


ListPatentPath = 'PatentLists'
ResultPathBiblio = 'PatentsBiblio'
temporPath = 'tempo'
#by default, data are not gathered yet
ficOk = False


# à ce niveau de script, la liste des brevets est chargée avec des données 
# biblio qui vont être complétées
import requests, time, pprint

cptNotFound=0



def RecupAbstract(dico):
    res = dict()
    if u'@lang' in dico.keys():
        if dico[u'@lang'].count(u'fr')>0:
            res[u'resume'] = dico[u'p']
        else:
            res[u'abstract'] = dico[u'p']
        return res      
    elif u'abstract' in str(dico):
        print "where is the key? \n", dico

def PatentSearch(client, requete, deb = 1, fin = 1):
    requete = requete.replace('/', '\\')
    data = client.published_data_search(requete, deb, fin)
    Brevets = []
    if data.ok:
        data = data.json()
        nbTrouv = int(data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
        patents = data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'ops:publication-reference']
        if isinstance(patents, list):
            for k in patents:
                if k not in Brevets:
                    Brevets.append(k)

        else: #sometimes its a sole patent
            if patents not in Brevets:
                Brevets.append(patents)
    else:
        print "request not correct, cql language only"
        return None
    return Brevets, nbTrouv
  
def ProcessBiblio(pat):
    PatentData = dict()
    if "country" in pat.keys():
        PatentData['label'] = pat["country"]['$']+pat[u'doc-number']['$']
    else:
        PatentData['label'] = pat['@country']+pat['@doc-number']
    try:
        PatentData['inventeur'] = Clean(ExtraitParties(pat, 'inventor', 'epodoc'))
    except:
        PatentData['inventeur'] = 'UNKNOWN'
    try:
        PatentData['applicant'] = Clean(ExtraitParties(pat, 'applicant','epodoc'))
    except:
        PatentData['applicant'] = 'UNKNOWN'
    try:
        PatentData['titre'] = Clean(ExtraitTitleEn(pat))
    except:
        PatentData['titre'] = 'UNKNOWN'
    try:
        PatentData['pays'] = ExtraitCountry(pat)
    except:
        PatentData['pays']  = 'UNKNOWN'
    try:    
        PatentData['portee'] = ExtraitKind(pat)
    except:
        PatentData['portee'] = 'UNKNOWN'
    date = ExtractionDate(pat)
    
    try:
        PatentData['classification'] = UnNest2List(ExtraitIPCR2(pat))
    except:
        PatentData['classification'] =''
#    if PatentData['classification'] is not None:
#        if isinstance(PatentData['classification'], list):
#            tempor = []
#            for classif in PatentData['classification']:
#                tempor.append(ExtractClassification(classif))
#        else:
#            tempor = ExtractClassification(PatentData['classification'])
#        if isinstance(tempor, list):
#            for temporar in tempor:                
#                for cle in temporar.keys():
#                    if cle != 'status': # old data model used this
#                        if cle in PatentData.keys():
#                            if temporar[cle] not in PatentData[cle]:
#                                PatentData[cle].append(temporar[cle])
#                        else:
#                            PatentData[cle] = []
#                            PatentData[cle].append(temporar[cle])
#        else:
#            for cle in tempor.keys():
#                if cle != 'status': # old data model used this
#                    if cle in PatentData.keys():
#                        if tempor[cle] not in PatentData[cle]:
#                            PatentData[cle].append(tempor[cle])
#                    else:
#                        PatentData[cle] = []
#                        PatentData[cle].append(tempor[cle])
        

#            del temporar    
#        if 'tempor' in locals().keys():
#            del tempor
    if str(pat).count('abstract')>0:
        if isinstance(pat[u'abstract'], dict):
            tempor = RecupAbstract(pat[u'abstract'])
            for cle in tempor:
                PatentData[cle] = tempor[cle] 
        else:
            for resum in pat[u'abstract']:
                tempor = RecupAbstract(resum)
                for cle in tempor:
                    PatentData[cle] = tempor[cle] 
    else:
        PatentData[u'abstract'] = ''
    try:
        PatentData['citations'] = len(pat[u'bibliographic-data'][u'references-cited']['citation'])
    except:
        PatentData['citations'] = 0
    try:
        if pat[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
            PatentData['priority-active-indicator'] = 1
    except:
        PatentData['priority-active-indicator'] = 0
        pass ## should check what is "active indicator" for patent
    try:
        if pat[u'bibliographic-data'][u'application-reference'][u'@is-representative'] == u'YES':
            PatentData['representative'] = 1                            
#                            PatentData['representative'] = True
        
    except:
        try:
            PatentData['application-ref'] = len(pat[u'bibliographic-data'][u'application-reference'][u'document-id'])/3 #epodoc, docdb, original... if one is missing, biais
        except:
            PatentData['application-ref'] = 0 # no application
        PatentData['representative'] = 0
    try:
        PatentData['publication-ref'] = pat[u'bibliographic-data'][u'publication-reference']
    except:
        PatentData['publication-ref'] = 0
    
    #doing some cleaning
        #transforming dates string in dates
    if date is not None:
        PatentData['date'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
#        print "patent date", PatentData['date']
    else:
        PatentData['date'] = datetime.date(datetime.date.today().year+2, 1, 1)
        #cleaning classsications
    #unesting everything
    for cle in PatentData.keys():
        if isinstance(PatentData[cle], list):
            PatentData[cle] = UnNest2List(PatentData[cle])
        
    return PatentData    

requete = ' '.join(sys.argv[2:]).replace(' = ', '=')
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'

try:  
    with open(ListPatentPath+'/'+ndf, 'r') as fic:
        DataBrevets= pickle.load(fic)
        lstBrevets = DataBrevets['brevets']
        nbActus = DataBrevets['number']
        if DataBrevets['requete'] != requete:
            print "care of using on file for one request, deleting this one."
            raw_input('sure? Unlee use ^C ( CTRL+C)')
        lstBrevets2, nbTrouves = PatentSearch(registered_client, requete)
        if len(lstBrevets) == nbTrouves and nbActus == nbTrouves:
            ficOk = True
            print len(lstBrevets), ' in file correspond t the request. Retreiving bibliographic data'
        else:
            ficOk = False
except:        
    lstBrevets = [] # gathering all again, I don t know if of serves the same ordered list of patents
    ficOk = False
if not ficOk:
    while len(lstBrevets) < nbTrouves:
        temp,  nbTrouves = PatentSearch(registered_client, requete, len(lstBrevets)+1, len(lstBrevets)+25)
        for p in temp:
            if p not in lstBrevets:
                lstBrevets.append(p)
    with open(ListPatentPath+'//'+ndf, 'w') as ficRes1:
        DataBrevets =dict()
        DataBrevets['brevets'] = lstBrevets
        DataBrevets['number'] = nbTrouves
        DataBrevets['requete'] = requete
        pickle.dump(DataBrevets, ficRes1)

print "found almost", len(lstBrevets), " patents. Saving list"

print "gathering bibliographic data"  
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'  
BiblioPatents = []
for brevet in lstBrevets:
    tempo =('publication', Docdb(brevet[u'document-id'][u'doc-number']['$'],brevet[u'document-id'][u'country']['$'], brevet[u'document-id'][u'kind']['$']))
    
    data = registered_client.published_data(*tempo, endpoint = 'biblio')
    if data.ok:
        patentBib = data.json()
        if isinstance(patentBib[u'ops:world-patent-data'][u'exchange-documents'], dict):
            tempo = ProcessBiblio(patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'])
            for cle in BiblioProperties:
                if cle not in tempo.keys():
                    tempo[cle] = ''
                elif tempo[cle] == 'N/A':
                    tempo[cle] = ''
            BiblioPatents.append(tempo)
        else:
            for patents in patentBib[u'ops:world-patent-data'][u'exchange-documents']:
                tempo = ProcessBiblio(patents[u'exchange-document'])
                for cle in BiblioProperties:
                    if cle not in tempo.keys():
                        tempo[cle] = ''
                    elif tempo[cle] == 'N/A':
                        tempo[cle] = ''
                    BiblioPatents.append(tempo)

with open(ResultPathBiblio +'/'+ndf, 'w') as ficRes:
    pickle.dump(BiblioPatents, ficRes)

print len(BiblioPatents), " bibliographic data gathered from OPS. Saving in file ", ficRes.name
print "use it with PatentToNetV5."    
    
