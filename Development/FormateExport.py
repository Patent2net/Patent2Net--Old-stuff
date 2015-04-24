# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import os
import pickle
import bs4
from bs4.dammit import EntitySubstitution
from OPS2NetUtils2 import ExtractClassificationSimple2, ReturnBoolean, Decoupe

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
clesRef = ['label', 'citations', 'titre', 'date','priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country"] #"citations"


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
for brev in LstBrevet:
    tempo = dict() # this one for DataTable
    tempo2 = dict() #the one for pitable
    PaysInv= [] #new field
    PaysApp = []
    if brev['inventeur'] is not None:
        
        if isinstance(brev['inventeur'], list):
            tempoInv = []
            for inv in brev['inventeur']:
                tempPaysInv = inv.split('[')
                for kk in range(1, len(tempPaysInv), 2):
                    PaysInv.append(tempPaysInv[kk].replace(']',''))
                tempoInv.append(tempPaysInv[0].strip())
            brev["inventeur"] = tempoInv
                
        else:
            tempPaysInv = brev['inventeur'].split('[')
            for kk in range(1, len(tempPaysInv), 2):
                PaysInv.append(tempPaysInv[kk].replace(']',''))
            brev["inventeur"] = tempPaysInv[0].strip()
    if brev['applicant'] is not None:
        if isinstance(brev['applicant'], list):
            tempoApp = []
            for APP in brev['applicant']:
                tempPaysApp = APP.split('[')
                for kk in range(1, len(tempPaysApp), 2):
                    PaysApp.append(tempPaysApp[kk].replace(']',''))
                tempoApp.append(tempPaysApp[0].strip())
            brev["applicant"] = tempoApp
        else:

            tempPaysApp = brev['applicant'].split('[')
            for kk in range(1, len(tempPaysApp), 2):
                PaysApp.append(tempPaysApp[kk].replace(']',''))
            brev["applicant"] = tempPaysApp[0].strip()
    brev["Inventor-Country"] = list(set(PaysInv))
    brev["Applicant-Country"] = list(set(PaysApp))
    if len(brev["Inventor-Country"]) == 1:
        brev["Inventor-Country"] = brev["Inventor-Country"][0]
    if len(brev["Applicant-Country"]) == 1:
        brev["Applicant-Country"] = brev["Applicant-Country"][0]
    for cle in clesRef:
        if cle not in ['representative', "citations"]:
            if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
                if isinstance(brev[cle], list) and cle == 'classification':
                    for classif in brev['classification']:
                        tempoClass = ExtractClassificationSimple2(classif)
                        for cle2 in tempoClass.keys():
                            if cle2 == 'classification':
                                if tempo.has_key(cle2) and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
                                    tempo[cle2] = [tempo[cle2]]
                                    tempo[cle2].append(tempoClass[cle2])
                                elif tempo.has_key(cle2) and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    tempo[cle2] = [tempoClass[cle2]]
                            elif cle2 in tempo.keys():
                                if tempoClass[cle2] not in tempo[cle2]:
                                    #tempo[cle] = []
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    pass
                                if tempoClass[cle2] not in tempo2[cle2]:   
                                    tempo2[cle2].append(tempoClass[cle2])
                                else:
                                    pass
                            else:
                                tempo[cle2] = []
                                tempo2[cle2] = []
                                tempo[cle2].append(tempoClass[cle2])
                                tempo2[cle2].append(tempoClass[cle2])
                elif isinstance(brev[cle], list):
                    temp = unicode(' '.join(brev[cle]))
                    tempo[cle] = temp
                    tempo2[cle] = brev[cle]
                elif cle =='titre':
                                 
                    temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                    formate = EntitySubstitution()
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo[cle] = temp
                    #tempo2[cle] = temp  #we do not need titles in pivotable
                elif cle =='date':
                    tempo[cle] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
                    tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
                elif cle =='classification' and brev['classification'] != '':
                        tempoClass = ExtractClassificationSimple2(brev['classification'])
                        for cle in tempoClass.keys():
                            if cle in tempo.keys() and tempoClass[cle] not in tempo[cle]:
                                tempo[cle].append(tempoClass[cle])
                                tempo2[cle].append(tempoClass[cle])
                            else:
                                tempo[cle] = []
                                tempo2[cle] = []
                                tempo[cle].append(tempoClass[cle])
                                tempo2[cle].append(tempoClass[cle])
                    
                else:
                    temp = unicode(brev[cle])#.replace('[','').replace(']', '')
                    
                    formate = EntitySubstitution()
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo[cle] = temp
                    tempo2[cle] = brev[cle]
                    
            else:
                tempo[cle] = ''
                tempo2[cle] = ''
            
    LstExp.append(tempo)
    
    tempoBrev = Decoupe(tempo2)
#    tempoBrev = Check(tempoBrev) # doublons enlevés
    clesRef2 = ['label', 'date',  'priority-active-indicator', 'portee', 'applicant', 'pays', 'inventeur',  'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country"] #'citations','representative',

    for brev2 in tempoBrev:
        tempo2 = dict() #the one for pitable
        for cle in clesRef2:
            if brev2[cle] is not None and brev2[cle] != 'N/A' and brev2[cle] != 'UNKNOWN':
                if isinstance(brev2[cle], list) and len(brev2[cle])>1:
                    tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev2[cle]]
                elif isinstance(brev2[cle], list) and len(brev2[cle]) == 1:
                    tempo2[cle] = [bs4.BeautifulSoup(brev2[cle][0]).text]
                                    
                if cle =='titre':
                    pass # no need of titles
                if cle == 'applicant' or cle == 'inventeur':
                    temp = unicode(brev2[cle])
                    if temp.count('[')>0:
                        tempo2 [cle] = temp.split('[')[0]
                    else:
                        tempo2 [cle] = temp
                else:
                    temp = unicode(brev2[cle])
                    
                    formate = EntitySubstitution()
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo2 [cle] = temp
                    
            else:
                tempo2[cle] = ''
        if tempo2 not in LstExp2:
            LstExp2.append(tempo2)
    print len(LstExp2),
    
Exclude = []
print "entering formating html process"
dicoRes = dict()
dicoRes['data'] = LstExp
contenu = json.dumps(dicoRes, ensure_ascii=True, indent = 3)
contenu2 = json.dumps(LstExp2, ensure_ascii=True, indent = 3)

import codecs
#if rep != ndf:
#    if ndf.lower() == 'families'+rep.lower():
#        #ndf = 'Families'+ ndf
#        Modele = "ModeleFamille.html"
#else:
#    
Modele = "Modele.html"
with codecs.open(ResultPathContent + '//'  +ndf+'.csv', 'w', 'utf-8') as resFic:
    entete = ''.join([u +';' for u in clesRef]) +'\n'
    resFic.write(entete)
    for brev in LstBrevet:
        ligne = ''
        for cle in clesRef:
            if isinstance(brev[cle], list):
                temp=''
                for k in brev[cle]:
                    temp += k + ' '
                try:
                    ligne += unicode(temp, 'utf8', 'replace') +';'
                except:
                    try:
                        ligne += unicode(temp, 'cp1252', 'replace') +';' 
                    except:
                        try:
                            ligne += unicode(temp, 'latin1', 'replace') +';'
                        except:
                            try:
                                ligne += unicode(temp) +';'
                            except:
                                print 'paté'
            else:
                try:
                    ligne += unicode(brev[cle], 'utf8', 'replace') +';'
                except:
                    ligne += unicode(brev[cle]) +';'
                    
        ligne += '\n'
        resFic.write(ligne)

with open(ResultPathContent + '//' +ndf+'.json', 'w') as resFic:
    resFic.write(contenu)

with open(ResultPathContent + '//' + ndf+'Pivot.json', 'w') as resFic:
    resFic.write(contenu2)
with open(Modele, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'.json' )  
    
    html = html.replace('**fichierHtmlFamille**', 'Families'+ndf+'.html' )
    html = html.replace('**fichierPivot**', ndf+'Pivot.html' )

    html = html.replace('**requete**', DataBrevet['requete'].replace('"', ''))
    with open(ResultPathContent + '//' + ndf+'.html', 'w') as resFic:
        resFic.write(html)

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

with open("scriptSearch.js", 'r') as Source:
    js = Source.read()
    js = js.replace('***fichierJson***', ndf+'.json')
    js = js.replace('{ "data": "application-ref"},', '') 
    with open(ResultPathContent + '//' + 'scriptSearch.js', 'w') as resFic:
        resFic.write(js)

#os.system('start firefox -url '+ URLs.replace('//','/') )
