# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 09:12:25 2015

@author: dreymond
"""

from OPS2NetUtils2 import ReturnBoolean



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

GlobalPath ='..//DONNEES//'
ResultPath = GlobalPath+ndf+'//PatentBiblios'
ResultPathGephi = GlobalPath+ndf+'//GephiFiles'
ResultPathContent = GlobalPath+ndf

#formating html
try: 
    with open('..//index.html', 'r') as ficRes:
        data = ficRes.read()
        contenuExist = data[data.index('<body ')+len('<body onload="DetectBrowser()">'):data.index('/body>')-1]
    ficRes = open('..//index.html', 'w')
except:
    with open('ModeleIndex.html', 'r') as fic:
        html = fic.read()
        html = html[:html.index('/body>')]
    contenuExist = ''
    ficRes = open('..//index.html', 'w')
    
with open('ModeleContenuIndex.html', 'r') as fic:
    NouveauContenu = fic.read()

contenuCleaned = []
if len(contenuExist)>1:
    if ndf in contenuExist and requete in contenuExist:
        
        for content in contenuExist.split('<ul>'):
            if ndf in content or requete in content:
                pass
            else:
                contenuCleaned.append('<ul>'+content)
        with open('ModeleIndex.html', 'r') as fic:
            html = fic.read()
            html = html[:html.index('</body>')]
        

NouveauContenu  = NouveauContenu .replace("***CollectName***", ndf)
NouveauContenu  = NouveauContenu .replace("***Request***", requete)
import datetime
today = datetime.datetime.today()
date= today.strftime('%d, %b %Y')
NouveauContenu  = NouveauContenu .replace("***Date***", date)
if len(contenuCleaned)>0:
    for element in contenuCleaned:
        html += '<ul>' + element
html += NouveauContenu + """
  </body>
</html>
"""
ficRes.write(html)
ficRes.close()
import os
os.system('start firefox -url ..\\index.html' )


