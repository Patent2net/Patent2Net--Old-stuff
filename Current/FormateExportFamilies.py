# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json
import pickle
import bs4
#from bs4.dammit import EntitySubstitution
from OPS2NetUtils2 import ReturnBoolean, Decoupe, CleanPatent, CleanPatentOthers2, UnNest
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
        print "Found ", len(set([bre['label'] for bre in LstBrevet])), ' uniques labels'


#checking patent list if some patents are missing
with open(ListBiblioPath+'//'+ndf.replace('Families', ''), 'r') as data:
    LstBrevetComp = pickle.load(data)
    LabelsComp = [bre['label'] for bre in LstBrevetComp['brevets']]
print "checking consistency"
Labels = [bre['label'] for bre in LstBrevet]
comptBad = 0
for lab in LabelsComp:
    if lab not in Labels:
        print lab
        comptBad +=1
print comptBad, " identified problems."
if comptBad == 0:
    print "This is good!"

#we filter data for exporting most significant values
LstExp = [] 
LstExp2 = [] 
for brev in LstBrevet:
    if brev['label'] == 'WO2007000665':
        print
    #cleaningbre[c]
    for cle in brev.keys():
        brev[cle] = UnNest(brev[cle])

    brev= CleanPatent(brev)
    brev= CleanPatentOthers2(brev)
    
    ##
    
    tempo = brev # this one for DataTable
    tempo2 = dict() #the one for pitable
    PaysInv= [] #new field
    PaysApp = []
    #tempo = CleanPatent(tempo)
    tempo2 = copy.deepcopy(tempo) #ugly
    tempo3 = dict() #what the problem        
    LstExp.append(tempo)
    for ket in brev.keys():
        tempo3[ket] = tempo[ket]
        if isinstance(tempo2[ket], list):
            tempo2[ket] = UnNest(tempo2[ket])
        else:
            tempo2[ket] = tempo[ket]
        

    clesRef2 = ['label', 'date', 'citations','family lenght', 'priority-active-indicator', 'IPCR4', 'IPCR7', 'portee', 'applicant', 'pays', 'inventeur', 'representative', 'prior', "Inventor-Country", "Applicant-Country"]

    tempoBrev = Decoupe(tempo2)            
    for nb in tempoBrev:
        brev2 = tempoBrev[nb]
        brev2 = CleanPatent(brev2)
        
        
        tempo2 = dict() #the one for pitable
        for cle in clesRef2:
            if cle not in brev2.keys():
                print "is no good -->", cle
                brev2[cle] = 0
            if brev2[cle] is not None and brev2[cle] != 'N/A' and brev2[cle] != 'UNKNOWN':
                
                if isinstance(brev2[cle], list):
                    print "impossible ?"
                    tempo2[cle] = [bs4.BeautifulSoup(unit).text for unit in brev2[cle] if unit != 'N/A']
                               
                elif cle=='date' and brev2[cle] is not None:
                    try:
                        tempo2[cle] = brev2[cle].split('-')[0]
                    except:
                        tempo2[cle] = brev2[cle][0:4]
                         #no date in data
                else:
                    temp = unicode(brev2[cle])
                    
                    #formate = EntitySubstitution()
                    soup = bs4.BeautifulSoup(temp)
                    temp = soup.text
                    tempo2 [cle] = temp
                    
            else:
                tempo2[cle] = u''
        
        if tempo2 not in LstExp2:
            LstExp2.append(CleanPatent(tempo2))
        
print len(LstExp2), " lines (patent labels with unique biblio data for each key)"
    
print len(LstExp), " patents"
Exclude = []

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
