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

def Initialize(bool1, bool2):
    if bool1 and bool2:
        return 0
    else:
        return "All"
        
def coupeEnMots(texte):
    "returns a list of words cleaned from punctuation, digits and other signs"
    if isinstance(texte, list):
        texte = ' '.join(texte)
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

def Update(dicoUpdated, dico):
    for cle in dicoUpdated.keys():
        if cle in dico.keys():
            if isinstance(dicoUpdated, list):
                if isinstance(dico, list):
                    for cont in dico[cle]:
                        if cont not in dicoUpdated[cle]:
                            dicoUpdated[cle].append(cont)
                elif dico[cle] not in dicoUpdated[cle]:
                    dicoUpdated[cle].append(dico[cle])
                else:
                    pass
            else:
                dicoUpdated[cle] = [dicoUpdated[cle]]
                if isinstance(dico, list):
                    for cont in dico[cle]:
                        if cont not in dicoUpdated[cle]:
                            dicoUpdated[cle].append(cont)
                elif dico[cle] not in dicoUpdated[cle]:
                    dicoUpdated[cle].append(dico[cle])
                else:
                    pass
        else:
            pass
    return dicoUpdated


def GetFamilly(client, brev, rep):
    from OPS2NetUtils2 import ExtractClassificationSimple2, Formate, SeparateCountryField, ExtractAbstract
    import epo_ops
    import datetime
    ResultContents = rep
    lstres = []
    comptExcept = 0
    
#    try:
#        url ='http://ops.epo.org/3.1/rest-services/family/publication/docdb/' +brev['label'] +'/biblio'
#        
#        data = requests.get(url, headers = headers)
    dico = None
    try:
        data = client.family('publication', epo_ops.models.Epodoc(brev['label']), 'biblio')
        data = data.json()
        dico = data[u'ops:world-patent-data'][u'ops:patent-family'][u'ops:family-member']
        #PatentDataFam[brev['label']] = dict()
        if type(dico) == type(dict()):
            dico=[dico]
        cpt = 1
    except:
        try:
            data = client.family('publication', epo_ops.models.Docdb(brev['label'][2:], brev['label'][0:2],brev['portee']))
            data = data.json()
            dico = data[u'ops:world-patent-data'][u'ops:patent-family'][u'ops:family-member']
            #PatentDataFam[brev['label']] = dict()
            if type(dico) == type(dict()):
                dico=[dico]
            cpt = 1
        except:

            print "nothing found for ", brev
            print "ignoring"
            return None

    if dico is not None:

        for donnee in dico:
            Go =True
            Brevet=dict(dict(dict(dict())))
            Brevet[u'ops:world-patent-data'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'] =dict()
            Brevet[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'] = donnee #hum no sure that it is a good way
            PatentData = dict()
            Req = Brevet
               
            try:
                PatentData[u'label'] = donnee[u'exchange-document'][u'bibliographic-data'][u'publication-reference'][u'document-id'][1][u'doc-number'][u'$']
            except:
                try:
                    PatentData[u'label'] = donnee[u'publication-reference'][u'document-id'][1][u'doc-number']['$']
                except:
                    print "no label ?"
                    Go = False
                   # print pprint.pprint(donnee)

            if Go:
                #PatentDataFam[PatentData['label']] = dict()
                PatentData[u'titre'] = Clean(ExtraitTitleEn(Req))                  
#                    print "Patent title(s)", PatentData['titre']
              
                PatentData[u'inventeur'] = Clean(ExtraitParties(Req, 'inventor', 'epodoc'))
#                    print "Inventors : ",  PatentData['inventeur']
                PatentData[u'applicant'] = Clean(ExtraitParties(Req, 'applicant','epodoc'))
#                    print "Applicants : ", PatentData['applicant']
                PatentData[u'pays'] = ExtraitCountry(Req)
                
                PatentData[u'portee'] = ExtraitKind(Req)
                try:
                    PatentData[u'classification'] = ExtraitIPCR2(Req)
                except:
                    PatentData[u'classification'] = ''
                if isinstance(PatentData[u'classification'], list):
                        for classif in PatentData[u'classification']:
                            PatentData2 = ExtractClassificationSimple2(classif)
                            for cle in PatentData2.keys():
                                if cle in PatentData.keys() and PatentData2[cle] not in PatentData[cle]:
                                    if PatentData[cle] == '':
                                        PatentData[cle] = []
                                    if isinstance(PatentData2[cle], list):
                                        for cont in PatentData2[cle]:
                                            if cont not in PatentData[cle]:
                                                PatentData[cle].append(cont)
                                    else:
                                        if PatentData2[cle] not in PatentData[cle]:
                                            PatentData[cle].append(PatentData2[cle])
                                else:
                                    PatentData[cle] = []
                                    if isinstance(PatentData2[cle], list):
                                        for cont in PatentData2[cle]:
                                            if cont not in PatentData[cle]:
                                                PatentData[cle].append(cont)
                                    else:
                                        PatentData[cle].append(PatentData2[cle])
                elif PatentData[u'classification'] != '':
                        PatentData2 = ExtractClassificationSimple2(PatentData[u'classification'])
                        for cle in PatentData2.keys():
                            if cle in PatentData.keys() and PatentData2[cle] not in PatentData[cle]:
                                if PatentData[cle] == '':
                                    PatentData[cle] = []
                                if isinstance(PatentData2[cle], list):
                                    for cont in PatentData2[cle]:
                                        if cont not in PatentData[cle]:
                                            PatentData[cle].append(cont)
                                else:
                                    PatentData[cle] = []
                                    PatentData[cle].append(PatentData2[cle])
                            elif cle not in PatentData.keys(): 
                                PatentData[cle] = []
                                if isinstance(PatentData2[cle], list):
                                    for cont in PatentData2[cle]:
                                        if cont not in PatentData[cle]:
                                            PatentData[cle].append(cont)
                                else:
                                    if PatentData2[cle] not in PatentData[cle]:
                                        PatentData[cle].append(PatentData2[cle])
                                #                print classif
                del(PatentData[u'classification'])
                PatentData[u'applicant'] = Formate(PatentData['applicant'], PatentData['pays'])
                
                # remember inventor original writing form to reuse in the url property of the node
                PatentData[u'inventeur'] = Formate(PatentData['inventeur'], PatentData['pays'])
                PatentData = SeparateCountryField(PatentData)

#            #print "Classification Reduced: ", PatentData['ClassifReduite']
                date = ExtractionDate(Req) #priority claim first date time
                if date is not None and date != "":
                    PatentData[u'date'] = date[0:4] +'-'+ date[4:6] +'-'+ date[6:]
                    PatentData[u'dateDate'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
 #                       print "patent date", PatentData['date']
                else:
                    PatentData[u'dateDate'] = datetime.date.today()
                    PatentData[u'date'] = str(datetime.date.today().year) +'-' + str(datetime.date.today().month) + '-' + str(datetime.date.today().day)
                #try: #hum straight forward may be not the good choice
                try:    
                    if u'references-cited' in donnee[u'exchange-document'][u'bibliographic-data'].keys():
                        if "citation"  in donnee[u'exchange-document'][u'bibliographic-data'][u'references-cited'].keys():
                            PatentData[u'citations'] = len(donnee[u'exchange-document'][u'bibliographic-data'][u'references-cited'][u'citation'])
                    else:
                        PatentData[u'citations'] = 0
                except:
                    PatentData[u'citations'] = 0 
                    #it is may be an Application patent. Hence, no CIB, no citation... so I should avoid it
#                        print " *********************************   "
                
                #if cpt == 1:#not the first one !!!!
                try:
                    if donnee[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
                        PatentData['priority-active-indicator'] = 1
                except:
                    PatentData['priority-active-indicator'] = 0
                     ## should check what is "active indicator" for patent
                try:
                    if donnee[u'application-reference'][u'@is-representative'] == u'YES':
                        PatentData['representative'] = 1                            
#                            PatentData['representative'] = True
                except:
                    PatentData[u'representative'] = 0
                        # should check what is reprensentativeness for patent
        
                PatentData[u'family lenght'] = len(dico)
                

                for cle in PatentData.keys():
                    if isinstance(PatentData[cle], list):
                        if len(PatentData[cle]) == 1:
                            PatentData[cle] == PatentData[cle][0] #UnNesting
                if None not in PatentData.values():
                    IRAM = '**** *Label_' + PatentData[u'label'] +' *Country_'+PatentData[u'pays']+ ' *CIB3_'+'-'.join(PatentData[u'IPCR3']) + ' *CIB1_'+'-'.join(PatentData[u'IPCR1']) + ' *CIB4_'+'-'.join(PatentData[u'IPCR4']) + ' *Date_' + str(PatentData[u'dateDate'].year) + ' *Applicant_'+'-'.join(coupeEnMots(str(PatentData[u'applicant'])))
                    TXT=dict()
                    if isinstance(donnee[u'exchange-document'], list):
                        for tempo in donnee[u'exchange-document']:
                            if tempo.has_key('abstract'):
                                txtTemp = ExtractAbstract(tempo['abstract'])
                                for cleLang in txtTemp:
                                    if TXT.has_key(cleLang):
                                        TXT[cleLang] += txtTemp[cleLang]
                                    else:
                                        TXT[cleLang] = txtTemp[cleLang]
                    else:
                      if donnee[u'exchange-document'].has_key('abstract'):
                          TXT = ExtractAbstract(donnee[u'exchange-document'][u'abstract'])
                    for lang in TXT.keys():                            
                        EcritContenu(IRAM + ' *Contenu_Abstract \n' + TXT[lang], ResultContents+'//FamiliesAbstracts//'+lang+'-'+PatentData['label']+'.txt')   

                    lstres.append(PatentData)
                    cpt += 1
                else:                        
#                    print "hum... missing values... avoiding this patent"
                    #print "Cleaning data"
                    for key in PatentData.keys():
                        if isinstance(PatentData[key], list):
                            if len(PatentData[key])==1:
                                PatentData[key] = PatentData[key][0]
                        elif isinstance(PatentData[key], unicode):
                            pass
                        elif isinstance(PatentData[key], unicode):
                            PatentData[key] = unicode(PatentData[key])
                        else:
                            PatentData[key] = u''

        datemin = datetime.date(3000, 1, 1)
        
        for brevet in lstres:
            if brevet.has_key('representative'):
                if brevet['dateDate'] < datemin:
                    datemin = brevet['dateDate']
                    prior = brevet['label']
        if 'prior' not in locals():
            prior = brev['label']
        for brevet in lstres:
            brevet['prior'] = prior
#        print "exceptions ", comptExcept
#        print len(lstres), ' patents added'
    return lstres

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
        PatentData[u'inventeur'] = Clean(ExtraitParties(pat, 'inventor', 'epodoc'))
    except:
        PatentData[u'inventeur'] = u'UNKNOWN'
    try:
        PatentData[u'applicant'] = Clean(ExtraitParties(pat, 'applicant','epodoc'))
    except:
        PatentData[u'applicant'] = u'UNKNOWN'
    try:
        PatentData[u'titre'] = Clean(ExtraitTitleEn(pat))
    except:
        PatentData[u'titre'] = u'UNKNOWN'
    try:
        PatentData[u'pays'] = ExtraitCountry(pat)
    except:
        PatentData[u'pays']  = u'UNKNOWN'
    try:    
        PatentData[u'portee'] = ExtraitKind(pat)
    except:
        PatentData[u'portee'] = u'UNKNOWN'
    date = ExtractionDate(pat)
    
    try:
        PatentData[u'classification'] = UnNest2List(ExtraitIPCR2(pat))
    except:
        PatentData[u'classification'] =''
    if str(pat).count(u'abstract')>0:
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
        PatentData[u'citations'] = len(pat[u'bibliographic-data'][u'references-cited']['citation'])
    except:
        PatentData[u'citations'] = 0
    try:
        if pat[u'priority-claim'][u'priority-active-indicator']['$'] == u'YES':
            PatentData[u'priority-active-indicator'] = 1
    except:
        PatentData[u'priority-active-indicator'] = 0
        pass ## should check what is "active indicator" for patent
    try:
        if pat[u'bibliographic-data'][u'application-reference'][u'@is-representative'] == u'YES':
            PatentData[u'representative'] = 1                            
#                            PatentData['representative'] = True
        
    except:
        try:
            PatentData[u'application-ref'] = len(pat[u'bibliographic-data'][u'application-reference'][u'document-id'])/3.0 #epodoc, docdb, original... if one is missing, biais
        except:
            PatentData[u'application-ref'] = 0 # no application
        PatentData[u'representative'] = 0
    try:
        PatentData[u'publication-ref'] = pat[u'bibliographic-data'][u'publication-reference']
    except:
        PatentData[u'publication-ref'] = 0
    
    #doing some cleaning
        #transforming dates string in dates
    if date is not None and date != '':
        PatentData[u'dateDate'] = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:]))
        PatentData[u'date'] = str(date[0:4])+'-'+str(date[4:6])+'-'+str(date[6:])
#        print "patent date", PatentData['date']
    else:
        tempodate= datetime.date(datetime.date.today().year+2, 1, 1) #adding two year arbitrary
        PatentData[u'dateDate'] = tempodate
        PatentData[u'date'] = str(tempodate.year)+'-'+str(tempodate.month)+'-'+str(tempodate.day)

        #cleaning classsications
    #unesting everything
    for cle in PatentData.keys():
        if isinstance(PatentData[cle], list):
            PatentData[cle] = UnNest2List(PatentData[cle])
        
    return PatentData    


def Clean(truc):
    if type(truc) == type(u''):
        temp = truc.translate('utf8')
#        temp = truc.replace(u'\x80', '')
#        temp = temp.replace(u'\x82', '')
#        temp = temp.replace(u'\u2002', '')
#        temp = temp.replace(u"\xe2", "")
#        string=temp.replace(u'\x80', '')
#        string=string.replace(u'\x82', '')
#        string=string.replace(u'\xf6', '')
#        string = string.replace(u'\xe2', '', string.count(u'\xe2'))
#        string = string.replace(u'\x80', '', string.count(u'\x80'))
#        string = string.replace(u'\x82', '', string.count(u'\x82'))
#        string = string.replace(u'\xe9', '', string.count(u'\xe9'))
#        string = string.replace(u'\xd6', '', string.count(u'\xd6'))
#        string = string.replace(u'\xd2', '', string.count(u'\xd2'))
#        string = string.replace(u'\xf6', '', string.count(u'\xf6'))
#        string = string.replace(u'\xe4', '', string.count(u'\xe4'))
#        string = string.replace(u'\xe7', '', string.count(u'\xe7'))
#        string = string.replace(u'\xfa', '', string.count(u'\xfa'))
#        string = string.replace(u'\xe1', '', string.count(u'\xe1'))
#        string = string.replace(u'\xf3', '', string.count(u'\xf3'))
#        string = string.replace(u'\xed', '', string.count(u'\xed'))
#        string = string.replace(u'\xe7', '', string.count(u'\xe7'))  
#        string = string.replace(u'\xf1', '', string.count(u'\xf1')) 
#        string = string.replace(u'\xf2', '', string.count(u'\xf2'))    
#        string = string.replace(u'\xf3', '', string.count(u'\xf3')) 
#        string = string.replace(u'\xf4', '', string.count(u'\xf4'))    
#        string = string.replace(u'\xf5', '', string.count(u'\xf5')) 
#        string = string.replace(u'\xf6', '', string.count(u'\xf6'))    
#        string = string.replace(u'\xf7', '', string.count(u'\xf7')) 
#        string = string.replace(u'\xf8', '', string.count(u'\xf8'))
#        string = string.replace(u'\xf9', '', string.count(u'\xf9')) 
#        string = string.replace(u'\xfa', '', string.count(u'\xfa'))
#        string = string.replace(u'\xfb', '', string.count(u'\xfb')) 
#        string = string.replace(u'\xfc', '', string.count(u'\xfc'))
#        string = string.replace(u'\xfd', '', string.count(u'\xfd')) 
#        string = string.replace(u'\xfe', '', string.count(u'\xfe'))     
#        string = string.replace(u'\xeb', '', string.count(u'\xeb'))
#        string = string.replace(u'\xef', '', string.count(u'\xef'))
#        string = string.replace(u'\xc9', '', string.count(u'\xc9'))
#        string = string.replace(u'\xc4', '', string.count(u'\xc4'))
#        string = string.replace(u'\xc3', '', string.count(u'\xc3'))
#        string = string.replace(u'\xc2', '', string.count(u'\xc2'))
#        string = string.replace(u'\xc1', '', string.count(u'\xc1'))
#        string = string.replace(u'\xc5', '', string.count(u'\xc5'))
#        string = string.replace(u'\xc6', '', string.count(u'\xc6'))
#        string = string.replace(u'\xc7', '', string.count(u'\xc7'))
#        string = string.replace(u'\xc8', '', string.count(u'\xc8'))
#        temp = string.replace(u'\xd1', '', string.count(u'\xd1'))
        return temp
    if isinstance(truc, list):
        if len(truc)>1:
            return [Clean(u) for u in truc]
        else:
            return Clean(truc[0])
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
#                        print "bad date", tempo
                        return ""
                else:
                    if u'date' in tempo[0].keys():
                        return tempo[0][u'date']['$'] #first on should be good
                    else:
#                        print "bad date", tempo
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
#                print 'something bad, Date'
                return None
    
def ExtraitKind(Brev):
     if u'@kind' in Brev.keys():
        return Brev[u'@kind']
     else:#retro ompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@kind']
        except:
#            print 'something bad, Kind'
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
#                print 'something bad, title'
                return None

def ExtraitCountry(Brev):
    if u'@country' in Brev.keys():
        return Brev[u'@country']
    else: #again retrocompatibility
        try:
            return Brev[u'ops:world-patent-data']['ops:biblio-search']['ops:search-result'][u'exchange-documents'][u'exchange-document']['@country']
        except:
#            print 'something bad, country'
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
#            print 'something bad, IPCR'
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
