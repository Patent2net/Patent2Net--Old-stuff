# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
This script will load the request from file "requete.cql", construct the list 
of patents corresponding to this request ans save it to the directorry ../DONNEES/PatentLists
Then, the bibliographic data associated to each patent in the patent List is collected and
strore to the same file name in the directory ../DONNEES/PatentBiblio.  
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
from epo_ops.models import Epodoc
os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('..//cles-epo.txt', 'r')
key, secret = fic.read().split(',')
fic.close()

 
DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme
import os, sys


ListeBrevet = [] # LA iste de brevets
#ouverture fichier de travail


 #should set a working dir one upon a time
ListPatentPath = '..//DONNEES//PatentLists'
ResultPathBiblio = '..//DONNEES//PatentBiblios'
ResultContents= '..//DONNEES//PatentContents'
temporPath = 'tempo'
#by default, data are not gathered yet
ficOk = False


try:
    os.makedirs(ListPatentPath)
except:
    pass 
try:
    os.makedirs(ResultPathBiblio)
except:
    pass

try:
    os.makedirs(ResultContents)
except:
    pass

# à ce niveau de script, la liste des brevets est chargée avec des données 
# biblio qui vont être complétées
#import requests, time, pprint

cptNotFound=0
nbTrouves = 0


with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()


#requete = "book digital"
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'

try:  
    with open(ListPatentPath+'//'+ndf, 'r') as fic:
        DataBrevets= pickle.load(fic)
        lstBrevets = DataBrevets['brevets']
        nbActus = DataBrevets['number']
        if DataBrevets['requete'] != requete:
            print "care of using on file for one request, deleting this one."
            raw_input('sure? Unlee use ^C ( CTRL+C)')
        lstBrevets2, nbTrouves = PatentSearch(registered_client, requete)
        if len(lstBrevets) == nbTrouves and nbActus == nbTrouves:
            ficOk = True
            print nbTrouves, " patents gathered yet. No more patents to retreive. Steping to bibliographic data."
        else:
            ficOk = False
            print nbTrouves, " patents corresponding to the request."
            
            print len(lstBrevets), ' in file corresponding to the request. Retreiving associated bibliographic data'

except:        
    lstBrevets = [] # gathering all again, I don t know if of serves the same ordered list of patents
    ficOk = False
    nbTrouves = 1 
STOP = False
if not ficOk:
    while len(lstBrevets) < nbTrouves and not STOP:
        if len(lstBrevets)+25<2000:
            temp,  nbTrouves = PatentSearch(registered_client, requete, len(lstBrevets)+1, len(lstBrevets)+25)
            ajouts = 0
        else:
            temp,  nbTrouves = PatentSearch(registered_client, requete, len(lstBrevets)+1, 2000)
            STOP = True
        for p in temp:
            if p not in lstBrevets:
                lstBrevets.append(p)
                ajouts+=1
            
        if ajouts == 0:
            STOP = True
            print "too many similar previous matches. Exciting"            
            
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
try:  
    with open(ResultPathBiblio+'//'+ndf, 'r') as fic:
        BiblioPatents= pickle.load(fic)
        if len(BiblioPatents) == len(lstBrevets):
            print len(BiblioPatents), " bibliographic patent data gathered yet? Nothing else to do :-)"
            GatherBibli = False
        else:
            ficOk = False
            print len(lstBrevets) - len(BiblioPatents), " patents data missing. Gathering."
            GatherBibli = True
            
except:        
    BiblioPatents = [] # gathering all again, I don t know if of serves the same ordered list of patents
    GatherBibli = True
PatIgnored=0   
if GatherBibli:
    registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
    registered_client.accept_type = 'application/json'  
    
    
    for brevet in lstBrevets:
        
        YetGathered = [u['label'] for u in BiblioPatents]
        # may be current patent has already be gathered in a previous attempt
        # should add a condition here to check in os.listdir()
        tempo =('publication', Docdb(brevet[u'document-id'][u'doc-number']['$'],brevet[u'document-id'][u'country']['$'], brevet[u'document-id'][u'kind']['$']))
        #tempo2 =('publication', Epodoc(brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']))#, brevet[u'document-id'][u'kind']['$']))
       
        ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent
        if ndb not in YetGathered:      
            try: #trying Epodoc first, unused due to response format (multi document instead of one only)
                data = registered_client.published_data(*tempo2, endpoint = 'biblio')
            except:
                try:
                    data = registered_client.published_data(*tempo, endpoint = 'biblio')
                except:
                    print 'patent ignored ', ndb
                    PatIgnored +=1
            if data.ok:
                if ndf not in os.listdir(ResultContents):
                    os.mkdir(ResultContents+'//' + ndf)
                if 'Abstracts' not in os.listdir(ResultContents+'//' + ndf):
                    os.mkdir(ResultContents+'//'+ ndf+'//Abstracts')
                    
                
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
                                EcritContenu(str(tempo[cle]),ResultContents+'//'+ndf+'//Abstracts//'+langue+'-'+ndb+'.txt')
                                del tempo[cle]
                        elif cle == 'resume':
                            langue='FR'
                            if cle in tempo.keys():
                                EcritContenu(str(tempo[cle]),ResultContents+'//'+ndf+'//Abstracts//'+langue+'-'+ndb+'.txt')
                                del tempo[cle]
                        else:
                            langue='UNK'
                            if cle in tempo.keys():
                                EcritContenu(str(tempo[cle]),ResultContents+'//'+ndf+'//Abstracts//'+langue+'-'+ndb+'.txt')
                                del tempo[cle]
                        
                #if Brev['label'] == Brev["prior"]: # just using primary patents not all the family
                    if isinstance(tempo['classification'], list):
                        for classif in tempo['classification']:
                            tempo2 = ExtractClassificationSimple2(classif)
                            for cle in tempo2.keys():
                                if cle in tempo.keys() and tempo2[cle] not in tempo[cle]:
                                    if tempo[cle] == '':
                                        tempo[cle] = []
                                    tempo[cle].append(tempo2[cle])
                                else:
                                    tempo[cle] = []
                                    tempo[cle].append(tempo2[cle])
                    elif tempo['classification'] != '':
                        tempo2 = ExtractClassificationSimple2(Brev['classification'])
                        for cle in tempo2.keys():
                            if cle in tempo.keys() and tempo2[cle] not in tempo[cle]:
                                if tempo[cle] == '':
                                        tempo[cle] = []
                                tempo[cle].append(tempo2[cle])
                            else:
                                tempo[cle] = []
                                tempo[cle].append(tempo2[cle])
                                #                print classif
                    #tempo['applicant'] = Formate(tempo['applicant'], tempo['pays'])
                    
                    # remember inventor original writing form to reuse in the url property of the node
                    #tempo['inventeur'] = Formate(tempo['inventeur'], tempo['pays'])
                 
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
                                    EcritContenu(str(tempo[cle]),ResultContents+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                                    del tempo[cle]
                            elif cle == 'resume':
                                if cle in patents.keys():                        
                                    langue='FR'
                                    EcritContenu(str(tempo[cle]),ResultContents+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                                    del tempo[cle]
                            else:
                                if cle in patents.keys():
                                    langue='UNK'
                                    EcritContenu(str(tempo[cle]),ResultContents+'//Abstracts//'+ndf+'//'+langue+ndb+'.txt')
                                    del tempo[cle]
                        if isinstance(tempo['classification'], list):
                            for classif in tempo['classification']:
                                tempo2 = ExtractClassificationSimple2(classif)
                                for cle in tempo2.keys():
                                    if cle in tempo.keys() and tempo2[cle] not in tempo[cle]:
                                        if tempo[cle] == '':
                                            tempo[cle] = []
                                        tempo[cle].append(tempo2[cle])
                                    else:
                                        tempo[cle] = []
                                        tempo[cle].append(tempo2[cle])
                        elif tempo['classification'] != '':
                            tempo2 = ExtractClassificationSimple2(Brev['classification'])
                            for cle in tempo2.keys():
                                if cle in tempo.keys() and tempo2[cle] not in tempo[cle]:
                                    if tempo[cle] == '':
                                            tempo[cle] = []
                                    tempo[cle].append(tempo2[cle])
                                else:
                                    tempo[cle] = []
                                    tempo[cle].append(tempo2[cle])
                                    #                print classif
                        tempo['applicant'] = Formate(tempo['applicant'], tempo['pays'])
                        
                        # remember inventor original writing form to reuse in the url property of the node
                        tempo['inventeur'] = Formate(tempo['inventeur'], tempo['pays'])
                
                        BiblioPatents.append(tempo)
                                
        
#==============================================================================
#             YetGathered = [u['label'] for u in BiblioPatents]
#             Temp = [u for u in BiblioPatents if u['label'] not in YetGathered] # one time cleaning
#==============================================================================
            
            with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
                pickle.dump(BiblioPatents, ficRes)
        else:
            pass #patent already gathered
    
print len(BiblioPatents), " bibliographic data gathered from OPS. Saving in file "
print "Ignored  patents from patent list", PatIgnored 
print "use it with PatentToNetV5."    

print "Formating export in HTML. See DONNEES\PatentContentHTML\\"+ndf
os.system("FormateExport.exe "+ndf)


    