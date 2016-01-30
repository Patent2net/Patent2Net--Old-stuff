# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 07:50:48 2015

@author: dreymond
"""

import sys, os
import cPickle
from collections import OrderedDict as dict
import epo_ops


os.environ['REQUESTS_CA_BUNDLE'] = 'cacert.pem'
global key
global secret

fic = open('..//cles-epo.txt', 'r')
key, secret = fic.read().split(',')
fic.close()
registered_client = epo_ops.RegisteredClient(key, secret)
    #        data = registered_client.family('publication', , 'biblio')
registered_client.accept_type = 'application/json'

print "Usage: FusionPatList dir1 dir2 [...] dirN dirResult"

###tout est faux en changeant le modèle de stockage de fichiers
#ListBiblioPath = ['..//DONNEES//'+ndf1+'//PatentBiblios', '..//DONNEES//'+ndf2+'//PatentBiblios']
#ListPatentPath = ['..//DONNEES//'+ndf1+'//PatentLists', '..//DONNEES//'+ndf2+'//PatentLists']#List
#ListContentPath = ['..//DONNEES//'+ndf1+'//PatentContents', '..//DONNEES//'+ndf2+'//PatentContents']

data = dict()
import copy
def BrevetFusion(Brevet1, Brevet2):
    BrevetFusion = copy.copy(Brevet1)
    BrevetFusion.extend(Brevet2)
    return BrevetFusion
    
#lstReq = [subFolders for root, subFolders, files in os.walk('..//DONNEES//')]
if len(sys.argv)>3:
    lstReq = sys.argv[1:len(sys.argv)-1]
    res = sys.argv[len(sys.argv)-1]
        
else:
    lstReq = [subFolders for root, subFolders, files in os.walk('..//DONNEES//')]
    res = "Fusion"
ResultFolder = '..//DONNEES//'+res
ResultFolderWin = '..\\DONNEES\\'+res
try:
    os.makedirs(ResultFolder+'//PatentLists')
except:
    if res.title() in lstReq[0]:
        lstReq[0].remove(res.title())
    pass
lig= ""
BrevetRes = dict()
BrevetRes["brevets"] = []
BrevetRes["number"] =0
BrevetRes["requete"] = ''
with open(ResultFolder+'//PatentLists/'+res, 'w') as ficRes:
    for ndf in lstReq:
        lstBrevets2, nbTrouves = [], 0
        if ndf in os.listdir('..//DONNEES//') and ndf in os.listdir('..//DONNEES//'+ndf+'//PatentLists//'):
            with open('..//DONNEES//'+ndf+'//PatentLists//'+ndf) as fic:
                Brevet1 = cPickle.load(fic)
                print "Doing ", ndf, "Found ", len(Brevet1 ["brevets"]), "patents in list"
            
        BrevetRes["brevets"] = BrevetFusion(Brevet1["brevets"], BrevetRes["brevets"])
        BrevetRes["number"] = len(BrevetRes["brevets"])
        if len(BrevetRes["requete"])>0:
            BrevetRes["requete"] = Brevet1["requete"] + " UNION " + BrevetRes["requete"]
        else:
            BrevetRes["requete"] = Brevet1["requete"] 
            
    cPickle.dump(BrevetRes, ficRes)
                    
    print "Fusion done. Total in list: ", BrevetRes["number"]
with open('..//Fusion'+res +'.txt', 'w') as ficSav:
    ficSav.write(BrevetRes["requete"])
print "create requete.cql with ", res, " as dataDirectory and setting GatherPatent to False"
print "Use the following sentence as Request value (writen in Fusion'"+res+".txt file) \n"
print BrevetRes["requete"] 
    
            