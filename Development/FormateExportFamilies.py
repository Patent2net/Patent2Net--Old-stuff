# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import pickle
import bs4
from bs4.dammit import EntitySubstitution
from OPS2NetUtils2 import ExtractClassificationSimple2, ReturnBoolean, Decoupe


#On récupère la requête et les noms des fichiers de travail
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
ndf = 'Families'+ndf
clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior']


ListBiblioPath = '..//DONNEES//'+rep+'//PatentBiblios'#Biblio'
ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'#List
ResultPathContent = '..//DONNEES//'+rep #+'//PatentContentsHTML'
temporPath = '..//DONNEES//'+rep+'//tempo'

        

with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
with open(ListPatentPath+'//'+rep, 'r') as data: # take the request only present in PatentList
    DataBrevet = pickle.load(data)

if isinstance(LstBrevet, dict):
    data = LstBrevet
    LstBrevet = data['brevets']    
    if data.has_key('requete'): 
        DataBrevet['requete'] = data["requete"]
    if data.has_key('number'):
        print "Found ", data["number"], " patents! Formating to HMTL tables"

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
                        tempoClass = ExtractClassificationSimple2(classif)
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
                temp = unicode(brev[cle]).replace('[','').replace(']', '')
                tempo2 [cle] = brev[cle]
                formate = EntitySubstitution()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp

                
        else:
            tempo[cle] = ''
            tempo2 [cle] = ''
    tempoBrev = Decoupe(tempo2)        
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
with codecs.open(ResultPathContent + '//' + ndf+'.csv', 'w', 'utf-8') as resFic:
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

with open(ResultPathContent + '//' + ndf+'.json', 'w') as resFic:
    resFic.write(contenu)

with open(ResultPathContent + '//' + ndf+'Pivot.json', 'w') as resFic:
    resFic.write(contenuPivotable)

with open(Modele, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'.json' )  
    html = html.replace('**requete**', DataBrevet['requete'])
    html = html.replace('**PivotFamille**', ndf+'Pivot.html' )
    html = html.replace('**fichierHtml**', ndf+'.html' )
    with open(ResultPathContent + '//'  +ndf+'.html', 'w') as resFic:
        resFic.write(html)

ModelePivot = "ModeleFamillePivot.html"
FichierHtml=ndf+'.html'
with open(ModelePivot, "r") as Source:
    html = Source.read()
    html = html.replace('**fichier**', ndf+'Pivot.json' )  
    html = html.replace('**requete**', DataBrevet['requete'])
    html = html.replace('**FichierHtml**', FichierHtml.replace('Families',''))
    html = html.replace('**FichierHtmlFamille**', FichierHtml)
    with open(ResultPathContent + '//' + ndf+'Pivot.html', 'w') as resFic:
        resFic.write(html)
        
        
        
with open("searchScript.js", 'r') as Source:
    js = Source.read()
    js = js.replace('***fichierJson***', ndf+'.json')
    js = js.replace('{ "data": "application-ref"},', '') 
    with open(ResultPathContent + '//' + 'searchScript.js', 'w') as resFic:
        resFic.write(js)

URLs = ResultPathContent+'//'+ndf.replace('Families','')+'.html '+ ResultPathContent+'//'+ndf.replace('Families','')+'Pivot.html '

URLs += ResultPathContent+'//'+FichierHtml +' ' +ResultPathContent+'//'+ndf+'Pivot.html'

#os.system('start firefox -url '+ URLs.replace('//','/') )
