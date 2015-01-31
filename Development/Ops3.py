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


#import requests
#import time
import datetime
try: import simplejson as json
except ImportError: import json
#import date
#low level functions

# hight level functions

#TAL Tools
import re
#import string
def coupeEnMots(texte):
    "returns a list of words cleaned from punctuation, digits and other signs"
    texte= texte.lower()
    res = re.sub('["\'<>]', ' ', texte) # on vire une partie de la ponctuation
    res = re.sub('\d', ' ', res) # extraction des chiffres
    res = re.findall('\w+', res, re.UNICODE) # extraction des lettres seulement
    return res


def decoupParagraphEnPhrases(paragraph):
    """returns the paragraph splited in phrases ignoring specifics titles. To be completed"""
    import re
    finsDePhrase = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
          (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  M\.   )    # Don't end sentence on "M."
        (?<!  Mme\.   )    # Don't end sentence on "Mme."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        \s+               # Split on whitespace between sentences.
        """, 
        re.IGNORECASE | re.VERBOSE)
    listeDePhrases  = finsDePhrase.split(paragraph)
    return [ph for ph in listeDePhrases if ph] #non vides


def RecupAbstract(dico):
    res = dict()
    if u'@lang' in dico.keys():
        if dico[u'@lang'].count(u'fr')>0:
            res[u'resume'] = dico[u'p']
        else:
            res[u'abstract'] = dico[u'p']
        return res    
    else:
        res['abs'] = dico[u'p']
        return res
    #elif u'abstract' in str(dico):
     #   print "where is the key? \n", dico

def EcritContenu(contenu, fic):
    with open(fic, 'w') as ficW:
        ficW.write(contenu.encode('utf8'))
        return 'OK'
        
def MakeText(Thing):
    res = u''
    if isinstance(Thing, list):
        for thing in Thing:
            res += MakeText(thing)
    elif isinstance(Thing, dict):
        if '$' in Thing.keys():
            if isinstance(Thing['$'], str) or isinstance(Thing['$'], unicode):
                return Thing['$'] +'\n'
            elif isinstance(Thing['$'], list):
                for thing in Thing['$']:
                    res += MakeText(thing) +'\n'
            else:
                print "I don't know what to do"
                    
        if 'p' in Thing.keys():
            if isinstance(Thing['p'], str) or isinstance(Thing['p'], unicode):
                return Thing['p']
            elif isinstance(Thing['p'], list):
                for thing in Thing['p']:
                    res += MakeText(thing)
            else:
                print "I don't know what to do"
                    
        elif 'claims' in str(thing):
            try:
                res = MakeText(Thing[u'claims']['claim'][u'claim-text'])
            except:
                print Thing.keys()
        else:
            print "what else ?"
    else:
        print "I don't know what to do"
    return res
        #not fun

def PatentSearch(client, requete, deb = 1, fin = 1):
    requete = requete.replace('/', '\\')
    data = client.published_data_search(requete, deb, fin)
    Brevets = []
    if data.ok:
        data = data.json()
        nbTrouv = int(data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
        patents = data[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'ops:publication-reference']
        if isinstance(patents, list):
            for k in patents:
                if k not in Brevets:
                    Brevets.append(k)

        else: #sometimes its a sole patent
            if patents not in Brevets:
                Brevets.append(patents)
    else:
        print "request not correct, cql language only"
        return None
    return Brevets, nbTrouv
  
def ProcessBiblio(pat):
    PatentData = dict()
    if "country" in pat.keys():
        PatentData['label'] = pat["country"]['$']+pat[u'doc-number']['$']
    else:
        PatentData['label'] = pat['@country']+pat['@doc-number']
    try:
        PatentData['inventeur'] = Clean(ExtraitParties(pat, 'inventor', 'epodoc'))
    except:
        PatentData['inventeur'] = 'UNKNOWN'
    try:
        PatentData['applicant'] = Clean(ExtraitParties(pat, 'applicant','epodoc'))
    except:
        PatentData['applicant'] = 'UNKNOWN'
    try:
        PatentData['titre'] = Clean(ExtraitTitleEn(pat))
    except:
        PatentData['titre'] = 'UNKNOWN'
    try:
        PatentData['pays'] = ExtraitCountry(pat)
    except:
        PatentData['pays']  = 'UNKNOWN'
    try:    
        PatentData['portee'] = ExtraitKind(pat)
    except:
        PatentData['portee'] = 'UNKNOWN'
    date = ExtractionDate(pat)
    
    try:
        PatentData['classification'] = UnNest2List(ExtraitIPCR2(pat))
    except:
        PatentData['classification'] =''
    if str(pat).count('abstract')>0:
        if u'abstract' in pat.keys():
            if isinstance(pat[u'abstract'], dict):
                tempor = RecupAbstract(pat[u'abstract'])
                for cle in tempor:
                    PatentData[cle] = tempor[cle] 
            else:
                for resum in pat[u'abstract']:
                    tempor = RecupAbstract(resum)
                    for cle in tempor:
                        PatentData[cle] = tempor[cle] 
        #should intent to recursively find abstract...
    else:
        PatentData[u'abstract'] = ''
    try:
        PatentData['citations'] = len(pat[u'bibliographic-data'][u'references-cited']['citation'])
    except:
        PatentData['citations'] = 0
    try:
        if pat[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
            PatentData['priority-active-indicator'] = 1
    except:
        PatentData['priority-active-indicator'] = 0
        pass ## should check what is "active indicator" for patent
    try:
        if pat[u'bibliographic-data'][u'application-reference'][u'@is-representative'] == u'YES':
            PatentData['representative'] = 1                            
#                            PatentData['representative'] = True
        
    except:
        try:
            PatentData['application-ref'] = len(pat[u'bibliographic-data'][u'application-reference'][u'document-id'])/3.0 #epodoc, docdb, original... if one is missing, biais
        except:
            PatentData['application-ref'] = 0 # no application
        PatentData['representative'] = 0
    try:
        PatentData['publication-ref'] = pat[u'bibliographic-data'][u'publication-reference']
    except:
        PatentData['publication-ref'] = 0
    
    #doing some cleaning
        #transforming dates string in dates
    if date is not None and date != '':
        PatentData['date'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
#        print "patent date", PatentData['date']
    else:
        PatentData['date'] = datetime.date(datetime.date.today().year+2, 1, 1)
        #cleaning classsications
    #unesting everything
    for cle in PatentData.keys():
        if isinstance(PatentData[cle], list):
            PatentData[cle] = UnNest2List(PatentData[cle])
        
    return PatentData    


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
                if isinstance(tempo, dict):
                    if u"text" in tempo.keys():
                            classTemp = tempo['text']['$'].replace(' ','')
                            if AlphaTest(classTemp[len(classTemp)-2:len(classTemp)]):
                                res.append(classTemp[:len(classTemp)-2])
                            else:
                                res.append(classTemp)
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
