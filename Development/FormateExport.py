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

rep = ndf

#if ndf.count('Families')>0:
#    clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']
#else:
clesRef = ['label', 'titre', 'date', 'citations', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative']


ListBiblioPath = '..//DONNEES//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//PatentLists'#List
ResultPathContent = '..//DONNEES//PatentContentsHTML'
temporPath = 'tempo'


try:
    os.makedirs(ResultPathContent + '//' + ndf)
except: 
    pass

with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
with open(ListPatentPath+'//'+ndf, 'r') as data:
    DataBrevet = pickle.load(data)

#we filter data for exporting most significant values
LstExp = [] 
LstExp2 = [] 
for brev in LstBrevet:
    brev["date"] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
    tempo = dict()
    tempo2 = dict()
    for cle in clesRef:
        if brev[cle] is not None and brev[cle] != 'N/A':
            if isinstance(brev[cle], list):
                temp = ' '.join(brev[cle])
                temp2 = brev[cle]
            elif cle =='titre':
                try:
                    temp = unicode(brev[cle], 'utf8', 'replace').replace('[','').replace(']', '').lower().capitalize()
                    temp2 = unicode(brev[cle], 'utf8', 'replace').lower().capitalize()
                except:
                    temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                    temp2 = unicode(brev[cle]).lower().capitalize()
            else:
                try:
                    temp = unicode(brev[cle], 'utf8', 'replace').replace('[','').replace(']', '')
                    temp2 = unicode(brev[cle], 'utf8', 'replace')
                except:
                    temp = unicode(brev[cle]).replace('[','').replace(']', '')
                    temp2 = unicode(brev[cle])
            formate = EntitySubstitution()
            soup = bs4.BeautifulSoup(temp)
            temp = soup.text
            tempo[cle] = temp
            if isinstance(temp2, list):
                temp2 = [bs4.BeautifulSoup(unit).text for unit in temp2]
        
            else:
                soup = bs4.BeautifulSoup(temp2)
                temp2 = soup.text
            tempo2[cle] = temp2
        else:
            tempo[cle] = ''
            tempo2[cle] = ''
    
    LstExp.append(tempo)
    LstExp2.append(tempo2)
    
Exclude = []

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

with open(ResultPathContent + '//' + rep+ '//' +ndf+'.json', 'w') as resFic:
    resFic.write(contenu)

with open(ResultPathContent + '//' + rep+ '//' +ndf+'Pivot.json', 'w') as resFic:
    resFic.write(contenu2)
with open(Modele, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'.json' )  
    
    html = html.replace('**fichierHtmlFamille**', 'Families'+ndf+'.html' )
    html = html.replace('**fichierPivot**', ndf+'Pivot.html' )

    html = html.replace('**requete**', DataBrevet['requete'])
    with open(ResultPathContent + '//' + rep+ '//' +ndf+'.html', 'w') as resFic:
        resFic.write(html)

FichierHtml=ndf+'.html'
ModelePivot = "Pivot.html"
with open(ModelePivot, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'Pivot.json' )  
    html = html.replace('**requete**', DataBrevet['requete'])
    html = html.replace('**FichierHtml**', FichierHtml)
    html = html.replace('**FichierHtmlFamille**', 'Families'+FichierHtml)
    with open(ResultPathContent + '//' + rep+ '//' +ndf+'Pivot.html', 'w') as resFic:
        resFic.write(html)
