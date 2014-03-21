# -*- coding: utf-8 -*-
"""
Created on Mon Jul 08 16:52:35 2013
version 0.9
@author: dreymond
**"""

from Ops2 import *
import os
import sys
import urllib
# construction de la liste de Brevets associés à des mots clés, argument
# du script
# sauvegarde dans un fichier
# gestion de la récupération d'incident
nb = len(sys.argv)
Termine = False
def quote(string):
    return urllib.quote(string, safe='/\\())')
    
request = ""
cpt = 0
for u in sys.argv[2:nb]:
    if cpt == 0:
        request += u.strip()#.strip("\'\"")
    else:
        request += ' '+u.strip()
    cpt +=1

request = request.replace('\\', '')
ndf = sys.argv[1]
if not ndf.endswith(".dump"):
    print "Incorrect file."
    print "GatherOPS nom_de_fichier.dump keyword OPERATOR keyword..."
#request = request.replace('"','', request.count('"'))
#request = request.replace("'",'', request.count("'"))#'"3D printer"' #
print 'Building list of patent for request: ', request
#print "13", request.count('"')
#print request.count("'")

tempoPath = 'PatentLists'
ResultPath = 'BiblioPatents'

if os.listdir('.').count(tempoPath) ==0:
    os.mkdir(tempoPath)
    

if os.listdir('.').count(ResultPath) ==0:
    os.mkdir(ResultPath)

ListeBrevet = list() # results
import pickle

    
Brevets = []

#request = quote(request.strip())

try:    
    ndfLstBrev = open(tempoPath+'//'+ndf, 'r')
    Brevets = pickle.load(ndfLstBrev)
    Termine = pickle.load(ndfLstBrev)
    if Termine == None:
        Termine = False
    ndfLstBrev.close()
    print "List loaded from file: '"+ndf+"'"
    print "Checking for missing patents"
    if not Termine or len(Brevets) ==0:
        raise "arg"
    parametres = construit_params('published-data', 'search', 'full-cycle', '', '') 
    url = ops_request_construct( parametres )
    url ='http://ops.epo.org/3.1/rest-services/published-data/search'
    url = url + '?q=' + quote(request.replace("",""))
    headers = {'Accept': 'application/json',}
    data = requests.get(url, headers = headers)
    data = data.json()
    premReq =True
    if type(data) == type(dict()):
        nbTrouv = int(data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
    if nbTrouv > len(Brevets):
        
        print "completing patent list, seeking for ", nbTrouv - len(Brevets), ' patents'
        raise 
        
    

except:
    if not premReq or not Termine:
        parametres = construit_params('published-data', 'search', 'full-cycle', '', '') 
        #url = ops_request_construct( parametres )
        url ='http://ops.epo.org/3.1/rest-services/published-data/search'
        url = url + '?q=' + quote(request.replace("",""))
        headers = {'Accept': 'application/json',}
        data = requests.get(url, headers = headers)
        data = data.json()
    
        if type(data) == type(dict()):
            nbTrouv = int(data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
        
    if nbTrouv > len(Brevets):
        premReq = False
        print "completing patent list, seeking for ", nbTrouv - len(Brevets), ' patents'
    
        deb = len(Brevets) 
        end = 1
        Res = Brevets # la liste des résultats
        cpt = 0
        cpt2 = 0
        while end <= nbTrouv and not Termine: 
            end = deb + 24  # epo ne renvoi que 25 résultat
            plage = str(deb) + '-' + str(end)
            
            
            if deb == 0:
                req = data
            else:
                time.sleep(6)
                url ='http://ops.epo.org/3.1/rest-services/published-data/search'
                url = url + '?q=' + quote(request.replace("","")) + '&range='+str(deb)+'-' + str(end)
                req = requests.get(url, headers = headers)
             #10 recherches par minute MaX : http://www.epo.org/searching/free/fair-use.html
                req = req.json()
            if type(req) == type(dict()):
                totalRes = int(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
                if totalRes >0:
                    uu = req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'ops:publication-reference']
                    if len(uu)>1:
                        for k in uu:
                            if k not in Brevets:
                                Brevets.append(k)
                                cpt2 += 1
                    else:
                        if uu not in Brevets:
                            Brevets.append(uu)
                            cpt2 += 1
                    deb = int(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:range'][u'@end']) + 1
                    print cpt2, " patents added"
                else:
                    print "No results", totalRes    
            if len(Brevets) == nbTrouv:
                Termine = True
            else:
                Termine = False
            ndfLstBrev = open(tempoPath+'//'+ndf, 'w')
            
            pickle.dump(Brevets, ndfLstBrev)
            pickle.dump(Termine, ndfLstBrev)
            pickle.dump(request, ndfLstBrev)
            ndfLstBrev.close()
    else:
        print 'No missing patents. ',

ndfLstBrev = open(tempoPath+'//'+ndf, 'w')

pickle.dump(Brevets, ndfLstBrev)

print len(Brevets), ' patents found and saved in file: '+ndf

if not nbTrouv or len(Brevets) == nbTrouv:
    Termine = True
    if len(Brevets) == 0:
        Termine == False
    pickle.dump(Termine, ndfLstBrev)
    pickle.dump(request, ndfLstBrev)
ndfLstBrev.close()

