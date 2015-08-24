# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json

import pickle
#import bs4
from P2N_Lib import ReturnBoolean, Decoupe2, UnNest3#, UrlInventorBuild, UrlApplicantBuild
import datetime
aujourd = datetime.date.today()

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

# the list of keys for filtering for pivitable
clesRef = ['label', 'citations', 'title', 'year','priority-active-indicator', 
'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4', 
'IPCR7', "Inventor-Country", "Applicant-Country",  "CPC", 'Citations', 'references'] # "equivalents", "CitedBy"


ListBiblioPath = '..//DONNEES//'+rep+'//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'#List
ResultPathContent = '..//DONNEES//'+rep #+'//PatentContentsHTML'
temporPath = '..//DONNEES//'+rep+'//tempo'



with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
    
with open(ListPatentPath+'//'+ndf, 'r') as data:
    DataBrevet = pickle.load(data)

if isinstance(LstBrevet, dict):
    data = LstBrevet
    LstBrevet = data['brevets']    
    if data.has_key('requete'): 
        DataBrevet['requete'] = data["requete"]
    if data.has_key('number'):
        print "Found ", data["number"], " patents! Formating to HMTL tables"
    
LstExp = [] 
LstExp2 = [] 
#just for testing las fnction in gathered should deseapear soon

clesRef2 = ['label', 'year',  'priority-active-indicator', 'kind', 'applicant', 'country', 'inventor',  "CPC", 'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country", 'Citations'] #'citations','representative',


for brev in LstBrevet:
#    filtering against keys in clesRefs2 for pivottable
    tempo2=dict()
    for ket in clesRef2:
        tempo2[ket] = brev[ket] #filtering against clesRef2
        if ket =="Citations":
            if isinstance(brev[ket], list):
                if "empty" in brev[ket]:
                    tempo2[ket] = 0
                else:
                    print tempo2[ket]
            elif brev[ket] =='empty' or brev[ket] == '':
                tempo2[ket] = 0
            else:
                pass

    #next function will split each patent wich as multivaluated entries in a list of patents for each multivaluated one (hope its clear :-) )
    tempoBrev = Decoupe2(tempo2)
    for nb in tempoBrev.keys():
        
        if tempoBrev[nb] not in LstExp2:
            LstExp2.append(tempoBrev[nb])
print "Expanded to ", len(LstExp2), " monovaluated patents"
Exclude = []
print "entering formating html process"
dicoRes = dict()
dicoRes['data'] = LstExp
#contenu = json.dumps(dicoRes, indent = 3) #ensure_ascii=True, 
contenu2 = json.dumps(LstExp2,  indent = 3) #ensure_ascii=True,



with open(ResultPathContent + '//' + ndf+'Pivot.json', 'w') as resFic:
    resFic.write(contenu2)

FichierHtml=ndf+'.html'
ModelePivot = "Pivot.html"
with open(ModelePivot, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'Pivot.json' )  
    html = html.replace('**requete**', DataBrevet['requete'].replace('"', ''))
    html = html.replace('**FichierHtml**', FichierHtml)
    html = html.replace('**FichierHtmlFamille**', 'Families'+FichierHtml)
    with open(ResultPathContent + '//' + ndf+'Pivot.html', 'w') as resFic:
        resFic.write(html)

#os.system('start firefox -url '+ URLs.replace('//','/') )
