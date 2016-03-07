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
import cPickle
#from P2N_Lib import ExtractAbstract, ExtractClassificationSimple2, UniClean, SeparateCountryField, CleanPatent, ExtractPatent, ExtractPubliRefs,
from P2N_Lib import ReturnBoolean, Initialize, PatentSearch,  GatherPatentsData, LoadBiblioFile
#from P2N_Lib import ProcessBiblio, MakeIram,  UnNest3, SearchEquiv, PatentCitersSearch
#from P2N_Lib import Update
#from P2N_Lib import EcritContenu, coupeEnMots

#
import epo_ops
import os
import sys
#from epo_ops.models import Docdb
#from epo_ops.models import Epodoc
os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret

# put your credential from epo client in this file...
# chargement clés de client
fic = open('..//cles-epo.txt', 'r')
key, secret = fic.read().split(',')
key, secret = key.strip(), secret.strip()
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
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as fic:
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
else:
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
nbTrouves  =0
#if GatherPatent:
BiblioPatents, PatIgnored = [], Initialize(GatherPatent, GatherBiblio)

registered_client = epo_ops.RegisteredClient(key, secret)
#        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'
GatherBibli = GatherBiblio #this parametric option was added after...
try:
    with open(ListPatentPath+'//'+ndf, 'r') as fic:
        DataBrevets= cPickle.load(fic)
        lstBrevets = DataBrevets['brevets']
        nbActus = DataBrevets['number']
        if DataBrevets.has_key('Fusion'):
            ficOk = True
            print nbActus, " patents gathered yet. No more patents to retreive. Steping to bibliographic data."
            GatherBibli = False
            requete = DataBrevets['brevets']
        if DataBrevets.has_key('FusionPat'):
            ficOk = True
            print nbActus, " patents gathered yet. Steping to bibliographic data."
            GatherPatent = False
            Gatherbibli = True
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
            print "You prefer not to gather data. I hope you know what you do. At your own risk. P2N may crash"
except:
    try:

        lstBrevets = LoadBiblioFile(ResultPathBiblio, ndf)
        nbActus = len(lstBrevets)
        ficOk = True

    except:
        lstBrevets = [] # gathering all again, I don t know if of serves the same ordered list of patents
        ficOknd = False
        nbTrouves = 1
STOP = False
#else:
#
#    print "Good, nothing to do"
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

        #cos.system('cls')
        print nbTrouves, " patents corresponding to the request."
        print len(lstBrevets), ' patents added',
    with open(ListPatentPath+'//'+ndf, 'w') as ficRes1:
        DataBrevets =dict() # this is the list of patents, same variable name as description and patent data in the following
        # this may cause problem sometime
        DataBrevets['brevets'] = lstBrevets
        DataBrevets['number'] = nbTrouves
        DataBrevets['requete'] = requete
        cPickle.dump(DataBrevets, ficRes1)
listeLabel = []
for brevet in lstBrevets:
    if u'document-id' in brevet.keys() and "invalid result" not in str(brevet):
        ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent for file system save (abstract, claims...)
        listeLabel.append(ndb)
print "Found almost", len(lstBrevets), " patents. Saving list"
print "Within ", len(set(listeLabel)), " unique patents"

listeLabel = []
# Entering PatentBiblio feeding
print "Gathering bibliographic data"
if GatherBibli and GatherBiblio:
    DataBrevets = dict()
    DataBrevets['brevets'] = []
    if ndf in os.listdir(ResultPathBiblio):
        with open(ResultPathBiblio+'//'+ndf, 'r') as fic:
            while 1:
                try:
                    DataBrevets['brevets'].append(cPickle.load(fic))
                except EOFError:
                    break

            if len(DataBrevets['brevets']) == len(listeLabel):
                print len(DataBrevets['brevets']), " bibliographic patent data gathered yet? Nothing else to do :-)"
                GatherBibli = False
                for brevet in lstBrevets:
                    ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent for file system save (abstract, claims...)
                    listeLabel.append(ndb)
    else:
        ficOk = False
        print str(abs(len(lstBrevets) - len(DataBrevets['brevets']))), " patents data missing. Gathering."
        GatherBibli = True

#    except:    #new data model
#        DataBrevets = dict()
#        DataBrevets['brevets'] = []
#        if ndf in os.listdir(ResultPathBiblio+'//'):
#            with open(ResultPathBiblio+'//'+ndf, 'r') as fic:
#                while 1:
#                    try:
#                        DataBrevets['brevets'].append(cPickle.load(fic))
#                    except EOFError:
#                        break
#            with open(ResultPathBiblio+'//Description'+ndf, 'r') as fic:
#                Descript = cPickle.load(fic)
#                DataBrevets['ficBrevets'] = Descript['ficBrevets']
#                DataBrevets['requete'] =  Descript['requete']
#            if len(DataBrevets['brevets']) == len(lstBrevets):
#                print len(BiblioPatents), " bibliographic patent data gathered yet? Nothing else to do :-)"
#                GatherBibli = False
#                for brevet in DataBrevets['brevets']:
#                    ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent for file system save (abstract, claims...)
#                    listeLabel.append(ndb)
#            else:
#                ficOk = False
#                print str(abs(len(DataBrevets['brevets']) - len(BiblioPatents))), "patents data missing. Gathering."
#                GatherBibli = True
#        else:
#            print str(abs(len(lstBrevets))), " patents data missing. Gathering."
#
#            BiblioPatents = [] # gathering all again, I don t know if of serves the same ordered list of patents
#            GatherBibli = True
PatIgnored=0



if GatherBibli and GatherBiblio:
    registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
    registered_client.accept_type = 'application/json'
    if "brevets" in DataBrevets.keys():
        YetGathered = list(set([bre['label'] for bre in DataBrevets["brevets"]]))
        print len(YetGathered), " patent bibliographic data gathered."
        DataBrevets["YetGathered"] = YetGathered
    elif "YetGathered" in DataBrevets.keys():
        YetGathered = DataBrevets["YetGathered"]

#        if len(YetGathered) < len(DataBrevets["brevets"]): # used for cleaning after first attempts :-) # removed for huge collects
#            DataBreTemp = [] # special cleaning process
#            for bre in DataBrevets["brevets"]:
#                if bre not in DataBreTemp:
#                    DataBreTemp.append(bre)
#            try:
#                os.remove(ResultPathBiblio +'//'+ndf)
#            except:
#                pass #should never be here
#            with open(ResultPathBiblio +'//'+ndf, 'w') as ficRes:
#                for bre in DataBreTemp:
#                    cPickle.dump(bre, ficRes)

    else:
        YetGathered = []
    for brevet in lstBrevets:

        # may be current patent has already be gathered in a previous attempt
        # should add a condition here to check in os.listdir()
       if 'invalid result' not in str(brevet) and u'document-id' in brevet.keys():
            ndb =brevet[u'document-id'][u'country']['$']+brevet[u'document-id'][u'doc-number']['$'] #nameOfPatent for file system save (abstract, claims...)
            listeLabel.append(ndb)
            if ndb not in YetGathered:
                try:
                    BiblioPatents = GatherPatentsData(brevet, registered_client, ResultContents, ResultAbstractPath,  PatIgnored, [])
                except:
                    print ndb, " ignored... error occured"
                    next

                if BiblioPatents is not None and BiblioPatents !=[]:
                    with open(ResultPathBiblio +'//'+ndf, 'a') as ficRes:

                        cPickle.dump(BiblioPatents[0], ficRes)
                        YetGathered.append(BiblioPatents[0]["label"])
                        print len(YetGathered), " patent bibliographic data already gathered."
                else:
                    #may should put current ndb in YetGathered...
                    #print
                    pass
    #
            else:
                pass # yet gathered
       else:
           print "invalid result"
           if 'label' in brevet.keys():
               if brevet['label'] not in YetGathered:
                    with open(ResultPathBiblio +'//'+ndf, 'a') as ficRes:

                        cPickle.dump(brevet, ficRes)
                        YetGathered.append(brevet["label"])
                        print len(YetGathered), " patent bibliographic data gathered."
               else:
                    pass #bad OPS entry
    with open(ResultPathBiblio +'//Description'+ndf, 'w') as ficRes:
        DataBrevets['ficBrevets'] = ndf
        DataBrevets['requete'] = requete
        DataBrevets["YetGathered"] = YetGathered
        DataBrevets.pop("brevets")
        cPickle.dump(DataBrevets, ficRes)


    NotGathered = [pat for pat in listeLabel if pat not in YetGathered]
    print "Ignored  patents from patent list", PatIgnored
    print "unconsistent patents: ",len(NotGathered)
    print "here is the list: ", " DONNEES\PatentContentHTML\\"+ndf

    print "Export in HTML using FormateExport"
#os.system("FormateExport.exe "+ndf)
#os.system("CartographyCountry.exe "+ndf)
