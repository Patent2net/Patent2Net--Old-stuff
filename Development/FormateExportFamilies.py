# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import pickle
import bs4
from bs4.dammit import EntitySubstitution
from OPS2NetUtils2 import ExtractClassificationSimple2, ReturnBoolean, Decoupe, CleanPatent
import copy

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
clesRef = ['label',  'titre', 'date', 'citations','family lenght', 'priority-active-indicator', 'classification', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior', "Inventor-Country", "Applicant-Country"]


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


#checking patent list if some patents are missing
with open(ListBiblioPath+'//'+ndf.replace('Families', ''), 'r') as data:
    LstBrevetComp = pickle.load(data)
for bb in LstBrevetComp:
    if bb not in LstBrevet and isinstance(bb, dict):
        #next will cause inconsistency of data...
        # to append needs to gather (again?) missing data
        #LstBrevet.append(bb)
        print bb['label']


#we filter data for exporting most significant values
LstExp = [] 
LstExp2 = [] 
for brev in LstBrevet:
    #cleaning
   
    brev= CleanPatent(brev)
    ##
    
    tempo = brev # this one for DataTable
    tempo2 = dict() #the one for pitable
    PaysInv= [] #new field
    PaysApp = []
#    if brev['inventeur'] is not None:
#        
#        if isinstance(brev['inventeur'], list):
#            tempoInv = []
#            for inv in brev['inventeur']:
#                tempPaysInv = inv.split('[')
#                if isinstance(tempPaysInv, list):
#                    for kk in range(1, len(tempPaysInv), 2):
#                        PaysInv.append(tempPaysInv[kk].replace(']',''))
#                    tempoInv.append(tempPaysInv[0].strip())
#                else:
#                    tempoInv.append(tempPaysInv.strip())
#            brev["inventeur"] = tempoInv
#                
#        else:
#            tempPaysInv = brev['inventeur'].split('[')
#            if isinstance(tempPaysInv, list):
#                for kk in range(1, len(tempPaysInv), 2):
#                    PaysInv.append(tempPaysInv[kk].replace(']',''))
#                brev["inventeur"] = tempPaysInv[0].strip()
#            else:
#                tempoInv.append(tempPaysInv.strip())
#    if brev['applicant'] is not None:
#        
#        if isinstance(brev['applicant'], list):
#            tempoApp = []
#            for APP in brev['applicant']:
#                tempPaysApp = APP.split('[')
#                if isinstance(tempPaysApp, list):
#                    for kk in range(1, len(tempPaysApp), 2):
#                        PaysApp.append(tempPaysApp[kk].replace(']',''))
#                    tempoApp.append(tempPaysApp[0].strip())
#                else:
#                    tempoApp.append(tempPaysApp.strip())
#            brev["applicant"] = tempoApp
#        else:
#
#            tempPaysApp = brev['applicant'].split('[')
#            if isinstance(tempPaysApp, list):
#                for kk in range(1, len(tempPaysApp), 2):
#                    PaysApp.append(tempPaysApp[kk].replace(']',''))
#                brev["applicant"] = tempPaysApp[0].strip()
#            else:
#                brev["applicant"] = tempPaysApp.strip()
#    brev["Inventor-Country"] = list(set(PaysInv))
#    brev["Applicant-Country"] = list(set(PaysApp))
#    if len(brev["Inventor-Country"]) == 1:
#            brev["Inventor-Country"] = brev["Inventor-Country"][0]
#    if len(brev["Applicant-Country"]) == 1:
#        brev["Applicant-Country"] = brev["Applicant-Country"][0]
#    if isinstance(brev["Inventor-Country"], list) and len(brev["Inventor-Country"]) == 0:
#        brev["Inventor-Country"] = ""
#    if isinstance(brev["Applicant-Country"], list) and len(brev["Applicant-Country"]) == 0: 
#        brev["Applicant-Country"] = ""
#    
#    for cle in clesRef:
#        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
#            if isinstance(brev[cle], list):
#                if cle == 'classification':
#                    for classif in brev['classification']:
#                        tempoClass = ExtractClassificationSimple2(classif)
#                        for cle2 in tempoClass.keys():
#                            if cle2 == 'classification':
#                                if tempo.has_key(cle2) and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
#                                    tempo[cle2] = [tempo[cle2]]
#                                    tempo[cle2].append(tempoClass[cle2])
#                                elif tempo.has_key(cle2) and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
#                                    tempo[cle2].append(tempoClass[cle2])
#                                else:
#                                    tempo[cle2] = [tempoClass[cle2]]
#                            elif cle2 in tempo.keys():
#                                if tempoClass[cle2] not in tempo[cle2]:
#                                    #tempo[cle] = []
#                                    tempo[cle2].append(tempoClass[cle2])
#                                else:
#                                    pass
##                                if tempoClass[cle2] not in tempo2[cle2]:   
##                                    tempo2[cle2].append(tempoClass[cle2])
##                                else:
##                                    pass
#                            else:
#                                tempo[cle2] = []
#                                tempo2[cle2] = []
##                                tempo[cle2].append(tempoClass[cle2])
##                                tempo2[cle2].append(tempoClass[cle2])
#
#                else:                
#                    temp = [unicode(a) for a in brev[cle]]
#                    tempo[cle] = temp
#                    tempo2 [cle] = brev[cle]
#            elif cle =='titre':
#                temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
#                formate = EntitySubstitution()
#                soup = bs4.BeautifulSoup(temp)
#                temp = soup.text
#                tempo[cle] = temp
#                #tempo2 [cle] = temp
#            elif cle =='date':
#                tempo[cle] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
#                tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
#            elif cle =='classification' and brev['classification'] != u'':
#                tempoClass = ExtractClassificationSimple2(brev['classification'])
#                for cle in tempoClass.keys():
#                    if cle in tempo.keys() and tempoClass[cle] not in tempo[cle]:
#                        tempo[cle].append(tempoClass[cle])
#                        tempo2[cle].append(tempoClass[cle])
#                    else:
#                        tempo[cle] = []
#                        tempo2[cle] = []
#                        tempo[cle].append(tempoClass[cle])
#                        tempo2[cle].append(tempoClass[cle])
#                            
#            else:
#                temp = unicode(brev[cle]).replace('[','').replace(']', '')
#                tempo2 [cle] = brev[cle]
#                formate = EntitySubstitution()
#                soup = bs4.BeautifulSoup(temp)
#                temp = soup.text
#                tempo[cle] = temp
#
#                
#        else:
#            tempo[cle] = ''
#            tempo2 [cle] = ''
    tempo = CleanPatent(tempo)
    tempo2 = copy.deepcopy(tempo) #ugly
    tempoBrev = Decoupe(tempo2)        
    LstExp.append(tempo)
    clesRef2 = ['label', 'date', 'citations','family lenght', 'priority-active-indicator', 'IPCR4', 'IPCR7', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior', "Inventor-Country", "Applicant-Country"]



    for nb in tempoBrev:
        brev2 = tempoBrev[nb]
        tempo2 = dict() #the one for pitable
        for cle in clesRef2:
            if cle not in brev2.keys():
                print "is no goof"
            if brev2[cle] is not None and brev2[cle] != 'N/A' and brev2[cle] != 'UNKNOWN':
                if isinstance(brev2[cle], list):
                    tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev2[cle]]
                               
                elif cle=='date':
                    try:
                        tempo2['cle'] = brev2[cle].split('-')[0]
                    except:
                        pass #no date in data
                else:
                    temp = unicode(brev2[cle])
                    
                    #formate = EntitySubstitution()
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo2 [cle] = temp
                    
            else:
                tempo2[cle] = ''
        
        if tempo2 not in LstExp2:
            LstExp2.append(tempo2)
        
print len(LstExp2)
    
print len(LstExp)
Exclude = []

PipoTest2 = [k['label'] for k in LstExp2]
PipoTest = [k['label'] for k in LstExp]
print len(set(PipoTest2))
print len(set(PipoTest))

dicoRes = dict()
dicoRes['data'] = LstExp
contenu = json.dumps(dicoRes, ensure_ascii=True, indent = 3)
contenuPivotable = json.dumps(LstExp2,  indent = 3)
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
    for brev in LstExp:
        ligne = ''
        clesRef = brev.keys()
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
