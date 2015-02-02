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
from OPS2NetUtils2 import *
from Ops3 import *
import os, sys
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



ListeBrevet = [] # LA iste de brevets
#ouverture fichier de travail
with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()



ListPatentPath = '..//DONNEES//PatentBiblios'#Lists'
ResultPathContent = '..//DONNEES//PatentContents'
temporPath = 'tempo'

try:
    os.makedirs(ResultPathContent)
except:
    pass
try:
    os.makedirs(ResultPathContent + '//' + ndf.replace('.dump', ''))
except: 
    pass
#by default, data are not gathered yet
ficOk = False


# à ce niveau de script, la liste des brevets est chargée avec des données 
# biblio qui vont être complétées
#import time, pprint

cptNotFound=0


def coupeEnMots(texte):
    "renvoie une liste de mots propres des signes de ponctuation et autres cochonneries"
    #texte= texte.lower()
    import re
    import string
    res = re.sub('['+string.punctuation+']', ' ', texte) # on vire la ponctuation
    res = re.sub('\d', ' ', res) # extraction des chiffres
    res = re.findall('\w+', res, re.UNICODE) # extraction des lettres seulement
    return res
    
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'

with open(ListPatentPath+'//'+ndf, 'r') as fic:
    lstBrevets = pickle.load(fic) #DataBrevets before with PatentList file
    #lstBrevets = DataBrevets['brevets']
    nbActus = len(lstBrevets)#DataBrevets['number']
    if nbActus != len(lstBrevets):
        print "some patents are missing for this request. ReUse OPSGatherPatents first."
        ficOk = False


        
def MakeText(Thing):
    res = u''
    if isinstance(Thing, list):
        for thing in Thing:
            res += MakeText(thing)
    elif isinstance(Thing, dict):
        if '$' in Thing.keys():
            if isinstance(Thing['$'], str) or isinstance(Thing['$'], unicode):
                return Thing['$'] +'\n'
            elif isinstance(Thing['$'], list):
                for thing in Thing['$']:
                    res += MakeText(thing) +'\n'
            else:
                print "I don't know what to do"
                    
        if 'p' in Thing.keys():
            if isinstance(Thing['p'], str) or isinstance(Thing['p'], unicode):
                return Thing['p']
            elif isinstance(Thing['p'], list):
                for thing in Thing['p']:
                    res += MakeText(thing)
            else:
                print "I don't know what to do"
                    
        elif 'claims' in str(thing):
            try:
                res = MakeText(Thing[u'claims']['claim'][u'claim-text'])
            except:
                print Thing.keys()
        else:
            print "what else ?"
    else:
        print "I don't know what to do"
        res = Thing
    return res
        #not fun
    
print "found in data file", len(lstBrevets), " patents."

print "gathering contents"  
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'  
BiblioPatents = []
#making the directory saving patents
    
RepDir = ResultPathContent + '//'+ ndf.replace('.dump', '')
try:
    os.makedirs(RepDir)
except:
    pass
#os.chdir(ndf.replace('.dump', ''))
desc, clm, ft = 0,0,0
for brevet in lstBrevets:
    #tempo =('publication', Docdb(,, ))
    #if brevet['label'] == 'FR2997041':
    tempo =('publication', Docdb(brevet[u'publication-ref'][u'document-id'][0][u'doc-number']['$'],brevet['publication-ref'][u'document-id'][0][u'country']['$'], brevet['publication-ref'][u'document-id'][0][u'kind']['$']))
    tempo2 =('publication', Epodoc(brevet['publication-ref'][u'document-id'][0][u'country']['$']+brevet[u'publication-ref'][u'document-id'][0][u'doc-number']['$']))#, brevet[u'document-id'][u'kind']['$']))

    ndb =brevet[u'label']#[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']brevet['publication-ref'][u'document-id'][0][u'kind']['$'])
    if not ndb.startswith('CN'):  #avoid check of chinese patents since they aren't descibed in english
        for content in [u'claims', u'description']: #, u'fulltext'
            if content not in os.listdir(RepDir):
                os.makedirs(RepDir +'//' +content)
                  # optional, list of constituents
    
            try :
                
                #registered_client.published_data()
                data = registered_client.published_data(reference_type = 'publication', 
                            input = Docdb(brevet['publication-ref'][u'document-id'][0][u'doc-number']['$'],#brevet[u'document-id'][u'doc-number']['$'], 
                            brevet['publication-ref'][u'document-id'][0][u'country']['$'],#brevet[u'document-id'][u'country']['$'], 
                            brevet['publication-ref'][u'document-id'][0][u'kind']['$']), endpoint = content, constituents = [])
            
            except:
                try:
                    data = registered_client.published_data(*tempo, endpoint = content)
                except:
                    try:
                        tmp = Epodoc(brevet['publication-ref'][u'document-id'][1][u'doc-number']['$'])
                        tmp.date = brevet['publication-ref'][u'document-id'][1][u'date']['$']
                        tmp.country_code = brevet['publication-ref'][u'document-id'][0][u'country']['$']
                        tmp.kind_code = brevet['publication-ref'][u'document-id'][0][u'kind']['$']
                        tempo = ('publication', tmp)                        
                        data = registered_client.published_data(*tempo, endpoint = content)
                    except:
                        try:
                            data = registered_client.published_data(*tempo2, endpoint = content)
                        except:
                            print "pas de ", content, ' pour ', ndb
                            break
            if data.status_code == 403:
                    #making necessary redirections
                    print data
            if data.ok:
                    patentCont = data.json()
                    IRAM = '**** *Nom_' + ndb +' *Pays_'+brevet['pays']+ ' *CIB3_'+'-'.join(brevet['IPCR3']) + ' *CIB1_'+'-'.join(brevet['IPCR1']) + ' *CIB4_'+'-'.join(brevet['IPCR4']) + ' *Date_' + str(brevet['date'].year) + ' *Mandataire_'+'-'.join(coupeEnMots(str(brevet['applicant'])))
                    #withch language ?
                    #the following could be factorized !!!!!!!!
                    if content == 'description':
                        description = []
                        description = patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'description'][u'p']
                        description = MakeText(description)
                        description = description.replace('\r\n', '\n')
                        Desc = u"" #cleaning process
                        for parag in description.split('\n'):
                            TXT = u""
                            for phrase in decoupParagraphEnPhrases(parag):
                                TXT+=' '.join(coupeEnMots(phrase)) #rebult phrases from words
                                TXT +='.' # Ending phrases by a point
                            Desc += TXT + '\n'#to retrieve the structure
                             
                            
                        lang = ''
                        if patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'description'][u'@lang'] == 'EN':    
                            lang = 'EN'
                        elif patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'description'][u'@lang'] == 'FR':
                            lang = 'FR'          
                        EcritContenu(IRAM + ' *Contenu_Description \n' + Desc, RepDir+ '//'+ content+'//'+lang+'-'+ndb+'.txt')   
                        desc +=1
                    if content == 'claims':
                        claims = []
                        lang = ''
                        claims = patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][u'claims'][u'claim'][u'claim-text']
                        claims = MakeText(claims)
                        claims = claims.replace('\r\n', '\n')
                        Claim = u"" #cleaning process
                        CompteClaim = 0
                        for parag in claims.split('\n'):
                            if len(parag)>4: #arbitraire
                                CompteClaim+=1
                                TXT = u" **** *Rev_"+str(CompteClaim)    
                                for phrase in decoupParagraphEnPhrases(parag):
                                    TXT+=' '.join(coupeEnMots(phrase)) #rebult phrases from words
                                    TXT +='.' # Ending phrases by a point
                                Claim += TXT + '\n'#to retrieve the structure
    
                        if patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'claims'][u'@lang'] == 'EN':  
                            lang = 'EN'
                        elif patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'claims'][u'@lang'] == 'FR':
                            lang = 'FR'          
                        EcritContenu(IRAM + ' *Contenu_Revendication \n' + Claim, RepDir + '//' + content+'//'+lang+'-'+ndb+'.txt')
                        clm += 1
                    if content == 'fulltext':
                        FT = []
                        if patentCont[u'ops:world-patent-data'][u'ops:fulltext-inquiry'][u'ops:publication-reference'][u'document-id'][u'kind']['$'].count('B')>0:
                           print 
    #                    if u'ftxt:fulltext-documents' in patentCont[u'ops:world-patent-data']:
    #                        print
                           ft +=1

                    
        


print 'Over the ', len(lstBrevets),  ' patents... '
print desc, " not so empty descriptions gathered. See ", ndf.replace('.dump', '')+'/description/ directory for files'
print clm, " not so empty claims files gathered. See ", ndf.replace('.dump', '')+'/claims/ directory for files'
#print ft, " fulltext gathered. See ", ndf.replace('.dump', '')+'/fulltext/ directory for files'

print "fusioning files for Iramuteq. See Donnees/PatentContents"
os.system("FusionIramuteq.exe "+ndf)
print "use it with whatever you want :-) or IRAMUTEQ"    

