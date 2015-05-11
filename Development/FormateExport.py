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
from OPS2NetUtils2 import CleanPatent, ReturnBoolean, Decoupe, SeparateCountryField,CleanPatentOthers

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
clesRef = ['label', 'citations', 'titre', 'date','priority-active-indicator', 'IPCR11', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country"] #"citations"


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
    tempo = CleanPatent(brev)
    brevet= SeparateCountryField(tempo)
    #cleaning classification
    tempo= CleanPatentOthers(brevet)
    ##
                
    LstExp.append(tempo)
    
    
#    tfiltering against keys
    tempo2=dict()
    clesRef2 = ['label', 'date',  'priority-active-indicator', 'portee', 'applicant', 'pays', 'inventeur',  'IPCR4', 'IPCR7', "Inventor-Country", "Applicant-Country"] #'citations','representative',
    for ket in clesRef2:
        tempo2[ket] = tempo[ket]
    tempoBrev = Decoupe(tempo2)
    for nb in tempoBrev:
        brev2 = CleanPatentOthers(tempoBrev[nb])
        tempo2 = dict() #the one for pitable
        for cle in clesRef2:
            if brev2[cle] is not None and brev2[cle] != 'N/A' and brev2[cle] != 'UNKNOWN':
                if isinstance(brev2[cle], list) and len(brev2[cle])>1:
                    tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev2[cle] if unit !='N/A']
                elif isinstance(brev2[cle], list) and len(brev2[cle]) == 1:
                    tempo2[cle] = [bs4.BeautifulSoup(brev2[cle][0]).text.replace('N/A', '')]
                elif cle=='date':
                    try:
                        tempo2[cle] = brev2[cle].split('-')[0]
                    except:
                        if brev2[cle] is not None: #no date in data
                            tempo2[cle] = brev2[cle][0:4]
                    
                if cle =='titre':
                    pass # no need of titles
                if cle == 'applicant' or cle == 'inventeur':
                    temp = unicode(brev2[cle])
                    if temp.count('[')>0:
                        tempo2 [cle] = temp.split('[')[0]
                    else:
                        tempo2 [cle] = temp
                elif cle not in ['applicant', 'inventeur', 'date', 'titre']:
                    temp = unicode(brev2[cle])
                    
                    formate = EntitySubstitution()
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo2 [cle] = temp.replace('N/A', '')
                    
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
