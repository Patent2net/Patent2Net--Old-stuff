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
import sys

ndf = sys.argv[1]

rep = ndf.replace('Families', '')

clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']


ListBiblioPath = '..//DONNEES//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//PatentLists'#List
ResultPathContent = '..//DONNEES//PatentContentsHTML'
temporPath = 'tempo'


try:
    os.makedirs(ResultPathContent + '//' + rep)
except: 
    pass

with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
with open(ListPatentPath+'//'+ndf.replace('Families', ''), 'r') as data: # take the request only present in PatentList
    DataBrevet = pickle.load(data)

#we filter data for exporting most significant values
LstExp = [] 
LstExp2 = [] 
for brev in LstBrevet:
    brev["date"] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
    tempo = dict() # this one for DataTable
    tempo2 = dict() #the one for pitable
    for cle in clesRef:
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list):
                temp = unicode(' '.join(brev[cle]))
                tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev[cle]]
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
            
            elif cle =='titre':
                temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                temp = unicode(brev[cle]).lower().capitalize()
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo2[cle] = temp
            else:
                temp = unicode(brev[cle]).replace('[','').replace(']', '')
                
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                temp = unicode(brev[cle])
                
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo2 [cle] = temp
                
        else:
            tempo[cle] = ''
            tempo2[cle] = ''
    LstExp.append(tempo)
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