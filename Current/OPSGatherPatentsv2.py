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
'representative', 'abs' ]

#from networkx_functs import *
import pickle
from OPS2NetUtils2 import *
from Ops3 import *

import epo_ops
import os
from epo_ops.models import Docdb

global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('../../../../cles-epo.txt', 'r')
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
#import requests, time, pprint

cptNotFound=0
nbTrouves = 0


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
            print nbtrouves, " patents to gather"
            print len(lstBrevets), ' in file corresponding to the request. Retreiving associated bibliographic data'
        else:
            ficOk = False
            print nbtrouves, " patents corresponding to the request."
except:        
    lstBrevets = [] # gathering all again, I don t know if of serves the same ordered list of patents
    ficOk = False
    nbTrouves = 1 
STOP = False
if not ficOk:
    while len(lstBrevets) < nbTrouves and not STOP:
        if len(lstBrevets)+25<2000:
            temp,  nbTrouves = PatentSearch(registered_client, requete, len(lstBrevets)+1, len(lstBrevets)+25)
        else:
            temp,  nbTrouves = PatentSearch(registered_client, requete, len(lstBrevets)+1, 2000)
            STOP = True
        for p in temp:
            if p not in lstBrevets:
                lstBrevets.append(p)
        os.system('cls')
        print nbTrouves, " patents corresponding to the request."
        print len(lstBrevets), ' patents added',
    with open(ListPatentPath+'//'+ndf, 'w') as ficRes1:
        DataBrevets =dict()
        DataBrevets['brevets'] = lstBrevets
        DataBrevets['number'] = nbTrouves
        DataBrevets['requete'] = requete
        pickle.dump(DataBrevets, ficRes1)

print "Found almost", len(lstBrevets), " patents. Saving list"

print "Gathering bibliographic data"  
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'  
BiblioPatents = []
for brevet in lstBrevets:
    tempo =('publication', Docdb(brevet[u'document-id'][u'doc-number']['$'],brevet[u'document-id'][u'country']['$'], brevet[u'document-id'][u'kind']['$']))
    ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent
    data = registered_client.published_data(*tempo, endpoint = 'biblio')
    if data.ok:
        if 'Abstracts' not in os.listdir(ResultPathBiblio):
            os.mkdir(ResultPathBiblio+'//Abstracts')
        if ndf not in os.listdir(ResultPathBiblio+'//Abstracts'):
            os.mkdir(ResultPathBiblio+'//Abstracts//'+ndf)
        patentBib = data.json()
        if isinstance(patentBib[u'ops:world-patent-data'][u'exchange-documents'], dict):
            tempo = ProcessBiblio(patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'])
            for cle in BiblioProperties:
                if cle != 'abstract' and cle != 'resume':
                    if cle not in tempo.keys():
                        tempo[cle] = ''
                    elif tempo[cle] == 'N/A':
                        tempo[cle] = ''
                elif cle == 'abstract':
                    langue='EN'
                    if cle in tempo.keys():
                        EcritContenu(str(tempo[cle]),ResultPathBiblio+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                        del tempo[cle]
                elif cle == 'resume':
                    langue='FR'
                    if cle in tempo.keys():
                        EcritContenu(str(tempo[cle]),ResultPathBiblio+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                        del tempo[cle]
                else:
                    langue='UNK'
                    if cle in tempo.keys():
                        EcritContenu(str(tempo[cle]),ResultPathBiblio+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                        del tempo[cle]
                    
            BiblioPatents.append(tempo)
        else:
            for patents in patentBib[u'ops:world-patent-data'][u'exchange-documents']:
                tempo = ProcessBiblio(patents[u'exchange-document'])
                for cle in BiblioProperties:
                    if cle != 'abstract' and cle != 'resume':
                        if cle not in tempo.keys():
                            tempo[cle] = ''
                        elif tempo[cle] == 'N/A':
                            tempo[cle] = ''
                        
                        
                    elif cle == 'abstract':
                        if cle in tempo.keys():
                            langue='EN'
                            EcritContenu(str(tempo[cle]),ResultPathBiblio+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                            del tempo[cle]
                    elif cle == 'resume':
                        if cle in patents.keys():                        
                            langue='FR'
                            EcritContenu(str(tempo[cle]),ResultPathBiblio+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                            del tempo[cle]
                    else:
                        if cle in patents.keys():
                            langue='UNK'
                            EcritContenu(str(tempo[cle]),ResultPathBiblio+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                            del tempo[cle]
                    BiblioPatents.append(tempo)
                        


with open(ResultPathBiblio +'/'+ndf, 'w') as ficRes:
    pickle.dump(BiblioPatents, ficRes)

print len(BiblioPatents), " bibliographic data gathered from OPS. Saving in file ", ficRes.name
print "use it with PatentToNetV5."    
    
