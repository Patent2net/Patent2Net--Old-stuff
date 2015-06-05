# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
This script will load the request from file "requete.cql", construct the list 
of patents corresponding to this request ans save it to the directorry ../DONNEES/PatentLists
Then, the bibliographic data associated to each patent in the patent List is collected and
stored to the same file name in the directory ../DONNEES/PatentBiblio.  
"""

BiblioProperties = ['publication-ref', 'priority-active-indicator', 'classification', 
u'resume', 'IPCR1', 'portee', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'label', 'IPCR11', 
'date', 'citations', 'application-ref', 'pays', u'abstract', 'titre', 'inventeur', 
'representative', 'abs' ]

#from networkx_functs import *
import pickle
from OPS2NetUtils2 import ExtractAbstract, ReturnBoolean, ExtractClassificationSimple2, \
                            SeparateCountryField, CleanPatent, UnNest, UniClean

from Ops3 import Update, Initialize, PatentSearch, ProcessBiblio, EcritContenu, coupeEnMots

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
if not ficOk and GatherPatent:
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
            else:
                ficOk = False
                print str(abs(len(lstBrevets) - len(BiblioPatents))), " patents data missing. Gathering."
                GatherBibli = True
                
    except:    
        print str(abs(len(lstBrevets))), " patents data missing. Gathering."

        BiblioPatents = [] # gathering all again, I don t know if of serves the same ordered list of patents
        GatherBibli = True
PatIgnored=0   


def ExtractPatent(pat, ResultContents, BiblioPatents):
    DejaLa = [bre['label'] for bre in BiblioPatents]
    for cle in ['inventeur', 'applicant', 'date', 'dateDate', 'titre']:
        if cle != 'date' and cle !='dateDate':
            if pat[cle] == None:
                pat[cle] = 'empty'
        else:
            if cle == 'date' and pat[cle] == None:
                import datetime
                pat[cle] = str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
            elif cle == 'dateDate' and pat[cle] == None:
                import datetime
                pat[cle] = datetime.date.today().year

    
    cles = [key for key in pat.keys() if pat[key]==None]
    for cle in cles:
        if cle=='date':
            pat[cle] = unicode(datetime.date.today().year)
        elif cle=="dateDate":
            pat[cle] = datetime.date.today()
        else:
            bre[cle] = u'empty'

    if None not in pat.values():        
#if Brev['label'] == Brev["prior"]: # just using primary patents not all the family
        if isinstance(pat['classification'], list):
            for classif in pat['classification']:
                tempo2 = ExtractClassificationSimple2(classif)
                for cle in tempo2.keys():
                    if cle in pat.keys() and tempo2[cle] not in pat[cle]:
                        if pat[cle] == '':
                            pat[cle] = []
                        if isinstance(tempo2[cle], list):
                            pat[cle].extend(tempo2[cle])
                        else:
                            pat[cle].append(tempo2[cle])
                    else:
                        pat[cle] = []
                        if isinstance(tempo2[cle], list):
                            pat[cle].extend(tempo2[cle])
                        else:
                            pat[cle].append(tempo2[cle])
                    if pat[cle].count(',')>0:
                        print pat[cle] #hum, strage state
        else:
            tempo2 = ExtractClassificationSimple2(pat['classification'])
            for cle in tempo2.keys():
                if cle in pat.keys() and tempo2[cle] not in pat[cle]:
                    if pat[cle] == '':
                        pat[cle] = []
                    if isinstance(tempo2[cle], list):
                        pat[cle].extend(tempo2[cle])
                    else:
                        pat[cle].append(tempo2[cle])
                else:
                    pat[cle] = []
                    if isinstance(tempo2[cle], list):
                        pat[cle].extend(tempo2[cle])
                    else:
                        pat[cle].append(tempo2[cle])
                if pat[cle].count(',')>0:
                    print pat[cle] #hum, strage state

            
                    #                print classif
        pat = SeparateCountryField(pat)
        for clekey in pat.keys():
            if isinstance(pat[clekey], list):
                pat[clekey] = UnNest(pat[clekey])
        if isinstance(pat['IPCR1'], list):
            CIB1 = '-'.join(dat for dat in pat['IPCR1'])
        else:
            CIB1 =  pat['IPCR1']
            
        if isinstance(pat['IPCR3'], list):
            CIB3 = '-'.join(dat for dat in pat['IPCR3'])
        else:
            CIB3 =  pat['IPCR3']
        if isinstance(pat['IPCR4'], list):
            CIB4 = '-'.join(dat for dat in pat['IPCR4'])
        else:
            CIB4 =  pat['IPCR4']
        IRAM = '**** *Label_' + ndb +' *Country_'+pat['pays']+ ' *CIB3_'+CIB3 + ' *CIB1_'+CIB1 + ' *CIB4_'+CIB4 + ' *Date_' + str(pat['dateDate'].year) + ' *Applicant_'+UniClean('-'.join(coupeEnMots(pat['applicant'])))
        IRAM = IRAM.replace('_ ', '_empty', IRAM.count('_ '))
        TXT=dict()
        if isinstance(patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'], list):
            for tempo in patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document']:
                if tempo.has_key('abstract'):
                    txtTemp = ExtractAbstract(tempo['abstract'])
                    for cleLang in txtTemp:
                        if TXT.has_key(cleLang):
                            TXT[cleLang] += txtTemp[cleLang]
                        else:
                            TXT[cleLang] = txtTemp[cleLang]
            
        else:
            if patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'].has_key('abstract'):
                TXT = ExtractAbstract(patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'][u'abstract'])
                for lang in TXT.keys():                            
                    EcritContenu(IRAM + TXT[lang], ResultAbstractPath+'//'+lang+'-'+ndb+'.txt')   
        if pat['label'] in DejaLa: #checking multiples status
                tempor = [patent for patent in BiblioPatents if patent['label'] == pat["label"]][0] #should be unique
                BiblioPatents.remove(tempor)
                tempor = Update(tempor, pat)
                for key in tempor.keys():
                    if isinstance(tempor[key], list):
                        tempor[key] = UnNest(tempor[key])
                tempor = CleanPatent(tempor)
                BiblioPatents.append(CleanPatent(tempor))
                
        else:
            for key in pat.keys():
                if isinstance(pat[key], list):
                    pat[key] =  UnNest(pat[key])
            pat = CleanPatent(pat)
            BiblioPatents.append(CleanPatent(pat))
            DejaLa.append(pat['label'])
        return pat, YetGathered, BiblioPatents
    else:#None values avoiding this patent
        if pat.has_key('label'):
            DejaLa.append(pat['label'])
        return None, DejaLa, BiblioPatents
    


if GatherBibli and GatherBiblio:
    registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
    registered_client.accept_type = 'application/json'  
    
    
    for brevet in lstBrevets:
        
        YetGathered = [u['label'] for u in BiblioPatents]
        # may be current patent has already be gathered in a previous attempt
        # should add a condition here to check in os.listdir()
        tempo =('publication', Docdb(brevet[u'document-id'][u'doc-number']['$'],brevet[u'document-id'][u'country']['$'], brevet[u'document-id'][u'kind']['$']))
        tempo2 =('publication', Epodoc(brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$']))#, brevet[u'document-id'][u'kind']['$']))
       
        ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent
        if ndb not in YetGathered:      
             try: #trying Epodoc first, unused due to response format (multi document instead of one only)
                 data = registered_client.published_data(*tempo2, endpoint = 'biblio')
                 patentBib = data.json()
                 data2 = registered_client.published_data(*tempo, endpoint = 'biblio')
                 if data.ok and data2.ok:
                     patentBibtemp = data.json()
                     patentBibtemp2= data2.json()
                     if len(str(patentBibtemp)) > len(str(patentBibtemp2)):
                         patentBib = patentBibtemp
                     else:
                         patentBib = patentBibtemp2
             except:
                 try:
                     data = registered_client.published_data(*tempo, endpoint = 'biblio')
                     patentBib = data.json()
                 except:
                     print 'patent ignored ', ndb
                     PatIgnored +=1
             if data.ok:
    #               hum this is unclear for all situations in OPS... in previous check
   
                
    
                
                if isinstance(patentBib[u'ops:world-patent-data'][u'exchange-documents'], dict):
                    if isinstance(patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'], dict):
                        tempoPat = ProcessBiblio(patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'])
                        tempoPat, YetGathered, BiblioPatents = ExtractPatent(tempoPat, ResultContents, BiblioPatents)
                        if tempoPat is not None:
                            for cle in tempoPat.keys():
                                    if isinstance(tempoPat[cle], list):
                                        for truc in tempoPat[cle]:
                                            if isinstance(truc, list):
                                                print "is no good"
                                            elif isinstance(truc, str) or isinstance(truc, unicode):
                                                if truc.count(",")>0:
                                                    print "is no goog 2"
                                    elif cle !='titre' and (isinstance(tempoPat[cle], str) or isinstance(tempoPat[cle], unicode)):
                                        if tempoPat[cle].count(",")>0:
                                            print "is no goog 2"                            
                            with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
                                pickle.dump(BiblioPatents, ficRes)
                    elif isinstance(patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'], list):
                        for patent in patentBib[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document']:
                            tempoPat = ProcessBiblio(patent)
                            tempoPat, YetGathered, BiblioPatents = ExtractPatent(tempoPat, ResultContents, BiblioPatents)
                            if tempoPat is not None:
                                 with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
                                      pickle.dump(BiblioPatents, ficRes)
                                 for cle in tempoPat.keys():
                                        if isinstance(tempoPat[cle], list):
                                            for truc in tempoPat[cle]:
                                                if isinstance(truc, list):
                                                    print "is no good"
                                                elif isinstance(truc, str) or isinstance(truc, unicode):
                                                    if truc.count(",")>0:
                                                        print "is no goog 2"
                                        elif cle !='titre' and (isinstance(tempoPat[cle], str) or isinstance(tempoPat[cle], unicode)):
                                            if tempoPat[cle].count(",")>0:
                                                print "is no goog 2"
                                    
                else: #list of patents but at upper level GRRRR
                    for patents in patentBib[u'ops:world-patent-data'][u'exchange-documents']:
                        tempoPat = ProcessBiblio(patents[u'exchange-document'])
                        #if None not in tempo.values():
                        tempoPat, YetGathered, BiblioPatents = ExtractPatent(tempoPat, ResultContents, BiblioPatents)
                        if tempoPat is not None:
                            with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
                                pickle.dump(BiblioPatents, ficRes)
                            for cle in tempoPat.keys():
                                if isinstance(tempoPat[cle], list):
                                    for truc in tempoPat[cle]:
                                        if isinstance(truc, list):
                                            print "is no good"
                                        elif isinstance(truc, str) or isinstance(truc, unicode):
                                            if truc.count(",")>0:
                                                print "is no goog 2"
                                elif cle !='titre' and (isinstance(tempoPat[cle], str) or isinstance(tempoPat[cle], unicode)):
                                    if tempoPat[cle].count(",")>0:
                                        print "is no goog 2"
        else:
            pass #patent already gathered

BiblioPatents2 = []
print len(BiblioPatents), " bibliographic data gathered from OPS. Cleaning and saving in file "
for bre in BiblioPatents:
    for cle in bre.keys():
        if bre[cle] is not None:
            if isinstance(bre[cle], list):
                bre[cle] = UnNest(bre[cle])
            elif isinstance(bre[cle], str):
                bre[cle] = unicode(bre[cle])
            else:
                bre[cle] = bre[cle]
        else:
            bre[cle] = ''
    BiblioPatents2.append(bre)
    
with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
    DataBrevets['brevets'] = BiblioPatents2
    DataBrevets['number'] = len(BiblioPatents2)
    DataBrevets['requete'] = requete
    pickle.dump(DataBrevets, ficRes)

YetGathered = [u['label'] for u in BiblioPatents]
listeLabel = [pat[u'document-id'][u'country']['$']+pat[u'document-id'][u'doc-number'][u'$'] for pat in lstBrevets]
NotGathered = [pat for pat in listeLabel if pat not in YetGathered]
print "Ignored  patents from patent list", PatIgnored 
print "unconsistent patents: ", DataBrevets['number'], len(NotGathered) 
print "here is the list: "

print "Formating export in HTML. See DONNEES\PatentContentHTML\\"+ndf
#os.system("FormateExport.exe "+ndf)
#os.system("CartographyCountry.exe "+ndf)

    