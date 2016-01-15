# -*- coding: utf-8 -*-
"""
Created on Tue Avr 1 13:41:21 2014

@author: dreymond
After loading patent list (created from 
OPSGather-BiblioPatent), the script will proceed a check for each patent
if it is orphan or has a family. In the last case, family patents are added to
the initial list (may be some are already in it), and a hierarchic within
the priority patent (selected as the oldest representative) and its brothers is created.  
V2:
#applications filling uncomplete are ignored
added citing field separating Patent citations ['CitP'] and External citations ['CitO']
#unconsistent with OPSGatherPatents...

12/12/15: file is update to get success in loading bibliofile. BUT, data is stored as a pickle file of the whole data patent set, not 
like in OPSGatherV2 witch is separated: one file for patents(append on file dump), the other for the description witch is much better
Amy be unconsistent with pivotable formating... (almost)
"""


#import networkx as nx

#from networkx_functs import *
import cPickle
#from Ops2 import ExtraitParties, Clean, ExtraitTitleEn, ExtraitKind, ExtraitCountry, ExtraitIPCR2, ExtractionDate
from P2N_Lib import Update, GetFamilly, flatten
from P2N_Lib import ReturnBoolean, LoadBiblioFile

import epo_ops
import os
import sys
from collections import OrderedDict as dict
import collections
global key
global secret

# put your credential from epo client in this file...

fic = open('..//cles-epo.txt', 'r')
key, secret = fic.read().split(',')
fic.close()

os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
DureeBrevet = 20
SchemeVersion = '20140101' #for the url to the classification scheme
 


ListeBrevet = []
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
rep = ndf

clesRef = ['label', 'title', 'year','priority-active-indicator', 'prior-Date', 'prior-dateDate', # dates of priority claims
'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4', 
'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", "CPC", u'references', u'CitedBy', 'prior', 'family lenght', 'CitO', 'CitP']

def dictCleaner(dico):
    for clef in dico.keys():
        if isinstance(dico[clef], list) and len(dico[clef]) ==1:
            dico[clef] = dico[clef][0]
        elif isinstance(dico[clef], list) and len(dico[clef]) == 0:
            dico[clef] = ''
        elif isinstance(dico[clef], list) and len(dico[clef]) >1:
            if '' in dico[clef]:
                for nb in range(dico[clef].count('')):
                    dico[clef].remove('')
        else:
            pass
    return dico
def CleanNones(dico):
    if isinstance(dico, list):
        Res = [CleanNones(subDict) for subDict in dico]
        return Res
    elif isinstance(dico, dict):
        Keys = [key for key in dico.keys() if None in dico[key]]
        for cle in Keys:
            dico[cle] = [truc for truc in dico[cle] if truc is not None]
        return dico
    else:
        return dico
    
if GatherFamilly:
    print "Hi! This is the family gatherer. Processing ", ndf
    ResultPath = '..//DONNEES//'+rep+'//PatentBiblios'
    #ResultPathFamilies = '..//DONNEES//'+rep+'//PatentBiblios'
    temporPath = '..//DONNEES//'+rep+'//tempo'
    ResultContents= '..//DONNEES//'+rep+'//PatentContents'
    try:
        os.makedirs(ResultContents+'//'+'FamiliesAbstract')
        os.makedirs(temporPath)
    except:
        pass
    try:
        
        fic = open(ResultPath+ '//' + ndf, 'r')
        
        print "loading data file ", ndf+' from ', ResultPath, " directory."
        if 'Description'+ndf or "Description" + ndf.title() in os.listdir(ResultPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
            data = LoadBiblioFile(ResultPath, ndf)

        else: #Retrocompatibility
            print "gather your data again"
            sys.exit()
        if isinstance(data, collections.Mapping):
            ListeBrevet = data['brevets']
            if data.has_key('number'):
                print "Found ", data["number"], " patents!"
        else:
            print 'data corrupted. Do something (destroy data directory is a nice idea)'
            sys.exit()
        print len(ListeBrevet), " patents loaded from file."
        print "Augmenting list with families."
        ficOk = True
    except:
        print "file ", ResultPath +"/"+ndf,"  missing. try gather again."
        ficOk = False
    
    ndf2 = "Complete"+ndf
    
    ListLab = [pat['label'] for pat in ListeBrevet]
    #import requests, time, pprint
        	####
    # Familly check
    
    try: #temporar directory if gathering processing have already started
        DoneLstBrev = open(temporPath+'//DoneTempo'+ ndf, 'r')
        Done = cPickle.load(DoneLstBrev) # these won't be gathered again
        DoneLab = [pat['label'] for pat in Done]
    except:
        DoneLab = []
        Done =[]
    if  0 < len(Done) <= len(ListeBrevet):
        tempoList = []
        try:
            #ndfLstBrev = open(ResultPath+'//Families'+ ndf, 'r')
            BrevetFam = LoadBiblioFile(ResultPath, "Families"+ndf)
            ListeBrevetAug = BrevetFam['brevets']
#            if isinstance(data, collections.Mapping):
#                ListeBrevetAug = data['brevets']
#            else:
#                ListeBrevetAug = data
            print len(ListeBrevetAug), " patents loaded from augmented list"
            if len(ListeBrevetAug) ==0:
                Done =[]
            for k in ListLab: #filtering
                if k not in DoneLab:
                    for brev in ListeBrevet:
                        if brev['label'] == k:
                            tempoList.append(brev)
            ListeBrevet = tempoList
            print len(DoneLab), ' patents treated yet... doing others : ', len(ListeBrevet)
            if len(ListeBrevet) == 0:
                print "Good, nothing to do!"
                print "If you want to gather again, please destroy the temporary file in ", temporPath
                sys.exit()

        except: #particular cases when I supress familiFile in Biblio ^_^
            ListeBrevetAug = []
            Done = []
    else: 
        ListeBrevetAug = []
        Done = []
    if ficOk and GatherFamilly:
        registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
        registered_client.accept_type = 'application/json'
        DejaVu = []
        for Brev in ListeBrevet:
            
            if Brev is not None and Brev != '':
                temp = GetFamilly(registered_client, Brev, ResultContents)
                temp = CleanNones(temp)
                if temp is not None:
                    tempFiltered =[]
                    LabList = [pat['label'] for pat in temp]
                    YetIn = []
                    for pat in LabList:
                        tempoPat = [patent for patent in temp if patent['label'] == pat] # fusionning several patents wwith same label
                        # OPS model seem to save one entry for several status documents... 
                                # in P2N model, label is unique key... so properties are lists.. this is the jobs of update function hereafter 
                        
                        tempoRar = dict()
                        for pate in tempoPat:
                            tempoRar = Update(pate, tempoRar)
                            for clef in tempoRar.keys():                            
                                if isinstance(tempoRar[clef], list):
                                    tempoRar[clef] = flatten(tempoRar[clef])
                                    tempo = []
                                    for contenu in set(tempoRar[clef]):
                                        if contenu is not None:
                                            tempo.append(contenu)
                                        else:
                                            if '' not in tempo and len(tempo)==0:
                                                tempo.append('')
                                    tempoRar[clef] = tempo
                                else:
                                    pass #should be good here
                        if pat not in YetIn:        
                            tempFiltered.append(dictCleaner(tempoRar))
                            YetIn.append(pat)
                        else:
                            pass # patent should be already in and updated for several states

                            
                    for pat in tempFiltered: # temp filtered should be nice
                        pat = dictCleaner(pat)
                        if pat not in ListeBrevetAug :
                            if pat['label'] in DejaVu:
                               #this may be enormous....should be update instead    
                               BrevetFam = LoadBiblioFile(ResultPath, "Families"+ndf)
                               LstPatents = BrevetFam['brevets']
                               bre = [pate for pate in LstPatents if pate['label'] == pat['label']] # retreive the good patent
                               tempoBre =pat
                               for brev in bre:
                                   LstPatents.remove(brev)
                                   tempoBre = Update(tempoBre, brev) #update it
                                   
                               tempoBre = dictCleaner(tempoBre)
                                  # remove previous
                               LstPatents.append(tempoBre) # save new
                               ListeBrevetAug.append(tempoBre)
                               with open(ResultPath+'//Families'+ ndf, 'a') as ndfLstBrev:
                                   for bre in LstPatents:
                                       cPickle.dump(bre , ndfLstBrev)    
                            else:
                                DejaVu.append(pat['label'])
                                ListeBrevetAug.append(dictCleaner(pat))
                                with open(ResultPath+'//Families'+ ndf, 'a') as ndfLstBrev:
                                    cPickle.dump(pat , ndfLstBrev) 
                        else:
                            # hum it is already in so, nothing to do
                             pass      
#                            
#                        if pat not in ListeBrevetAug and pat != '':
#                            if pat['label'] in DejaVu:
#                                temporar = [patent for patent in temp if patent['label'] == pat['label']] # may be several entries
#                                # OPS model seem to save one entry for several status documents... 
#                                # in P2N model, label is unique key... so properties are lists.. this is the jobs of updater 
#                                
##Note 12/12/15 appending new chganges in data storage, I'm not sure of what is done here....
#                                with open(ResultPath+'//Families'+ ndf, 'a') as ndfLstBrev:  
#                                    if isinstance(temporar, list):
#                                        tempoPat = dict()
#                                        for pate in temporar:
#                                            tempoPat = Update(pate, tempoPat)
#                                        for clef in tempoPat.keys():
#                                            tempoPat[clef] = flatten(tempoPat[clef])
#                                        if tempoPat not in ListeBrevetAug:
#                                            cPickle.dump(tempoPat, ndfLstBrev)
#                                        else:
#                                            print "already in ?"
#                                    elif temporar not in ListeBrevetAug:
#                                        for clef in tempoPat.keys():
#                                            tempoPat[clef] = flatten(tempoPat[clef])
#                                        cPickle.dump(temporar, ndfLstBrev) #should I check again if it is in it ?
#                                        
#                                #temp.append(temporar)
#                            else:
##                                pat = CleanPatent(pat)
##                                for cle in pat.keys():
##                                    pat[cle] = UnNest(pat[cle])
#                                with open(ResultPath+'//Families'+ ndf, 'a') as ndfLstBrev:
#                                    cPickle.dump(pat, ndfLstBrev)
#                                DejaVu.append(pat['label'])
#                                ListeBrevetAug.append(pat)
#                        elif pat in ListeBrevetAug and pat != '':
#                            temporar = [patent for patent in ListeBrevetAug if patent['label'] == pat['label']] #hum should be unique                  
#                            if isinstance(temporar, list):
#                                tempoPat = dict()
#                                for pate in temporar:
#                                    tempoPat = Update(pate, tempoPat)
#                                for clef in tempoPat.keys():
#                                    tempoPat[clef] = flatten(tempoPat[clef])
#                                cPickle.dump(tempoPat, ndfLstBrev)
#                                ListeBrevetAug.remove(pat)
#                                ListeBrevetAug.append(tempoPat)
#                            elif temporar not in ListeBrevetAug:
#                                for clef in temporar.keys():
#                                    temporar[clef] = flatten(temporar[clef])
#                                ListeBrevetAug.append(temporar)
#                                with open(ResultPath+'//Families'+ ndf, 'a') as ndfLstBrev:
#                                    cPickle.dump(temporar, ndfLstBrev)
#                        else:
#                            print "why are we there ? pat:", pat
                        
    #            time.sleep(7)
            Done.append(Brev)
            Data = dict()
            with open(ResultPath+'//DescriptionFamilies'+ ndf, 'w') as ndfLstBrev:
                Data['ficBrevets'] = 'Families'+ ndf
                Data['number'] = len(ListeBrevetAug)
                Data['requete'] = "Families of: " + requete
                cPickle.dump(Data, ndfLstBrev)
            with open(temporPath+'//DoneTempo'+ ndf, 'w') as DoneLstBrev:
                cPickle.dump(Done, DoneLstBrev)
                
    
    
    print "before", len(ListeBrevet)
    print "now", len(ListeBrevetAug)
    #####
    Data = dict()
    with open(ResultPath+'//DescriptionFamilies'+ ndf, 'w') as ficRes:
        Data['ficBrevets'] = 'Families'+ ndf
        Data['number'] = len(ListeBrevetAug)
        Data['requete'] = "Families of: " + requete
        cPickle.dump(Data, ficRes)
    
    print len(ListeBrevetAug), ' patents found and saved in file: '+ ResultPath+'//Families'+ ndf
    #    os.system("FormateExportFamilies.exe Families"+ndf)