# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json

import pickle
#import bs4
from P2N_Lib import ReturnBoolean, DecoupeOnTheFly # UnNest3#, UrlInventorBuild, UrlApplicantBuild
import datetime
aujourd = datetime.date.today()

with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf2 = lig.split(':')[1].strip()
            if lig.count('GatherContent')>0:
                Gather = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherBiblio')>0:
                GatherBiblio = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherPatent')>0:
                GatherPatent = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherFamilly')>0:
                GatherFamilly = ReturnBoolean(lig.split(':')[1].strip())

rep = ndf2

# the list of keys for filtering for pivitable
#clesRef = ['label', 'citations', 'title', 'year','priority-active-indicator', 
#'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4', 
#'IPCR7', "Inventor-Country", "Applicant-Country",  "CPC", 'Citations', 'references'] # "equivalents", "CitedBy"
clesRef = ['label', 'title', 'year','priority-active-indicator', 
'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4', 
'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", "CPC", 
u'references',  # the number of refences into the document len(CitP) + len(CitO)
u'Citations',   # the number of citations granted by the document
#u'CitedBy',     # the list of docs (patents) cititng this patent
#'CitP',         # the patents cited by this patent
#'CitO'          # the other docs cited by this patent
] #"citations"

ListBiblioPath = '..//DONNEES//'+rep+'//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'#List
ResultPathContent = '..//DONNEES//'+rep #+'//PatentContentsHTML'
temporPath = '..//DONNEES//'+rep+'//tempo'

import os, collections

#filterFile = [fi for fi in os.listdir(ListBiblioPath) if fi.count('Expanded')]
srcFile = [fi for fi in os.listdir(ListBiblioPath)]

for ndf in srcFile:
    with open(ListBiblioPath+'//'+ndf, 'r') as data:
        DataBrevet = pickle.load(data)
    
    if isinstance(DataBrevet, collections.Mapping):
        #data = DataBrevet
        LstBrevet = DataBrevet['brevets']    
        if DataBrevet.has_key('number'):
            print "Found ", DataBrevet["number"], " patents! Formating to HMTL tables"
    else:
        print "Please delete you datat directory... incompatible old stuf in it"
    LstExp = [] 
    LstExp2 = [] 
    #just for testing las fnction in gathered should deseapear soon
    if ndf.count('Families')>0:
    #clesRef2 = ['label', 'year',  'priority-active-indicator', 'kind', 'applicant', 'country', 'inventor',  "CPC", 'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country", 'Citations'] #'citations','representative',
        clesRef2 = ['label', 'year',#'priority-active-indicator', 
        'prior-Date', 'family lenght',
         'kind', 'applicant', 'country', 'inventor', 'representative', "CPC", 'IPCR4', 
        'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", 
        u'references',  # the number of refences into the document len(CitP) + len(CitO)
        u'Citations',   # the number of citations granted by the document
        #u'CitedBy',     # the list of docs (patents) cititng this patent
        #'CitP',         # the patents cited by this patent
        #'CitO'          # the other docs cited by this patent
        ] #"citations"
    else:
        clesRef2 = ['label', 'year',#'priority-active-indicator', 
    'prior-Date',
     'kind', 'applicant', 'country', 'inventor', 'representative', "CPC", 'IPCR4', 
    'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", 
    u'references',  # the number of refences into the document len(CitP) + len(CitO)
    u'Citations',   # the number of citations granted by the document
    u'CitedBy',     # the list of docs (patents) cititng this patent
    'CitP',         # the patents cited by this patent
    'CitO'          # the other docs cited by this patent
    ] #"citations"
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
        tempoBrev = DecoupeOnTheFly(tempo2, [])
        for pat in tempoBrev:       
            if pat not in LstExp2:
                LstExp2.append(pat)
    print "Expanded to ", len(LstExp2), " monovaluated patents"
#    with open(ListBiblioPath + '//Expanded' + ndf, 'w') as SavFic:
#        pickle.dump(LstExp2, SavFic)
    
    Exclude = []
    print "entering formating html process"
    dicoRes = dict()
    dicoRes['data'] = LstExp
    #contenu = json.dumps(dicoRes, indent = 3) #ensure_ascii=True, 
    contenu2 = json.dumps(LstExp2,  indent = 3) #ensure_ascii=True,
    
    
    
    with open(ResultPathContent + '//' + ndf+'Pivot.json', 'w') as resFic:
        resFic.write(contenu2)
    
    FichierHtml=ndf+'.html'
    if ndf.startswith('Families'):
        ModelePivot = "ModeleFamillePivot.html"
    else:
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
