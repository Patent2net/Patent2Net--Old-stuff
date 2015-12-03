# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
This script will load the request from file "requete.cql", construct the list 
of patents corresponding to this request ans save it to the directorry ../DONNEES/PatentLists
Then, the bibliographic data associated to each patent in the patent List is collected and
stored to the same file name in the directory ../DONNEES/PatentBiblio.  
"""

#BiblioPropertiesOLD = ['publication-ref', 'priority-active-indicator', 'classification', 
#u'resume', 'IPCR1', 'portee', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'label', 'IPCR11', 
#'date', 'citations', 'application-ref', 'pays', u'abstract', 'titre', 'inventeur', 
#'representative', 'abs' ]
#
#
#BiblioPropertiesOLD2 =  ['applicant', 'application-ref', 'citations', 'classification', 
#'inventor', 'IPCR1', 'IPCR11', 'IPCR3', 'IPCR4', 'IPCR7', 'label', 'country', 'kind', 
#'priority-active-indicator', 'title','date',"publication-ref","representative",
#"CPC", "prior", "priority-claim", "year", "family-id", "equivalent",
# 'inventor-country', 'applicant-country', 'inventor-nice', 'applicant-nice']

#New in V2... 11/2015
BiblioProperties =  ['applicant', 'application-ref', 'citations', 'classification', 
                     'prior-Date', 'prior-dateDate'
'inventor', 'IPCR1', 'IPCR11', 'IPCR3', 'IPCR4', 'IPCR7', 'label', 'country', 'kind', 
'priority-active-indicator', 'title','date',"publication-ref","representative",
"CPC", "prior", "priority-claim", "year", "family-id", "equivalent",
 'inventor-country', 'applicant-country', 'inventor-nice', 'applicant-nice', 'CitP', 'CitO', 'references']
#from networkx_functs import *
import pickle
#from P2N_Lib import ExtractAbstract, ExtractClassificationSimple2, UniClean, SeparateCountryField, CleanPatent, ExtractPatent, ExtractPubliRefs,
from P2N_Lib import ReturnBoolean, Initialize, PatentSearch,  GatherPatentsData
#from P2N_Lib import ProcessBiblio, MakeIram,  UnNest3, SearchEquiv, PatentCitersSearch
#from P2N_Lib import Update
#from P2N_Lib import EcritContenu, coupeEnMots

#
import epo_ops
import os
#from epo_ops.models import Docdb
#from epo_ops.models import Epodoc
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
import os

ListeBrevet = [] # LA iste de brevets
#ouverture fichier de travail

ficOk = False
cptNotFound=0
nbTrouves = 0

lstBrevets = [] # The patent List
BiblioPatents = [] # The bibliographic data

#opening request file, reading parameters
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
                GatherBibli = ReturnBoolean(lig.split(':')[1].strip())
                
            if lig.count('GatherPatent')>0:
                GatherPatent = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherFamilly')>0:
                GatherFamilly = ReturnBoolean(lig.split(':')[1].strip())
 #should set a working dir one upon a time... done it is temporPath
rep = ndf
ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'
ResultPathBiblio = '..//DONNEES//'+rep+'//PatentBiblios'
ResultContents= '..//DONNEES//'+rep+'//PatentContents'
temporPath = '..//DONNEES//'+rep+'//tempo'
ResultAbstractPath = ResultContents+'//Abstract'
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
try:
    os.makedirs(temporPath)
except:
    pass
if 'Abstract' not in os.listdir(ResultContents):
    os.mkdir(ResultContents+'//Abstract')                                    


#by default, data are not gathered yet
# building patentList
if GatherPatent:
    BiblioPatents, PatIgnored = [], Initialize(GatherPatent, GatherBiblio)
    #requete = "book digital"
    registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
    registered_client.accept_type = 'application/json'
    GatherBibli = GatherBiblio #this parametric option was added after...
    try:  
        with open(ListPatentPath+'//'+ndf, 'r') as fic:
            DataBrevets= pickle.load(fic)
            lstBrevets = DataBrevets['brevets']
            nbActus = DataBrevets['number']
            if DataBrevets.has_key('Fusion'):
                ficOk = True
                print nbTrouves, " patents gathered yet. No more patents to retreive. Steping to bibliographic data."
                GatherBibli = False
                requete = DataBrevets['brevets']
            if GatherPatent:
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
            else:
                print "You prefer not to gather data. At your own risk. P2N may crash"
    except:    
        try:
            with open(ResultPathBiblio+'//'+ndf, 'r') as fic:
                DataBrevets= pickle.load(fic)
                lstBrevets = DataBrevets['brevets']
                nbActus = DataBrevets['number']
                if DataBrevets.has_key('Fusion'):
                    ficOk = True
                    print nbTrouves, " patents gathered yet. No more patents to retreive. Steping to bibliographic data."
                    GatherBibli = False
                    requete = DataBrevets['brevets']
                else:
                    ficOk = False
                    nbTrouves = 1 
        except:
            lstBrevets = [] # gathering all again, I don t know if of serves the same ordered list of patents
            ficOk = False
            nbTrouves = 1 
    STOP = False
else:
    print "Good, nothing to do"
if not ficOk and GatherPatent:
    while len(lstBrevets) < nbTrouves and not STOP:
        if len(lstBrevets)+25<2000:
            temp,  nbTrouves = PatentSearch(registered_client, requete, len(lstBrevets)+1, len(lstBrevets)+25)
            ajouts = 0
        else:
            temp,  nbTrouves = PatentSearch(registered_client, requete, len(lstBrevets)-25, 2000) #hum should gather twice here
            if 'ajouts' not in locals():
                ajouts = 0
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

listeLabel = []        
# Entering PatentBiblio feeding
print "Gathering bibliographic data"  
if GatherBibli and GatherBiblio:
    try:  
        with open(ResultPathBiblio+'//'+ndf, 'r') as fic:
            data = pickle.load(fic)
            if isinstance(data, dict):
                BiblioPatents = data['brevets']
                    # not forcing not to collect data
                    # while fusion may occor on patent list... and
                    # a not complete biblioPatent collection
            else:
                BiblioPatents = data
            if len(BiblioPatents) == len(lstBrevets):
                print len(BiblioPatents), " bibliographic patent data gathered yet? Nothing else to do :-)"
                GatherBibli = False
                for brevet in lstBrevets:
                    ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent for file system save (abstract, claims...)
                    listeLabel.append(ndb)
            else:
                ficOk = False
                print str(abs(len(lstBrevets) - len(BiblioPatents))), " patents data missing. Gathering."
                GatherBibli = True
                
    except:    
        print str(abs(len(lstBrevets))), " patents data missing. Gathering."

        BiblioPatents = [] # gathering all again, I don t know if of serves the same ordered list of patents
        GatherBibli = True
PatIgnored=0   

        
    
if GatherBibli and GatherBiblio:
    registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
    registered_client.accept_type = 'application/json'  
    
    
    for brevet in lstBrevets:
        
        YetGathered = [u['label'] for u in BiblioPatents]
        # may be current patent has already be gathered in a previous attempt
        # should add a condition here to check in os.listdir()
       
        ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent for file system save (abstract, claims...)
        listeLabel.append(ndb)
        if ndb not in YetGathered:      
            BiblioPatents = GatherPatentsData(brevet, registered_client, ResultContents, ResultAbstractPath,  PatIgnored, BiblioPatents)
            
            with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
                pickle.dump(BiblioPatents, ficRes)
                #verification of contents
#                LastPat = BiblioPatents[len(BiblioPatents)-1]
#                for key in LastPat.keys():
#                    print key, ' --->', LastPat[key]
#                    
#                print 
#                    
 
        else:
            pass #patent already gathered


    with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
        DataBrevets['brevets'] = BiblioPatents
        DataBrevets['number'] = len(BiblioPatents)
        DataBrevets['requete'] = requete
        pickle.dump(DataBrevets, ficRes)
    
    YetGathered = [u['label'] for u in BiblioPatents]
    
    NotGathered = [pat for pat in listeLabel if pat not in YetGathered]
    print "Ignored  patents from patent list", PatIgnored 
    print "unconsistent patents: ",len(NotGathered) 
    print "here is the list: ", " DONNEES\PatentContentHTML\\"+ndf
    
    print "Export in HTML using FormateExport"
#os.system("FormateExport.exe "+ndf)
#os.system("CartographyCountry.exe "+ndf)

    