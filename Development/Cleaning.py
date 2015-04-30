# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:11:03 2015

@author: dreymond
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""


import pickle

from OPS2NetUtils2 import ReturnBoolean, SeparateCountryField, CleanPatentOthers
import sys

#On récupère la requête et les noms des fichiers de travail
if len(sys.argv)>1:
    ndf = sys.argv[1]
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
                if lig.count('GatherPatent')>0:
                    GatherPatent = ReturnBoolean(lig.split(':')[1].strip())
                if lig.count('GatherFamilly')>0:
                    GatherFamilly = ReturnBoolean(lig.split(':')[1].strip())
                if lig.count('InventorNetwork')>0:
                    P2NInv = ReturnBoolean(lig.split(':')[1].strip())
                if lig.count('ApplicantNetwork')>0:
                    AppP2N = ReturnBoolean(lig.split(':')[1].strip())
                if lig.count('ApplicantInventorNetwork')>0:
                    P2NAppInv = ReturnBoolean(lig.split(':')[1].strip())
                if lig.count('InventorCrossTechNetwork')>0:
                    P2NInvCT = ReturnBoolean(lig.split(':')[1].strip())
                if lig.count('CompleteNetwork')>0:
                    P2NComp = ReturnBoolean(lig.split(':')[1].strip())    
                if lig.count('CountryCrossTechNetwork')>0:
                    P2NCountryCT = ReturnBoolean(lig.split(':')[1].strip())
                if lig.count('FamiliesNetwork')>0:
                    P2NFamilly = ReturnBoolean(lig.split(':')[1].strip())    
                if lig.count('FamiliesHierarchicNetwork')>0:
                    P2NHieracFamilly = ReturnBoolean(lig.split(':')[1].strip())    
    
    
    
rep = ndf.replace('Families', '')
ndf = ndf.replace('Families', '')
clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior', "Inventor-Country", "Applicant-Country"]


ListBiblioPath = '..//DONNEES//'+rep+'//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'#List
ResultPathContent = '..//DONNEES//'+rep #+'//PatentContentsHTML'
temporPath = '..//DONNEES//'+rep+'//tempo'

data=dict()
with open(ListPatentPath+'//'+rep, 'r') as fic: # take the request only present in PatentList
    DataBrevet = pickle.load(fic)

    if isinstance(DataBrevet, dict):
        if DataBrevet.has_key('requete'): #just for catching this
            data["requete"] = DataBrevet['requete']


with open(ListBiblioPath+'//'+ndf, 'r') as fic:
    LstBrevet = pickle.load(fic)

if isinstance(LstBrevet, dict):
    data = LstBrevet
    LstBrevet = data['brevets']    
    if data.has_key('number'):
        print "Found ", data["number"], " patents in ", ndf, " file. Cleaning"

LstPat = [] 

for brev in LstBrevet:
#cleaning
   
    brevet= SeparateCountryField(brev)
    #cleaning classification
    tempo= CleanPatentOthers(brevet)
    #
    tempo['status'] = brev['portee']
    LstPat.append(tempo)
        
    ##
    #LstPat.append(brevet)
if isinstance(LstBrevet, dict):
    data['brevets'] = LstPat
else:
    data['brevets'] = LstPat
    data['number'] = len(LstPat)
    
#SAVING
with open(ListBiblioPath+'//'+ndf, 'w') as fic:
    pickle.dump(data, fic)
    print "Saved"
#DOING SAME FOR FAMILIES
ndf = 'Families'+ndf

with open(ListBiblioPath+'//'+ndf, 'r') as fic:
    LstBrevet = pickle.load(fic)

if isinstance(LstBrevet, dict):
    data = LstBrevet
    LstBrevet = data['brevets']    
    if data.has_key('number'):
        print "Found ", data["number"], " patents in ", ndf, " file. Cleaning!"
    
LstPat = [] 

for brev in LstBrevet:
#cleaning countries   
    brevet= SeparateCountryField(brev)
#cleaning classification
    tempo= CleanPatentOthers(brevet)
    ##
    LstPat.append(tempo)
data['brevets'] = LstPat        
data['number'] = len(LstPat)
#SAVING
with open(ListBiblioPath+'//'+ndf, 'w') as fic:
    pickle.dump(data, fic)
            #next will cause inconsistency of data...
        # to append needs to gather (again?) missing data
        #LstBrevet.append(bb)
