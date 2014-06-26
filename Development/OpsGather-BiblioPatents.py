# -*- coding: utf-8 -*-
"""
Created on Sun Feb 09 15:54:10 2014

@author: dreymond
"""
import sys

from Ops2 import *
import os
import datetime


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
if not ndf.endswith(".dump"):
    print "Incorrect file. Usage:"
    print "GatherOPS FileName.dump keyword OPERATOR keyword..."
#request = request.replace('"','', request.count('"'))
#request = request.replace("'",'', request.count("'"))#'"3D printer"' #
#print 'building list of patent for request: '
#print "13", request.count('"')
#print request.count("'")
import urllib
tempoPath = 'PatentLists'
ResultPath = 'BiblioPatents'

if os.listdir('.').count(tempoPath) ==0:
    os.mkdir(tempoPath)
    

if os.listdir('.').count(ResultPath) ==0:
    os.mkdir(ResultPath)

ListeBrevet = list() # results
import pickle
def quote(string):
    return urllib.quote(string, safe='/\\())')
    
Brevets = []

#request = quote(request.strip())

try:
    ndfLstBrev = open(tempoPath+'//'+ndf, 'r')
    ListeBrevets = pickle.load(ndfLstBrev)
    
    try:
        print "Loading patent list from file: '"+ ndf+"'"
        Termine = pickle.load(ndfLstBrev)
    except:
        Termine = False
        print 'pas de terminé'
    try:
        requete = pickle.load(ndfLstBrev)
        print "Patent list from request: ", requete, " loaded."
    except:
        print 'pas de requête'
    
    ndfLstBrev.close()
    ListeOk = True
    
    print len(ListeBrevets), " patents in list."
    if len(ListeBrevets) == 0:
            raise "arg"
    

except:
    print "use the correct file name or GatherOpenPatentList to make it before"
    requete = ''
    Termine = False
    ListeBrevets = []
    ListeOk = False

if ListeOk:
    try:
        fic = open(ResultPath+'//'+ndf, 'r') 
        Brevets = pickle.load(fic)
        NumBrevetsCollectes = [u['label'] for u in Brevets]
        print len(Brevets), " biblio content yet gathered from OPS.", 
        if len(ListeBrevets)-len(Brevets) != 0:
            print str(len(ListeBrevets)-len(Brevets)), " patents are missing. I continue gathering." 
            
            Collecte = True
        else:
            print "No missing patents.\n The file ", ResultPath+'/'+ndf, ' is up to date.'
            Collecte = False
        
    except:
        print "Gathering biblio contents... wait at least ", str(6*(len(ListeBrevets) - len(Brevets))), ' seconds.'
        NumBrevetsCollectes = []
        Collecte = True
        
    LstPresente =  []  
    for Brevet in ListeBrevets:
        try:
            LstPresente.append(Brevet['document-id']["country"]['$']+Brevet['document-id'][u'doc-number']['$'])
        except:
            LstPresente.append(Brevet[u'exchange-document']['@country']+Brevet[u'exchange-document']['@doc-number'])
    ListeACollecter = [k for k in LstPresente if k not in NumBrevetsCollectes]
    print "Gathering ", len(ListeACollecter), " patents."
    for bre in Brevets:
        ListeBrevets.append(bre)
    for NumBrevet in ListeACollecter:
       try:
            Collecte = True
            PatentData = dict() #the dictionnary will content the list of patent data extrated 
            PatentData['label'] =  NumBrevet
            
            #building the url request to retreive patent bibliography
            print "Patent number:", NumBrevet        
            params = construit_params(srv='published-data', ref='search', in_type='biblio', entree = '', output='')
            
            url = ops_request_construct(params)
            time.sleep(6)
            # data gathering
            req = ops_request_data2( url, param= {'q': NumBrevet})
            # in some cases OPS return more than one document...
            # we copy the structure so as they come as they where from separates requests
            cpt = 0
           
            if int(req[u'ops:world-patent-data']['ops:biblio-search'][u'@total-result-count']) > 1:
                Reqs = []
                
                for t in range (len(req[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'])):
                    cpt += 1
                    dico = dict()
                    dico[u'ops:world-patent-data'] = dict()
                    dico [u'ops:world-patent-data']['ops:biblio-search'] = dict()
                    dico [u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'] = dict()
                    dico [u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'] = req[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][t] 
                    Reqs.append(dico)
                    print cpt
            else:
                Reqs = []
                Reqs.append(req)
            # printing to reassure the user  
            for Req in Reqs:
                PatentData['titre'] = Clean(ExtraitTitleEn(Req))                  
                print "Patent title(s)", PatentData['titre']
              
                PatentData['inventeur'] = Clean(ExtraitParties(Req, 'inventor', 'epodoc'))
                print "Inventors : ",  PatentData['inventeur']
                PatentData['applicant'] = Clean(ExtraitParties(Req, 'applicant','epodoc'))
                print "Applicants : ", PatentData['applicant']
                PatentData['pays'] = ExtraitCountry(Req)
                print "Country:", PatentData['pays'] 
                PatentData['portee'] = ExtraitKind(Req)
                print "Level :", PatentData['portee']
                PatentData['classification'] = ExtraitIPCR2(Req)
                    
                if PatentData["classification"] is not None:
                    if type(PatentData['classification']) == type ([]):
                        temp = []
                        for classif in PatentData['classification']:
                            temp.append(classif.replace(' ', '', classif.count(' ')))
                        PatentData['classification'] = []
                        for ipc in temp:
                            PatentData['classification'].append(ipc)
                        temp = []                
                        for ipcr in PatentData['classification']:
                            temp.append(ipcr[0:4])
                        PatentData["ClassifReduite"] = list(set(temp))
                    else:
                        PatentData['classification'] = PatentData['classification'].replace(' ', '', PatentData['classification'].count(' '))
                        PatentData["ClassifReduite"] = PatentData['classification'][0:4]
                    
                else:
                    PatentData["ClassifReduite"] = None
                print "Classification (not always) IPCR : ", PatentData['classification']
                print "Classification Reduced: ", PatentData['ClassifReduite']
                date = ExtractionDate(Req) #priority claim first date time
                if date is not None:
                    
                    PatentData['date'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
                    print "patent date", PatentData['date']
                else:
                    PatentData['date'] = datetime.date(datetime.date.today().year+2, 1, 1)
                print " *********************************   "
                if None not in PatentData.values():
                    ListeBrevet.append(PatentData)
                 #dans ce cas on aura au moins les précédents sauvegardés
                fic = open(ResultPath+'//'+ndf, 'w') 
                pickle.dump(ListeBrevet, fic)
       except:
            print "encoding error ?"
            next
    if Collecte:
        #print "Saving Data. "
        #saving data gathered in a file   
        #print 'Patent list for request: ', requete, " saved in file ",  ndf + ' into ', tempoPath, " directory"
        print "Saving patents data in file", ndf + " into ", ResultPath, "  directory"
        print "This last file will be used to produce network"
        try:
            fic.close()
        except:
            print "no results gathered, network problem ?"
