# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
After loading patent list (created from 
OPSGather-BiblioPatent), the script will proceed a check for each patent
if it is orphan or has a family. In the last case, family patents are added to
the initial list (may be some are already in it), and a hierarchic within
the priority patent (selected as the oldest representative) and its brothers is created. 
IRAMUTEQ tagguing is added to analyse content 
****PatentNumber ****date ****CIB3
"""

BiblioProperties = ['publication-ref', 'priority-active-indicator', 'classification', 
u'resume', 'IPCR1', 'portee', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'label', 'IPCR11', 
'date', 'citations', 'application-ref', 'pays', u'abstract', 'titre', 'inventeur', 
'representative'] 

#from networkx_functs import *
import pickle
from OPS2NetUtils2 import ReturnBoolean, ExtractAbstract, CleanPatent
from OPS2NetUtils2 import EcritContenu, coupeEnMots

import os
import epo_ops
from epo_ops.models import Docdb
from epo_ops.models import Epodoc

os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'#cacert.pem
os.environ['CA_BUNDLE'] = 'cacert.pem'

global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('../cles-epo.txt', 'r')
key, secret = fic.read().split(',')
fic.close()

 
DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme

ListeBrevet = [] # The patent List

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
                GatherContent = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherBiblio')>0:
                GatherBiblio = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherPatent')>0:
                GatherPatent = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherFamilly')>0:
                GatherFamilly = ReturnBoolean(lig.split(':')[1].strip())

rep = ndf
ListPatentPath = '..//DONNEES//'+rep+'//PatentBiblios'#Lists'
ResultPathContent = '..//DONNEES//'+rep+'//PatentContents'
temporPath = '..//DONNEES//'+rep+'//tempo'

try:
    os.makedirs(ResultPathContent)
except:
    pass

#by default, data are not gathered yet
ficOk = False


# à ce niveau de script, la liste des brevets est chargée avec des données 
# biblio qui vont être complétées
#import time, pprint

cptNotFound=0


#not fun
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'

with open(ListPatentPath+'//'+ndf, 'r') as fic:
    lstBrevet = pickle.load(fic) #DataBrevets before with PatentList file
    #lstBrevet = DataBrevets['brevets']
    
    if isinstance(lstBrevet, dict):
        data = lstBrevet
        lstBrevet = data['brevets']    
#        if data.has_key('requete'): 
#            DataBrevet['requete'] = data["requete"]
        if data.has_key('number'):
            print "Found ", data["number"], " patents! Gathering contents"

print "found in data file", len(lstBrevet), " patents."

print "gathering abstracts"  
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'  
BiblioPatents = []
#making the directory saving patents
    
RepDir = ResultPathContent
try:
    if 'abstracts' not in os.listdir(RepDir):
        os.makedirs(RepDir+"//Abstracts")
except:
    pass
#os.chdir(ndf.replace('.dump', ''))
desc, clm, ft, abstract = 0,0,0, 0
Langues = set()
if GatherContent:

    for brevet in lstBrevet:
        #tempo =('publication', Docdb(,, ))
        #if brevet['label'] == 'FR2997041':
#        tempo =('publication', Docdb(brevet[u'publication-ref'][u'document-id'][0][u'doc-number']['$'],brevet['publication-ref'][u'document-id'][0][u'country']['$'], brevet['publication-ref'][u'document-id'][0][u'kind']['$']))
#        tempo2 =('publication', Epodoc(brevet['publication-ref'][u'document-id'][0][u'country']['$']+brevet[u'publication-ref'][u'document-id'][0][u'doc-number']['$']))#, brevet[u'document-id'][u'kind']['$']))
        #tempoDocDb = 
        brevet = CleanPatent(brevet)
        brevet = CleanPatent(brevet)
        ndb =brevet[u'label']#[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']brevet['publication-ref'][u'document-id'][0][u'kind']['$'])
#check for already gathered patents        
        lstfic = os.listdir(ResultPathContent+'//Abstracts/')
        fichier = [fics[3:] for fics in lstfic]      
        if ndb+'.txt' not in fichier:
            for content in [u'abstract']:#claims', u'description']: #, u'fulltext'              
                try :
                    
                    tmp = Epodoc(ndb)
                    
                    tempo = ('publication', tmp)
                    data = registered_client.published_data(*tempo, endpoint = content)             #registered_client.published_data()
                    if 'abstract' not in str(data.json()):
                        tmp = Docdb(ndb[2:], ndb[0:2],brevet['status'])
                        tempo = ('publication', tmp)
                        data = registered_client.published_data(*tempo, endpoint = content)
                                               #brevet['publication-ref'][u'document-id'][0][u'doc-number']['$'],#brevet[u'document-id'][u'doc-number']['$'], 
                                #brevet['publication-ref'][u'document-id'][0][u'country']['$'],#brevet[u'document-id'][u'country']['$'], 
                                #brevet['publication-ref'][u'document-id'][0][u'kind']['$']), endpoint = content, constituents = [])
                except:
                    try:
                        tmp = Docdb(ndb[2:], ndb[0:2],brevet['status'])
                        tempo = ('publication', tmp)
                        data = registered_client.published_data(*tempo, endpoint = content)         #registered_client.published_data()

                    except:#from there totally fun... may be we do not get there...
                        try:
#                            print 'yes we get'
                            tmp = Epodoc(brevet['publication-ref'][u'document-id'][1][u'doc-number']['$'])
                            tmp.date = brevet['publication-ref'][u'document-id'][1][u'date']['$']
                            tmp.country_code = brevet['publication-ref'][u'document-id'][0][u'country']['$']
                            tmp.kind_code = brevet['publication-ref'][u'document-id'][0][u'kind']['$']
                            tempo = ('publication', tmp)                        
                            data = registered_client.published_data(*tempo, endpoint = content)
                        except:
                            try:
                                data = registered_client.published_data(*tempo, endpoint = content)
                            except:                                
                                print "pas de ", content, ' pour ', ndb
                                break
                if data.status_code == 403:
                        #making necessary redirections
                        print data
                if data.ok:
                        patentCont = data.json()
                        # Next line is for setting analyses variables for Iramuteq....
                        if isinstance(brevet['date'], list):
                            DateBrev = '-'.join(dat[0:4] for dat in brevet['date'])
                        else:
                            DateBrev =  brevet['date'][0:4]
                        IRAM = '**** *Nom_' + ndb +' *Pays_'+brevet['pays']+ ' *CIB3_'+'-'.join(brevet['IPCR3']) + ' *CIB1_'+'-'.join(brevet['IPCR1']) + ' *CIB4_'+'-'.join(brevet['IPCR4']) + ' *Date_' + DateBrev + ' *Deposant_'+'-'.join(coupeEnMots(str(brevet['applicant'])))
                        #withch language ?
                        #allready gathered
                        
                        #the following could be switchted... hope abstract do not change!
                        if str(patentCont).count('abstract')>0 and ndb+'.txt' not in fichier:
                            #description = [
    #                        try:
                            TXT=dict()
                            if isinstance(patentCont[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'], list):
                                for tempo in  patentCont[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document']:
                                    if tempo.has_key('abstract'):
                                        txtTemp = ExtractAbstract(tempo['abstract'])
                                        for cleLang in txtTemp:
                                            if TXT.has_key(cleLang):
                                                TXT[cleLang] += txtTemp[cleLang]
                                            else:
                                                TXT[cleLang] = txtTemp[cleLang]
                            else:
                              if patentCont[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'].has_key('abstract'):
                                  TXT = ExtractAbstract(patentCont[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'][u'abstract'])
                            
                                                
                            for lang in TXT.keys():                            
                                EcritContenu(IRAM + ' *Contenu_Abstract \n' + TXT[lang], RepDir+ '//'+ content+'s//'+lang+'-'+ndb+'.txt')   
                                Langues.add(lang)
                            abstract +=1
    #                        except:
    #                            print "pas glop"
    #                            print patentCont
                        
else:
    print "no gather parameter set. Finishing."

lstfic = os.listdir(ResultPathContent+'//abstracts/')
lang = [fics[0:2] for fics in lstfic]
Langues = set(lang)
print 'Over the ', len(lstBrevet),  ' patents... '
print abstract, " not so empty abstract gathered. See ", ndf.replace('.dump', '')+'/Abstracts/ directory for files'
print 'and ', len(lstBrevet) - abstract, " where already present"

#print ft, " fulltext gathered. See ", ndf.replace('.dump', '')+'/fulltext/ directory for files'

print "fusioning files for Iramuteq. See Donnees/"+ndf+"/PatentContents"
lstfic = os.listdir(ResultPathContent+'//abstracts/')
for ling in Langues:
    with open(ResultPathContent+'//'+ling.upper()+ '_Abstract_' +ndf+'.txt', "w") as ficRes:
        for fi in [fic2 for fic2 in lstfic if fic2.startswith(ling)]:
            content = RepDir+ '//abstracts/'+fi
            with open(content, 'r') as absFic:
                data = absFic.read().strip()
                ficRes.write(data +'\n')
print "use it with whatever you want :-) or IRAMUTEQ"    

