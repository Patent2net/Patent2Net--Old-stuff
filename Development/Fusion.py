# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 07:50:48 2015

@author: dreymond
"""

import sys, os
import pickle

ndf1 = sys.argv[1]
ndf2 = sys.argv[2]

###tout est faux en changeant le modèle de stockage de fichiers
ListBiblioPath = ['..//DONNEES//'+ndf1+'//PatentBiblios', '..//DONNEES//'+ndf2+'//PatentBiblios']
ListPatentPath = ['..//DONNEES//'+ndf1+'//PatentLists', '..//DONNEES//'+ndf2+'//PatentLists']#List
ResultFolder = '..//DONNEES//Fusion'+ndf1.title()+ndf2.title()
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
        if "PatentList" not in rep1 or "PatentList" not in rep2 and nom != "Families": # no patentList for families
            with open(rep1+'//'+nom+ndf1) as fic1:
               Brevet1 = pickle.load(fic1)
               with open(rep2+'//'+nom+ndf2) as fic2:  
                   Brevet2 = pickle.load(fic2)
            data["Fusion"] = True
            if isinstance(Brevet1, dict) and isinstance(Brevet2, dict):
                requete = Brevet1["requete"] + ' UNION ' + Brevet2["requete"] 
                number = Brevet1["number"] + Brevet2["number"]
                data["brevets"] = BrevetFusion(Brevet1["brevets"], Brevet2["brevets"])
                data["requete"] = requete
                data["number"] = number
            else:
                data["brevets"] = BrevetFusion(Brevet1, Brevet2)
                
            if rep1.count('Biblio'):
                try:
                    os.mkdir(ResultFolder+'//PatentBiblios')
                except:
                    pass
                with open((ResultFolder+'//PatentBiblios//Fusion'+nom+ndf1.title()+ndf2.title()), "w") as ficRes:
                    pickle.dump(data, ficRes)
            else:
                try:
                    os.mkdir(ResultFolder+'//PatentLists')
                except:
                    pass
                with open((ResultFolder+'//PatentLists//Fusion'+nom+ndf1.title()+ndf2.title()), "w") as ficRes:
                    pickle.dump(data, ficRes)        
if Go:
    print "Collects " + ndf1 + " and " + ndf2 + " merged in file :" + 'Fusion'+ndf1.title()+ndf2.title() + '\n'
    print "in ", ResultFolder, " directory"
