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
OPS_REST_VERSION = '3.1' 

def ops_request_data2( url, param = {}):
    headers = {'Accept': 'application/json',}
    compteur = 0
    requete = requests.get(url, headers=headers, params = param)
    while not (requete.status_code <300) and compteur < 30:
        time.sleep(6)
        requete = requests.get(url, headers=headers, params = param)
        compteur +=1
        print "attemps failed, trying again", compteur,'   ', param
    return json.loads(requete.text)
 
def ops_request_data( url):
    headers = {'Accept': 'application/json',}
    requete = requests.get(url, headers=headers)
    if requete.status_code < 300:
        return json.loads(requete.text)       
    else:
        return requete.text
    
def ops_request_construct( params ):
    """Function used to build up the url using the dictionnary parameter (params)
    keys used here are ['rest_version'],['service'],['reference'],['input_type']['input'] 
    these will build an url on the form :
    http://ops.epo.org/rest_version/service/reference-type/input-format/input/[endpoint]/[constituent(s)]"""
        # rest_version=OPS_REST_VERSION,
        # service='number-service',
        # reference='application',
        # input_type='original',
        # input='US.7654321', 
        # output_format='docdb'):

    # protocol/authority/prefix/service/reference-type/input-format/input/[endpoint]/[constituent(s)]/output-format
    url = 'ops.epo.org/{rest_version}/rest-services/{service}/{reference}/{input_type}/'.format( #{input}
        rest_version     = params['rest_version'],        
        service         = params['service'],
        reference         = params['reference'],
        input_type         = params['input_type'],
#        input             = params['input'], #'US.11380365.A1.20070515',
        output_format     = params['output_format'],
        )
    url = 'http://' + url.replace('//', '/') #in case of empty values in params.values()
    
    return url

def ops_request_construct2( params ):
    """Function used to build up the url using the dictionnary parameter (params)
    keys used here are ['rest_version'],['service'],['reference'],['input_type']['input'] 
    these will build an url on the form :
    http://ops.epo.org/rest_version/service/reference-type/input-format/input/[endpoint]/[constituent(s)]"""
        # rest_version=OPS_REST_VERSION,
        # service='number-service',
        # reference='application',
        # input_type='original',
        # input='US.7654321', 
        # output_format='docdb'):

    # protocol/authority/prefix/service/reference-type/input-format/input/[endpoint]/[constituent(s)]/output-format
    url = 'ops.epo.org/{rest_version}/rest-services/{service}/{reference}/{docformat}/{PatentNum}/{outputcontent}'.format( #
        rest_version     = params['rest_version'],        
        service         = params['service'],
        reference         = params['reference'],
        docformat        = params['docformat'],
        PatentNum             = params['PatentNum'], #'US.11380365.A1.20070515',
        outputcontent     = params['outputcontent'],
        )
    url = 'http://' + url.replace('//', '/') #in case of empty values in params.values()
    
    return url
    
def construit_params(srv = 'published-data', ref = 'search', in_type = 'abstract', entree = 'epodoc', output = 'biblio'):
     # protocol/authority/prefix/service/reference-type/input-format/input/[endpoint]/[constituent(s)]/output-format
    #function to build up parameters that will be used to construct the url targetted    
    params = {
        'rest_version'     : OPS_REST_VERSION,        
        'service'         : srv,
        'reference'     :  ref, # application, priority
        'input_type'     : in_type,
        'output_format' : output,
      #  'input'         : entree,
    }  
#       
    return params

def construit_params2(srv = 'published-data', ref = 'search', PatentNum ='', docformat = 'epodoc', outputcontent = 'biblio'):
     # protocol/authority/prefix/service/reference-type/docformat/PatentNum/[endpoint]/[constituent(s)]/output-format
    #function to build up parameters that will be used to construct the url targetted    
    params = {
        'rest_version'     : OPS_REST_VERSION,        
        'service'         : srv,
        'reference'     :  ref, # application, priority
        'docformat'     : docformat,
        'outputcontent' : outputcontent,
        'PatentNum'         : PatentNum,
        
    }  
#       
    return params
# hight level functions

def TransformeCle(cle):
    cle = cle.replace("u'","'", cle.count("u'"))
    cle = cle.replace("']['",'][',cle.count("']['"))
    cle = cle.split("][")
    temp =[]
    for cl in cle:
        cl =cl.replace('[','')
        cl =cl.replace(']','')
        cl =cl.replace("'","")
        temp.append(cl)  
    return temp
    
def ExtraitContenuDico(dico, cle):
    cle = TransformeCle(cle)
    cle2 = ''
    for k in cle[1:]:
        cle2 += "[u'" + k +']'
    
        
    if type(dico[cle[0]]) == type(dict()) and cle != '$':
        return ExtraitContenuDico(dico[cle[0]], cle2)
    elif type(dico[cle[0]]) == type([]):
        res = ''
        
        for contenu in dico[cle[0]]:
            res += ExtraitContenuDico(contenu, cle2) +'\n'
        return res
    elif cle[0] =='$' and dico.has_key('$'):
        return dico[cle[0]]
    elif len(cle) == 1:
        try:
            return dico[cle[0]]
        except:
            pass
    else:
            print "do know what tot do for U"
            return None
        

def ExtraitNb(request):
    parametres = construit_params('published-data', 'search', 'abstract', '', '') 
    url = ops_request_construct( parametres )

    req = ops_request_data2(url, param = {'q':request})
    #time.sleep(6) #10 recherches par minute MaX : http://www.epo.org/searching/free/fair-use.html
    #if type(req) == type(dict()):
        #totalRes = int(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
    return req
        
def ExtraitClaim (where, brev):
# where : priority or  application or publication
#http://ops.epo.org/3.0/rest-services/published-data/priority/docdb/GB2487055/claims
    # format epodoc or docdb
    #Not working as it is"
    pars = construit_params2 (ref = where, PatentNum = brev, outputcontent = 'claims', docformat = 'docdb')
    url = ops_request_construct2( pars)
    data = ops_request_data( url)
    donnees = None
    cle = "[u'ops:world-patent-data'][u'ftxt:fulltext-documents'][u'ftxt:fulltext-document'][u'claims'][u'claim'][u'claim-text']['$']"

    # la cle la plus directe, nomrmalement l'arbre est récursivement parcouru en cas de variantes
    if type(data) == type(dict()):
        donnees = ExtraitContenuDico(data, cle)
    if donnees == None:
        pars = construit_params2 (ref = where, PatentNum = brev, outputcontent = 'claims', docformat = 'epodoc')
        url = ops_request_construct2( pars)
        data = ops_request_data( url)
        if type(data) == type(dict()):
            donnees = ExtraitContenuDico(data, cle)
        else:
            #print 'toujours rien', brev,'  ', url
            return None
    else:
        return donnees
                


def ExtraitBrevetMotCle(query):
    # renvoi la liste des brevets associés à un mot clé  
    '''extracts the list of patents associated to a query (in CPL language ?)
    return a list type of patents dictionnaries
    if they are patents attached to the keyword, 
    res[u'ops:world-patent-data'][u'ops:biblio-search'][u'ops:search-result'][u'exchange-documents']
    contains the list of dictionnary (again) patents
    example : 
    pp.pprint(Res[u'ops:world-patent-data'][u'ops:biblio-search'][u'ops:search-result'][u'exchange-documents'][0][u'exchange-document'][u'bibliographic-data'])
{   u'publication-reference': {   u'document-id': [   {   u'@document-id-type': u'docdb',
                                                          u'country': {   u'$': u'WO'},
                                                          u'date': {   u'$': u'20110210'},
                                                          u'doc-number': {   u'$': u'2011015115'},
                                                          u'kind': {   u'$': u'A1'}},
                                                      {   u'@document-id-type': u'epodoc',
                                                          u'date': {   u'$': u'20110210'},
                                                          u'doc-number': {   u'$': u'WO2011015115'}}]}}
    '''
    requete = query
    plage = ''
      
    # Compteurs et variables pour le traitement
    totalRes = 2
    deb = 1
    end = 1
    Res = [] # la liste des résultats
    cpt = 0
    while end < totalRes: 
        end = deb + 24  # epo ne renvoi que 25 résultat
        plage = str(deb) + '-' + str(end)
        parametres = construit_params('published-data', 'search', 'abstract', '', '') 
        url = ops_request_construct( parametres )
        
        if deb >24:
            req = ops_request_data2(url, param = {'q':requete, 'range':plage})
        else:
            req = ops_request_data2(url, param = {'q':requete})
        time.sleep(6) #10 recherches par minute MaX : http://www.epo.org/searching/free/fair-use.html
        if type(req) == type(dict()):
            totalRes = int(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'@total-result-count'])
            if totalRes > 1:
                for k in req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'exchange-documents']:
                    Res.append(k)
                deb = int(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:range'][u'@end']) + 1
            elif totalRes == 1:
                Res.append(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'exchange-documents'])
            else:
                print "no results", totalRes
#            try:
#                if len(Res)>0:
#                    Res += req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'exchange-documents']
#                else:
#                    Res.append(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:search-result'][u'exchange-documents'])
#                deb = int(req[u'ops:world-patent-data'][ u'ops:biblio-search'][u'ops:range'][u'@end']) + 1
#            except:
#                print "paté à cause de ", req, type(req), req.keys()
            
            if cpt == 0 :
                print totalRes
            cpt +=1
        else:
            print "robot détecté et prié d'attendre"
            print "fin de collecte de données"
            end = totalRes
    return Res
 

def ExtractionDate (Brev):
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
    try:
        return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@kind']
    except:
        print 'something bad, Kind'
        return None

def ExtraitTitleEn(Brev):
    try:
        return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['invention-title'][0]['$']
    except:
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data']['invention-title']['$']
        except:
            print 'something bad, title'
            return None

def ExtraitCountry(Brev):
    try:
        return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@country']
    except:
        print 'something bad, country'
        return None

def ExtraitClassification(DicoOuLst):
    if type(DicoOuLst) == type(dict()):
        temp = DicoOuLst['section']['$'] +DicoOuLst['class']['$'] + DicoOuLst['subclass']['$'] +DicoOuLst['main-group']['$'] + '/' +DicoOuLst['subgroup']['$'] +' '+ DicoOuLst['classification-value']['$']
        return temp
    else:
        res = []
        for Dico in DicoOuLst:
            temp = Dico['section']['$'] +Dico['class']['$'] + Dico['subclass']['$'] +Dico['main-group']['$'] + '/' +Dico['subgroup']['$'] +' '+ Dico['classification-value']['$']
#    section, class, subclass, main-group / subgroup Classif value
            res.append(temp)
    return res
    
def ExtraitIPCR2(Brevet):
    res = []
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
    try:
        Brev = Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document'][u'bibliographic-data'][u'parties']
    except:
        return None
    if Brev.has_key(content+'s'):
        for truc in Brev[content+'s'][content]:
            if truc[u'@data-format'] == Format:
                res.append(truc[content+u'-name'][u'name'][u'$'])
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

# testing part

#params = construit_params()
#url = ops_request_construct( params )
#Req = ops_request_data( url )
##
##print Req.keys()
##print type(Req) , len(Req)
##print "results expected for this request", Req[u'ops:world-patent-data'][u'ops:biblio-search'][u'@total-result-count']
##
##print "the same request gathering recursivelly all results"
#Req2 = ExtraitBrevetMotCle('lentille and rue')
#print len(Req2)
#import pprint
#pp = pprint.PrettyPrinter(indent=2)
#
#
#params = construit_params(srv='published-data', ref='publication', 
#                          in_type='docdb', entree='WO2011015115', requete='',
#                          plage='', output='')
#                          
#url = ops_request_construct(params)
#print url
#Req = ops_request_data( url)
#pp.pprint( Req[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document'] )
#print Req[u'ops:world-patent-data'][u'exchange-documents'][u'exchange-document']
##ExtraitsAppliquants
##ExtraitPays
##ExtraitPortee
##ExtraitCPC
##ExtraitIPC
#print "les inventeurs :"
#print ExtraitInventeurs(Req, 'epodoc')
#print "les appliquants :"
#print ExtraitsAppliquants(Req, 'epodoc')
#print "le pays d'origine :", ExtraitPays(Req)
#
#print "la portee ;", ExtraitPortee(Req)
#print "la classification IPCR :"
#print ExtraitIPCR(Req, Format = None)  # if Format equal something will reformat content return avoiding double spaces