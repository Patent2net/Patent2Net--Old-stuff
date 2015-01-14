# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 07:50:48 2015

@author: dreymond
"""

import sys
import pickle

ndf1 = sys.argv[1]
ndf2 = sys.argv[2]

ListBiblioPath = '..//DONNEES//PatentBiblios'

BrevetFusion = []
with open(ListBiblioPath+'//'+ndf1) as fic1:
   Brevet1 = pickle.load(fic1)
   with open(ListBiblioPath+'//'+ndf2) as fic2:  
       Brevet2 = pickle.load(fic2)
       
for brev in Brevet2:
    if brev not in Brevet1:
        BrevetFusion.append(brev)
for brev in Brevet1:
    if brev not in BrevetFusion:
        BrevetFusion.append(brev)

      
with open((ListBiblioPath+'//Fusion'+ndf1.title()+ndf2.title()), "w") as ficRes:
    pickle.dump(BrevetFusion, ficRes)
    