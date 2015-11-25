# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:57:19 2015

@author: dreymond
"""



import json
import os
import pickle
#from bs4.dammit import EntitySubstitution
from P2N_Lib import ReturnBoolean

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

#if ndf.count('Families')>0:
#    clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']
#else:
#clesRef = ['label', 'titre', 'date', 'citations', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'IPCR4', 'IPCR7']
#clesRef =['status', 'Inventor-Country', 'citations', 'Applicant-Country', 'priority-active-indicator', 'IPCR1', 'portee', 'IPCR3', 'applicant', 'IPCR4', 'IPCR7', 'label', 'IPCR11', 'abs', 'titre', 'application-ref', 'pays', 'date', 'publication-ref', 'inventeur', 'representative']

ListBiblioPath = '..//DONNEES//'+rep+'//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'#List
ResultPathContent = '..//DONNEES//'+rep #+'//PatentContentsHTML'
temporPath = '..//DONNEES//'+rep+'//tempo'


try:
    os.makedirs(ResultPathContent)
except: 
    pass

with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
with open(ListPatentPath+'//'+ndf, 'r') as data:
    DataBrevet = pickle.load(data)

if isinstance(LstBrevet, dict):
    data = LstBrevet
    LstBrevet = data['brevets']    
    if data.has_key('requete'): 
        DataBrevet['requete'] = data["requete"]
    if "requete" not in DataBrevet.keys():
        DataBrevet['requete'] = "?"
    if data.has_key('number'):
        print "Found ", data["number"], " patents! Formating to HMTL Cartography (Beta)"

# the list of keys in database
clesRef = ['label', 'title', 'year','priority-active-indicator', 
'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4', 
'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", "CPC", u'references', u'Citations', u'CitedBy']

NomPays = dict()
NomTopoJSON = dict()
with open('NameCountryMap.csv', 'r') as fic:  
    #2 means using short name...
    for lig in fic.readlines():
        li = lig.strip().split(';')    
        NomPays[li[2].upper()] = li[1]
        NomTopoJSON[li[1]] = li[0]
        NomPays[li[1]] = li[2].upper() #using same dict for reverse mapping
cptPay = dict()
for field in ['Applicant-Country', 'Inventor-Country']:
    for bre in LstBrevet:
        if bre[field] != '':
            if isinstance(bre[field], list):
                for tempo in bre[field]:
                    if tempo in NomPays.keys(): #aptent country in name (ouf)
                        if cptPay.has_key(NomPays[tempo]): #has it been found yet ?
                            cptPay[NomPays[tempo]] += 1 #so add one
                        else: #set it intead to one
                            cptPay[NomPays[tempo]] = 1
                    elif tempo =='SU':
                        if cptPay.has_key('RU'): #has it been found yet ?
                            cptPay[NomPays['RU']] += 1 #so add one
                        else: #set it intead to one
                            cptPay[NomPays['RU']] = 1
                    else:
                        print tempo, " country not found"
            elif bre[field] in NomPays.keys(): #patent country in name (saved :-)
                if cptPay.has_key(NomPays[bre[field]]): #has it been found yet ?
                    cptPay[NomPays[bre[field]]] += 1 #so add one
                else: #set it intead to one
                    cptPay[NomPays[bre[field]]] = 1
            else:
                print  bre[field], " country not found"
    dico =dict()
    for k in cptPay.keys():
        tempo = dict()
        tempo["value"] = cptPay[k]
        tempo["name"] = k
        tempo["country"] = NomTopoJSON[k]
        if "data" in dico.keys():
            dico["data"].append(tempo)
        else:
            dico["data"]=[tempo]
    nameFic = field.split('-')[0]
    with open(ResultPathContent+'//'+rep+"Map"+nameFic+ ".json", "w") as fic:
        json.dump(dico, fic)
        resJsonName = rep+"Map"+nameFic+ ".json" 
    with open("ModeleCartoDeposant.html") as fic:
        html = fic.read()
    html = html.replace("***Field***", nameFic)
    html = html.replace("***requete***", DataBrevet["requete"])
    html = html.replace("ficJson", '"'+resJsonName+'"')
    
    with open(ResultPathContent+'//'+rep+"Carto"+nameFic+ ".html", "w") as fic:
        fic.write(html)
#due to limit of D3, countries ressources are necessary placed
# in same working directory... other solution is to start an http server
# http://stackoverflow.com/questions/17077931/d3-samples-in-a-microsoft-stack
    
#with open(ResultPathContent+'//'+"countries.json", "w") as fic:
#    with open('countries.json', 'r') as fic2:
#        tempo = fic2.read()
#        fic.write(tempo)
