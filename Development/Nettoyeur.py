# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 14:53:29 2014
Already included in last version of biblioGathering
@author: dreymond
"""


import pickle, sys
ResultPath = 'BiblioPatents'

def Clean(truc):
    if type(truc) == type(u''):
        temp = truc.replace(u'\x80', '')
        temp = temp.replace(u'\x82', '')
        temp = temp.replace(u'\u2002', '')
        temp = temp.replace(u"\xe2", "")
        return temp
    if type(truc) == type([]):
        return [Clean(u) for u in truc]
    else:
        return truc        

ndf = sys.argv[1]
fic = open(ResultPath+ '//' + ndf, 'rb')
print "loading data file ", ndf+' from ', ResultPath, " directory."

ListeBrevet = pickle.load(fic)


fic.close()
print len(ListeBrevet), " patents loaded from file."

listeRes = []
for Brev in ListeBrevet:
    BreTemp = dict()    
    for cle in Brev.keys():
        BreTemp[cle] = Clean(Brev[cle])
        
    listeRes.append(BreTemp)

fic = open(ResultPath+ '//Nettoye' + ndf, "w")
pickle.dump(listeRes, fic)
fic.close()
