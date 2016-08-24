# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 09:12:25 2015

@author: dreymond
"""

from P2N_Lib import ReturnBoolean, LoadBiblioFile
import codecs
import os
import cPickle
nbFam = 0
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

GlobalPath ='..//DONNEES'
ResultPath = GlobalPath+'//'+ndf+'//PatentBiblios'
ResultPatentPath = GlobalPath+'//'+ndf+'//PatentLists'

ResultPathGephi = GlobalPath+'//'+ndf+'//GephiFiles'
ResultPathContent = GlobalPath+'//'+ndf

# take request from BiblioPatent file


if 'Description'+ndf in os.listdir(ResultPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
    data = LoadBiblioFile(ResultPath, ndf)

else: #Retrocompatibility
    print "please use Comptatibilizer"
    #if 'Fusion' in data.keys()
requete = data['requete']
    
if GatherFamilly:#pdate needed for families
    if 'DescriptionFamilies'+ndf in os.listdir(ResultPath): # NEW 12/12/15 new gatherer append data to pickle file in order to consume less memory
        data2 = LoadBiblioFile(ResultPath, 'Families' + ndf)
        nbFam = len(data2['brevets'])
    else: #Retrocompatibility
        print "please use Comptatibilizer"
    #if 'Fusion' in data.keys()with open( ResultPath+'//Families'+ndf, 'r') as ficBib:
 #        data2 = cPickle.load(ficBib)
        
else:
    nbFam=0

#if 'Description'+ndf in os.listdir(ListBiblioPath):
#    with open(ListBiblioPath+'//'+ndf, 'r') as data:
#        dico = LoadBiblioFile(ListBiblioPath, ndf)
#else: #Retrocompatibility
#    print "please use Comptatibilizer"    
#    sys.exit()
#LstBrevet = dico['brevets']    
#if dico.has_key('requete'): 
#    requete = dico["requete"]
#    print "Using ", ndf," file. Found ", len(dico["brevets"]), " patents! Formating to HMTL tables"
#
#
#    
#formating html
#try: 
#    with open(GlobalPath+'//index.html', 'r') as ficRes:
#        data = ficRes.read()
#        contenuExist = data[data.index('<body ')+len('<body onload="DetectBrowser()">'):data.index('/body>')-1]
#    ficRes = open('..//index.html', 'w')
#except:

ficRes = codecs.open(GlobalPath+'//'+ndf+'.html', 'w', 'utf8')
    
with codecs.open('ModeleContenuIndex.html', 'r', 'utf8') as fic:
    NouveauContenu = fic.read()


with open('ModeleIndexRequete.html', 'r') as fic:
    html = fic.read()
    html = html[:html.index('</body>')]
        
html  = html .replace("***Request***", requete)

NouveauContenu  = NouveauContenu .replace("***CollectName***", ndf)
NouveauContenu  = NouveauContenu .replace("***Request***", requete)
if data.has_key("brevets"): #compatibility, this may be useless
    if nbFam ==0:
        NouveauContenu  = NouveauContenu.replace("***NombreRes***", str(len(data["brevets"])))
    else:
        NouveauContenu  = NouveauContenu.replace("***NombreRes***", str(len(data["brevets"])) + " <br> <li> Family lenght:" + str(nbFam) +"</li>")
else:
    NouveauContenu  = NouveauContenu.replace("***NombreRes***", "see datatable :-)")
    

import datetime
today = datetime.datetime.today()
date= today.strftime('%d, %b %Y')


if Gather:
    
    FileComps = ""
    nbFic = dict()
    for content in [u'Abstract', u'Claims', u'Description', u'FamiliesAbstract', u'FamiliesClaims', u'FamiliesDescription' ]:
        nbFic[content] = dict()
        try:
            lstfic = os.listdir(ResultPathContent+'//PatentContents//' + content)
            Langues = set()
            for fi in lstfic:
                Langues.add(str(fi[0:2]))
        except:
            lstfic = []
            Langues =set()
        if len(Langues)>0:            
            for ling in Langues:
                nbFic[content][ling] = len([fi for fi in lstfic if fi.startswith(ling)])
        else:
            pass
    for content in [u'Abstract', u'Claims', u'Description', u'FamiliesAbstract', u'FamiliesClaims', u'FamiliesDescription' ]:
        if len(Langues)>0:
            FileComps  += u"<li>"+content+": " +  " &nbsp; ".join([str(nbFic[content][ling]) +u" ("+ling.upper() +")" for ling in nbFic[content].keys()]) +u"</li>\n"
        else:
            FileComps  += u"<li>"+content+": 0 </li>\n"             
        FileComps = FileComps .replace('[', '')   
        FileComps = FileComps .replace(']', '')
        FileComps = str(FileComps .replace("'", ''))  

        NouveauContenu  = unicode(NouveauContenu) 
        NouveauContenu  = NouveauContenu .replace(u"***Date***", date + FileComps )
else:
    NouveauContenu  = NouveauContenu .replace(u"***Date***", unicode(date))

    
html += NouveauContenu + """
  </body>
</html>
"""
ficRes.write(html)
ficRes.close()

# updating index.js for server side and local menu
inFile =[] # memorize content
with open('../dex.js') as FicRes:
    data = FicRes.readlines()
    for lig in data[2:]:
        if '</ul>' not in lig and "');" not in lig:
            inFile.append(lig)
        
with open('../index.js', 'w') as ficRes:
    ficRes.write("document.write('\ ".strip())
    ficRes.write("\n") 
    ficRes.write(" <ul>\ ".strip()) 
    ficRes.write("\n") 

     # write last analyse
    ficRes.write("""<li><a href="DONNEES/***request***.html" target="_blank">***request***</a></li>\ """.replace('***request***', ndf).strip())
    ficRes.write("\n")     
    for exist in inFile:
        if ndf not in exist:
            ficRes.write(exist.strip().replace('</ul>\ ', ''))
            ficRes.write("\n") 
            
    ficRes.write(" </ul>\ ".strip())
    ficRes.write("\n") 
    ficRes.write("');")
    