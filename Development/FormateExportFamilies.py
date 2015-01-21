# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import sys
import os
import pickle
import bs4
from bs4.dammit import EntitySubstitution
import OPS2NetUtils2

ndf = sys.argv[1]

rep = ndf.replace('Families', '')

clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']


ListBiblioPath = '..//DONNEES//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//PatentLists'#List
ResultPathContent = '..//DONNEES//PatentContentsHTML'
temporPath = 'tempo'

#def Decoupe(dico):
#    """will return a list of dictionnary patents monovaluated as long as the product of multivalued entries"""
#    Res = []
#    import copy
#    temporar = copy.deepcopy(dico)    
#    dicoRes = dict()
#    for cle in temporar.keys():
#        if isinstance(dico[cle], list) and len(dico[cle])>1:
#            dicoTemp = copy.deepcopy(dico)
#            for cont in dico[cle]:
#                dicoTemp[cle] = cont
#                for k in Decoupe(dicoTemp):
#                    if k not in Res:
#                        Res.append(k)
#        elif isinstance(dico[cle], list) and len(dico[cle]) == 1:
#            dicoRes[cle] = dico[cle][0]
#        else:
#            dicoRes[cle] = dico[cle]
#    if len(dicoRes.keys()) == len(dico.keys()):
#        if dicoRes not in Res:
#            Res.append(dicoRes)
#    return Res
#    
        
try:
    os.makedirs(ResultPathContent + '//' + rep)
except: 
    pass

with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
with open(ListPatentPath+'//'+rep, 'r') as data: # take the request only present in PatentList
    DataBrevet = pickle.load(data)

#def Check(lstDicos):
#    assert isinstance(lstDicos, list)
#    Res = []
#    
#    for ind in range(len(lstDicos)):
#        notUnic = False
#        for dico2 in lstDicos[ind+1:]:
#            if lstDicos[ind] == dico2:
#                notUnic = True
#                break
#        if not notUnic:
#            Res.append(lstDicos[ind])
#    return Res
#we filter data for exporting most significant values
LstExp = [] 
LstExp2 = [] 
for brev in LstBrevet:
    
    tempo = dict() # this one for DataTable
    tempo2 = dict() #the one for pitable
    for cle in clesRef:
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list):
                if cle == 'classification':
                    for classif in brev['classification']:
                        tempoClass = OPS2NetUtils2.ExtractClassificationSimple2(classif)
                        for cle2 in tempoClass.keys():
                            if cle2 == 'classification':
                                if tempo.has_key(cle2):
                                    tempo[cle2] = [tempo[cle2]].append(tempoClass[cle2])
                                else:
                                    tempo[cle2] = tempoClass[cle2]                           
                            elif cle2 in tempo.keys() and tempoClass[cle2] not in tempo[cle2]:
                                    #tempo[cle] = []
                                tempo[cle2].append(tempoClass[cle2])
                                tempo2[cle2].append(tempoClass[cle2])
                            else:
                                tempo[cle2] = []
                                tempo2[cle2] = []
                                tempo[cle2].append(tempoClass[cle2])
                                tempo2[cle2].append(tempoClass[cle2])
                else:                
                    temp = unicode(' '.join(brev[cle]))
                    tempo[cle] = temp
                    tempo2 [cle] = brev[cle]
            elif cle =='titre':
                temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                #tempo2 [cle] = temp
            elif cle =='date':
                tempo[cle] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
                tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
            elif cle =='classification' and brev['classification'] != u'':
                tempoClass = OPS2NetUtils2.ExtractClassificationSimple2(brev['classification'])
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
                temp = unicode(brev[cle]).replace('[','').replace(']', '')
                tempo2 [cle] = brev[cle]
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp

                
        else:
            tempo[cle] = ''
            tempo2 [cle] = ''
    tempoBrev = OPS2NetUtils2.Decoupe(tempo2)        
    LstExp.append(tempo)
    clesRef2 = ['label', 'date', 'citations','family lenght', 'priority-active-indicator', 'IPCR4', 'IPCR7', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']



    for brev2 in tempoBrev:
        tempo2 = dict() #the one for pitable
        for cle in clesRef2:
            if brev2[cle] is not None and brev2[cle] != 'N/A' and brev2[cle] != 'UNKNOWN':
                if isinstance(brev2[cle], list):
                    tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev2[cle]]
                               
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
        
    
Exclude = []

dicoRes = dict()
dicoRes['data'] = LstExp
contenu = json.dumps(dicoRes, ensure_ascii=True, indent = 3)
contenuPivotable = json.dumps(LstExp2, ensure_ascii=True, indent = 3)
import codecs
#if rep != ndf:
#    if ndf.lower() == 'families'+rep.lower():
#        #ndf = 'Families'+ ndf
Modele = "ModeleFamille.html"
#else:
#    Modele = "Modele.html"
with codecs.open(ResultPathContent + '//' + rep+ '//' +ndf+'.csv', 'w', 'utf-8') as resFic:
    entete = ''.join([u +';' for u in clesRef]) +'\n'
    resFic.write(entete)
    for brev in LstBrevet:
        ligne = ''
        for cle in clesRef:
            if isinstance(brev[cle], list):
                temp=''
                for k in brev[cle]:
                    temp += k + ' '
                ligne += unicode(temp) +';'
            else:
                ligne += unicode(brev[cle]) +';'
        ligne += '\n'
        resFic.write(ligne)

with open(ResultPathContent + '//' + rep+ '//' +ndf+'.json', 'w') as resFic:
    resFic.write(contenu)

with open(ResultPathContent + '//' + rep+ '//' +ndf+'Pivot.json', 'w') as resFic:
    resFic.write(contenuPivotable)

with open(Modele, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'.json' )  
    html = html.replace('**requete**', DataBrevet['requete'])
    html = html.replace('**PivotFamille**', ndf+'Pivot.html' )
    html = html.replace('**fichierHtml**', ndf+'.html' )
    with open(ResultPathContent + '//' + rep+ '//' +ndf+'.html', 'w') as resFic:
        resFic.write(html)

ModelePivot = "Pivot.html"
FichierHtml=ndf+'.html'
with open(ModelePivot, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'Pivot.json' )  
    html = html.replace('**requete**', DataBrevet['requete'])
    html = html.replace('**FichierHtml**', FichierHtml.replace('Families',''))
    html = html.replace('**FichierHtmlFamille**', FichierHtml)
    with open(ResultPathContent + '//' + rep+ '//' +ndf+'Pivot.html', 'w') as resFic:
        resFic.write(html)