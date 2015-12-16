# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 07:50:48 2015

@author: dreymond
"""

import sys, os
import cPickle as pickle
from collections import OrderedDict as dict
import collections
ndf1 = sys.argv[1]
ndf2 = sys.argv[2]
res = sys.argv[3]

###tout est faux en changeant le modèle de stockage de fichiers
ListBiblioPath = ['..//DONNEES//'+ndf1+'//PatentBiblios', '..//DONNEES//'+ndf2+'//PatentBiblios']
ListPatentPath = ['..//DONNEES//'+ndf1+'//PatentLists', '..//DONNEES//'+ndf2+'//PatentLists']#List
ListContentPath = ['..//DONNEES//'+ndf1+'//PatentContents', '..//DONNEES//'+ndf2+'//PatentContents']
ResultFolder = '..//DONNEES//'+res.title()
ResultFolderWin = '..\\DONNEES\\'+res.title()
data = dict()

def BrevetFusion(Brevet1, Brevet2):
    BrevetFusion = []
    for brev in Brevet2:
        if brev not in Brevet1:
            BrevetFusion.append(brev)
    for brev in Brevet1:
        if brev not in BrevetFusion:
            BrevetFusion.append(brev)
    return BrevetFusion

Go  = True

try:
    os.mkdir(ResultFolder)
except:
    pass
for rep1, rep2 in [ListPatentPath, ListBiblioPath]:
    
    if ndf1.count('Families') >0 or ndf2.count('Families') > 0:
        if rep1 not in ListBiblioPath:
            Go = False
            # families patent are not gathered form request
            # but from  Patent List
            # so no file in PatentList Diractory
    for nom in ["", "Families"]:
        if "PatentList" in rep1 or "PatentList" in rep2: 
            if nom != "Families": # no patentList for families
                with open(rep1+'//'+nom+ndf1) as fic1:
                   Brevet1 = pickle.load(fic1)
                   with open(rep2+'//'+nom+ndf2) as fic2:  
                       Brevet2 = pickle.load(fic2)
                data["Fusion"] = True
#                if isinstance(Brevet1, dict) and isinstance(Brevet2, dict):
                requete = Brevet1["requete"] + ' UNION ' + Brevet2["requete"] 
                number = Brevet1["number"] + Brevet2["number"]
                data["brevets"] = BrevetFusion(Brevet1["brevets"], Brevet2["brevets"])
                data["requete"] = requete
                data["number"] = number
#                else:
#                    data["brevets"] = BrevetFusion(Brevet1, Brevet2)
                    
                if rep1.count('Biblio'):
                    try:
                        os.mkdir(ResultFolder+'//PatentBiblios')
                    except:
                        pass
                    with open((ResultFolder+'//PatentBiblios//Fusion'+nom + res.title()), "w") as ficRes:
                        pickle.dump(data, ficRes)
                else:
                    try:
                        os.mkdir(ResultFolder+'//PatentLists')
                    except:
                        pass
                    with open((ResultFolder+'//PatentLists//'+nom + res.title()), "w") as ficRes:
                        pickle.dump(data, ficRes)        
        else:
            with open(rep1+'//'+nom+ndf1) as fic1:
               Brevet1 = pickle.load(fic1)
               with open(rep2+'//'+nom+ndf2) as fic2:  
                   Brevet2 = pickle.load(fic2)
            data["Fusion"] = True
            if isinstance(Brevet1, dict) or isinstance(Brevet1, collections.Mapping):
                requete1 = Brevet1["requete"] 
                number1 = Brevet1["number"] 
                data1 = Brevet1["brevets"]
            else:
                requete1 = 'unkonwn'
                number1 = 0
                data1 = Brevet1
            if isinstance(Brevet2, dict) or isinstance(Brevet2, collections.Mapping):
                requete2 = Brevet2["requete"] 
                number2 = Brevet2["number"]
                data2 = Brevet2["brevets"]
                
            else:#we should not get ther since new version (may 2015)
                requete2 = 'unkonwn'
                number2 = 0
                data2 = Brevet2
            data["requete"] = requete1 + ' UNION ' + requete2
            data["number"] = number1 +number2
            data["brevets"] = BrevetFusion(data1, data2)
            
            if rep1.count('Biblio'):
                try:
                    os.mkdir(ResultFolder+'//PatentBiblios')
                except:
                    pass
                with open((ResultFolder+'//PatentBiblios//'+nom+ res.title()), "w") as ficRes:
                    pickle.dump(data, ficRes)
            else:
                try:
                    os.mkdir(ResultFolder+'//PatentLists')
                except:
                    pass
                with open((ResultFolder+'//PatentLists//Fusion'+ nom + res.title()), "w") as ficRes:
                    pickle.dump(data, ficRes)        
if Go:
    for source in ListContentPath:
        commande = 'xcopy /Y /S '+source.replace('//', '\\') +'\\*.* ' + ResultFolderWin + '\\PatentContents\\'
        os.system(commande)
    print "Collects " + ndf1 + " and " + ndf2 + " merged in file :" + res.title() + '\n'
    print "in ", ResultFolder, " directory"
#    print "would you like me to generate networks and threatment ?"
#    print "Ensure requete.cql parameters you wish to launch are set to True\n"
#    print "I will modify datadirectory for you."
#    print 'Y / N'

#    resp = raw_input()
#    
#    if resp =='Y' or resp =='O':
#        result = """"""    
#        with open('..//requete.cql') as fic:
#            contenu = fic.readlines()
#            for lig in contenu:
#        #if not lig.startswith('#'):
#                if lig.count('request:')>0:
#                    lig  = "request: " + data['requete'] + '\n'
#                if lig.count('DataDirectory:')>0:
#                    lig = "DataDirectory: " + res + '\n'
##                for param in ["GatherPatent","GatherBiblio", "GatherContent", "GatherFamilly"]:
##                    if lig.count(param)>0:
##                        lig = param+": False\n"
##                
#                    
#                result += lig
#        with open('..//requete.cql', 'w') as ficRes:
#            ficRes.write(result)
#        lstPrg = ["FormateExportAttractivityCartography.exe", "FormateExportCountryCartography.exe", "FormateExportBiblio.exe", "FormateExportDataTable.exe",
#                  "FormateExportDataTableFamilies.exe", "FormateExportPivotTable.exe", "FusionCarrot2.exe", "FusionIramuteq2.exe",
#                  "P2N-networksCit.exe", "P2N-FreePlane.exe", "P2N-networksMix.exe", "Interface2.exe"]
#        for cmd in lstPrg:
#            print "Launching " + cmd
#            os.system('.\\' + cmd)
#            print "Done " + cmd
#            
        