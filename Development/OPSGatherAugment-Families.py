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


#import networkx as nx

#from networkx_functs import *
import pickle
#from Ops2 import ExtraitParties, Clean, ExtraitTitleEn, ExtraitKind, ExtraitCountry, ExtraitIPCR2, ExtractionDate
from P2N_Lib import Update, GetFamilly
from P2N_Lib import ReturnBoolean, CleanPatent, UnNest

import epo_ops, os

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
if GatherFamilly:
    ResultPath = '..//DONNEES//'+rep+'//PatentBiblios'
    ResultPathFamilies = '..//DONNEES//'+rep+'//PatentBiblios'
    temporPath = '..//DONNEES//'+rep+'//tempo'
    ResultContents= '..//DONNEES//'+rep+'//PatentContents'
    try:
        os.makedirs(ResultContents+'//'+'FamiliesAbstracts')
        os.makedirs(temporPath)
    except:
        pass
    try:
        fic = open(ResultPath+ '//' + ndf, 'r')
        print "loading data file ", ndf+' from ', ResultPath, " directory."
        data = pickle.load(fic)
        fic.close()
        if isinstance(data, dict):
            ListeBrevet = data['brevets']
            if data.has_key('number'):
                print "Found ", data["number"], " patents!"
        else:
            raise
        print len(ListeBrevet), " patents loaded from file."
        print "Augmenting list with families."
        ficOk = True
    except:
        print "file ", ResultPath +"/"+ndf,"  missing. try gather again."
        ficOk = False
    
    ndf2 = "Complete"+ndf
    
    
    #import requests, time, pprint
        	####
    # Familly check
    
    try:
        DoneLstBrev = open(temporPath+'//DoneTempo'+ ndf, 'r')
        Done = pickle.load(DoneLstBrev)
    except:
        Done = []
    if len(Done) > 1:
        tempoList = []
        try:
            ndfLstBrev = open(ResultPathFamilies+'//Families'+ ndf, 'r')
            ListeBrevetAug = pickle.load(ndfLstBrev)
            print len(ListeBrevetAug), " patents loaded from augmented list"
            print len(Done), ' patents treated yet... doing others : ', len(ListeBrevet) - len(Done)
            for k in ListeBrevet:
                if k not in Done:
                    tempoList.append(k)
            ListeBrevet = tempoList
        except: #particular cases when I supress familiFile in Biblio ^_^
            ListeBrevetAug = []
            Done = []
    else: 
        ListeBrevetAug = []
    if ficOk and GatherFamilly:
        registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
        registered_client.accept_type = 'application/json'
        DejaVu = []
        for Brev in ListeBrevet:
            
            if Brev is not None and Brev != '' and Brev not in Done:
                temp = GetFamilly(registered_client, Brev, ResultContents)
                if temp is not None:
                    for pat in temp:
                        pat = CleanPatent(pat)
                        if pat not in ListeBrevetAug and pat != '':
                            if pat['label'] in DejaVu:
                                temporar = [patent for patent in temp if patent['label'] == pat['label']][0] #hum should be unique
                                temporar=UnNest(temporar)
                                for cle in temporar.keys():
                                    temporar[cle] = UnNest(temporar[cle])
                                temporar = CleanPatent(Update(temporar, pat))      
                                temporar = CleanPatent(temporar)
                                ListeBrevetAug.append(temporar)
                                #temp.append(temporar)
                            else:
                                pat = CleanPatent(pat)
                                for cle in pat.keys():
                                    pat[cle] = UnNest(pat[cle])
                                ListeBrevetAug.append(CleanPatent(pat))
                                DejaVu.append(pat['label'])
                        elif pat['label'] in ListeBrevetAug and pat != '':
                            temporar = [patent for patent in ListeBrevetAug if patent['label'] == pat['label']][0] #hum should be unique                  
                            ListeBrevetAug.remove(temporar)
                            temporar = CleanPatent(Update(temporar, pat))
                            temporar = CleanPatent(temporar)        
                            for cle in temporar.keys():
                                temporar[cle] = UnNest(temporar[cle])
                            ListeBrevetAug.append(temporar)
                        
    #            time.sleep(7)
            Done.append(Brev)
            with open(ResultPathFamilies+'//Families'+ ndf, 'w') as ndfLstBrev:
                pickle.dump(ListeBrevetAug, ndfLstBrev)
            with open(temporPath+'//DoneTempo'+ ndf, 'w') as DoneLstBrev:
                pickle.dump(Done, DoneLstBrev)
                
    
    
    print "before", len(ListeBrevet)
    print "now", len(ListeBrevetAug)
    #####
    Data = dict()
    with open(ResultPathFamilies+'//Families'+ ndf, 'w') as ficRes:
        Data['brevets'] = ListeBrevetAug
        Data['number'] = len(ListeBrevetAug)
        Data['requete'] = "Families of: " + requete
        pickle.dump(Data, ficRes)
    
    print len(ListeBrevetAug), ' patents found and saved in file: '+ ResultPathFamilies+'//Families'+ ndf
    print "Formating results"
#    os.system("FormateExportFamilies.exe Families"+ndf)