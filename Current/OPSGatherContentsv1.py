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
ResultPathContent = 'PatentsContent'
temporPath = 'tempo'
#by default, data are not gathered yet
ficOk = False


# à ce niveau de script, la liste des brevets est chargée avec des données 
# biblio qui vont être complétées
#import time, pprint

cptNotFound=0

   
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'

with open(ListPatentPath+'/'+ndf, 'r') as fic:
    DataBrevets= pickle.load(fic)
    lstBrevets = DataBrevets['brevets']
    nbActus = DataBrevets['number']
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
    return res
        #not fun
    
print "found in data file", len(lstBrevets), " patents."

print "gathering contents"  
registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'  
BiblioPatents = []
#making the directory saving patents
if 'Contents' not in  filter(os.path.isdir, os.listdir(os.getcwd())):
    os.mkdir(u'Contents')
os.chdir('Contents')
if ndf.replace('.dump', '') not in  filter(os.path.isdir, os.listdir(os.getcwd())):
    os.makedirs(ndf.replace('.dump', ''))
os.chdir(ndf.replace('.dump', ''))
desc, clm, ft = 0,0,0
for brevet in lstBrevets:
    tempo =('publication', Docdb(brevet[u'document-id'][u'doc-number']['$'],brevet[u'document-id'][u'country']['$'], brevet[u'document-id'][u'kind']['$']))
    ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']
    for content in [u'claims', u'description', u'fulltext']:
        if content not in filter(os.path.isdir, os.listdir(os.getcwd())):
            os.makedirs(content)
            
        try :
            data = registered_client.published_data(*tempo, endpoint = content)
            if data.status_code == 403:
                #making necessary redirections
                print data
            if data.ok:
                patentCont = data.json()
                
                #withch language ?
                #the following could be factorized !!!!!!!!
                if content == 'description':
                    description = []
                    description = patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'description'][u'p']
                    description = MakeText(description)
                    lang = ''
                    if patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'description'][u'@lang'] == 'EN':    
                        lang = 'EN'
                    elif patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'description'][u'@lang'] == 'FR':
                        lang = 'FR'          
                    EcritContenu(description, content+'\\'+lang+'-'+ndb+'.txt')   
                    desc +=1
                if content == 'claims':
                    claims = []
                    lang = ''
                    claims = patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][u'claims'][u'claim'][u'claim-text']
                    claims = MakeText(claims)
                    if patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'claims'][u'@lang'] == 'EN':  
                        lang = 'EN'
                    elif patentCont[u'ops:world-patent-data'][ u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][ u'claims'][u'@lang'] == 'FR':
                        lang = 'FR'          
                    EcritContenu(claims, content+'\\'+lang+'-'+ndb+'.txt')
                    clm += 1
                if content == 'fulltext':
                    FT = []
                    if patentCont[u'ops:world-patent-data'][u'ops:fulltext-inquiry'][u'ops:publication-reference'][u'document-id'][u'kind']['$'].count('B')>0:
                       print 
#                    if u'ftxt:fulltext-documents' in patentCont[u'ops:world-patent-data']:
#                        print
                       ft +=1

                    
        except:
            pass
       


print 'Over the ', len(BiblioPatents),  ' patents... '
print desc, " descriptions gathered. See ", ndf.replace('.dump', '')+'/description/ directory for files'
print clm, " claims files gathered. See ", ndf.replace('.dump', '')+'/claims/ directory for files'
print ft, " fulltext gathered. See ", ndf.replace('.dump', '')+'/fulltext/ directory for files'


print "use it with whatever you want :-)"    
    
