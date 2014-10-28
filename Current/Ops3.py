# -*- coding: utf-8 -*-
"""
Created on Sun Jul 07 16:17:01 2013

Indeed, this is not the best way for doing a simplified interface to OPS (http://ops.epo.org) 
REST services as they are described in wadl format. 
Best programmer could perform the web service inquiries to fully construct the interfaces
using the semantics of web services (instead of re-constructing it as I could do...)

version 0.5
@author: dreymond
"""


import requests
import time
try: import simplejson as json
except ImportError: import json
#import date
#low level functions

# hight level functions
        
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
        

def ExtractionDate (Brev):
    if u'bibliographic-data' in Brev.keys():
        if u'publication-reference' in Brev[u'bibliographic-data'].keys():
            if u'document-id' in Brev[u'bibliographic-data'][u'publication-reference'].keys():
                tempo = Brev[u'bibliographic-data'][u'publication-reference'][u'document-id']
                if isinstance(tempo, dict):
                    if u'date' in tempo.keys():
                        return tempo[u'date']['$']
                    else:
                        print "bad date", tempo
                        return ""
                else:
                    if u'date' in tempo[0].keys():
                        return tempo[0][u'date']['$'] #first on should be good
                    else:
                        print "bad date", tempo
                        return ""
                
                #again retrocompatibility
    try:
        return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['priority-claims'][u'priority-claim']['document-id'][0]['date']['$']
    except:
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['priority-claims'][u'priority-claim'][0]['document-id'][0]['date']['$']
        except:
            try:
                return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['priority-claims'][u'priority-claim']['document-id']['date']['$']
            except:
                print 'something bad, Date'
                return None
    
def ExtraitKind(Brev):
     if u'@kind' in Brev.keys():
        return Brev[u'@kind']
     else:#retro ompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@kind']
        except:
            print 'something bad, Kind'
            return None

def ExtraitTitleEn(Brev):
    if u'bibliographic-data' in Brev.keys():
        if isinstance(Brev[u'bibliographic-data']['invention-title'], dict):
            return Brev[u'bibliographic-data']['invention-title']['$']
        else: #list are use for multilanguage title support
            #just taking the first one
            return Brev[u'bibliographic-data']['invention-title'][0]['$']
    else: #retro ompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['invention-title'][0]['$']
        except:
            try:
                return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['invention-title']['$']
            except:
                print 'something bad, title'
                return None

def ExtraitCountry(Brev):
    if u'@country' in Brev.keys():
        return Brev[u'@country']
    else: #again retrocompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@country']
        except:
            print 'something bad, country'
            return None

def AlphaTest(chain):
    for let in chain:
        if let.isdigit():
            return False
    return True
    
def UnNest2List(thing):
    CoolType = [str, unicode, int, float]
    if type(thing) in CoolType:
        return thing
    else:
        res = []
        for tt in thing:
            if type(tt) in CoolType:
                res.append(tt)
            else:
                for k in tt:
                    tempo = UnNest2List(k)
                    if type(tempo) in CoolType:
                        if tempo not in res:
                            res.append(tempo)
                    else:
                        for ttt in tempo:
                            res.append(UnNest2List(ttt))
        return res
        
def ExtraitIPCR2(Brevet):
    res = []
    if u'bibliographic-data' in Brevet.keys():
        if u'classifications-ipcr' in Brevet[u'bibliographic-data'].keys():
            if u'classification-ipcr' in Brevet[u'bibliographic-data'][u'classifications-ipcr'].keys():
                tempo = Brevet[u'bibliographic-data'][u'classifications-ipcr'][u'classification-ipcr']
                for classif in tempo:
                    if isinstance(classif, dict):
                        if u"text" in classif.keys():
                            classTemp = classif['text']['$'].replace(' ','')
                            if AlphaTest(classTemp[len(classTemp)-2:len(classTemp)]):
                                res.append(classTemp[:len(classTemp)-2])
                            else:
                                res.append(classTemp)
                            
                return res
        elif u'classification-ipc' in Brevet[u'bibliographic-data'].keys():
            if u'text' in Brevet[u'bibliographic-data'][u'classification-ipc'].keys():
                res.append(Brevet[u'bibliographic-data'][u'classification-ipc']['text']['$'])
                return res
        else:
            return None
        
    else: #retrocomp
        try:
            Brev = Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['classifications-ipcr']['classification-ipcr']
        except:
            print 'something bad, IPCR'
            try:        
                return ExtraitClassification(Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['patent-classifications']['patent-classification'])
            except:
                return None
        if type(Brev) == type(list()):
            for clas in Brev:
                res.append(clas['text']['$'])
            return res
        else:
            return Brev['text']['$']
    
    
def ExtraitParties(Brev, content, Format):
    res = []
    if u'bibliographic-data' in Brev.keys():
        Brev = Brev[u'bibliographic-data'][u'parties']
    else: #for retrocompatibility, should be cleaned   
        try:
            Brev = Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data'][u'parties']
        except:
            return None
    if Brev.has_key(content+'s'):
        for truc in Brev[content+'s'][content]:
            if truc[u'@data-format'] == Format:
                res.append(truc[content+u'-name'][u'name'][u'$'].replace('\u2002', ' '))
    else:
        return None
    return res
  


def NomBrevet(Brev):
    """extracts the invention title of a patent bibliographic data"""
    try:
        if Brev.has_key(u'ops:world-patent-data'):
            Brev = Brev[u'ops:world-patent-data']
            if Brev.has_key(u'exchange-documents'):
                Brev = Brev[u'exchange-documents']
                if Brev.has_key(u'exchange-document'):
                    Brev = Brev[u'exchange-document'] 
                    if Brev.has_key(u'bibliographic-data'):
                        Brev = Brev[u'bibliographic-data']
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None
        if Brev.has_key(u'invention-title'):
            if type(Brev[u'invention-title']) == type(''):
                return Brev[u'invention-title']
            elif type(Brev[u'invention-title']) == type(dict()):
                if Brev[u'invention-title'].has_key('$'):
                    return Brev[u'invention-title']['$']
            else:
                titre = []
                for tit in Brev[u'invention-title']:
                    if tit.has_key('$'):
                        titre.append(tit['$'])
                return titre
        else:
            return None
    except:
        return None
