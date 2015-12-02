# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 12:05:05 2014

@author: dreymond
"""

import json

import pickle
#import bs4
from P2N_Lib import ReturnBoolean, Decoupe, UnNest3, UrlInventorBuild, UrlApplicantBuild, UrlIPCRBuild
import datetime
aujourd = datetime.date.today()

with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()
            if lig.count('GatherContent')>0:
                Gather = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherBiblio')>0:
                GatherBiblio = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherPatent')>0:
                GatherPatent = ReturnBoolean(lig.split(':')[1].strip())
            if lig.count('GatherFamilly')>0:
                GatherFamilly = ReturnBoolean(lig.split(':')[1].strip())

rep = ndf

# the list of keys for filtering for datatable
clesRef = ['label', 'title', 'year','priority-active-indicator', 
'IPCR11', 'kind', 'applicant', 'country', 'inventor', 'representative', 'IPCR4', 
'IPCR7', "Inventor-Country", "Applicant-Country", "equivalents", "CPC", u'references', u'Citations', u'CitedBy']

ListBiblioPath = '..//DONNEES//'+rep+'//PatentBiblios'#Biblio'
#ListPatentPath = '..//DONNEES//'+rep+'//PatentLists'#List
ResultPathContent = '..//DONNEES//'+rep #+'//PatentContentsHTML'
temporPath = '..//DONNEES//'+rep+'//tempo'



with open(ListBiblioPath+'//'+ndf, 'r') as data:
    LstBrevet = pickle.load(data)
    

data = LstBrevet
LstBrevet = data['brevets']    
if data.has_key('requete'): 
    requete = data["requete"]
if data.has_key('number'):
    print "Found ", data["number"], " patents! Formating to HMTL tables"
    
LstExp = [] 



import codecs
#if rep != ndf:
#    if ndf.lower() == 'families'+rep.lower():
#        #ndf = 'Families'+ ndf
#        Modele = "ModeleFamille.html"
#else:
#    

compt  = 0
Dones = []
Double = dict() #dictionnary to manage multiple bib entries (same authors and date)
with codecs.open(ResultPathContent + '//'  +ndf+'.bib', 'w', 'utf-8') as resFic:
    cleBib = ['year', 'kind', 'title', 'inventor', 'IPCR11', 'label', 'country']
    for bre in LstBrevet:
        if len(cleBib) == len([cle for cle in cleBib if cle in bre.keys()]):
            Gogo = True #checkin consistency
#==============================================================================
#            for cle in cleBib:
           # some cleaning in old version of gathered. Should be ok in V2
#                 Gogo = Gogo * (bre[cle] is not None)
#                 Gogo = Gogo * (u'None' not in bre[cle])
#                 Gogo = Gogo * ( bre[cle] != u'')
#==============================================================================
            if Gogo>0:
                if "A" in ' '.join(bre['kind']) or "B" in ' '.join(bre['kind']) or "C" in ' '.join(bre['kind']): #filter patent list again their status... only published
                    if bre['dateDate'] is not None or bre['dateDate'] != u'None' or bre['dateDate'] != u'' or u'None' not in bre['dateDate'] or None in bre['dateDate']:
                        if len(bre['year'])>0 and not isinstance(bre['date'], list):
                            teatime=bre['date'].split('-')
                            bre['dateDate'] = datetime.date(int(teatime[0]), int(teatime[1]), int(teatime[2]))
                        elif len(bre['year'])>0:
                            teatime=bre['date'][0].split('-')
                            bre['dateDate'] = datetime.date(int(teatime[0]), int(teatime[1]), int(teatime[2]))

#                        # hum last test prooves that they is a bug in collector for dateDate field
                    if isinstance(bre['dateDate'], list):
                        Date = bre['dateDate'][0] #first publication (hope so)
                    else:
                        Date = bre['dateDate']
#                    else:
#                        if isinstance(bre['year'], list):
#                            temp= bre['year'][0] #first publication
#                            temp = temp.split('-')
#                            Date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
#                        else:
#                            temp = bre['year']
#                            temp = temp.split('-')
#                            Date = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
                            
                    if isinstance(bre['inventor'], list):
                        try:                        
                            entryName=bre['inventor'][0].split(' ')[0]+'etAl'+str(Date.year)
                        except:
                            print
                        tempolist = [nom.replace(' ', ', ', 1).title() for nom in bre['inventor']]
                        Authors = unicode(' and '.join(tempolist))
                    else:
                        entryName=bre['inventor'].split(' ')[0]+'etAl'+str(Date.year)
                        Authors = bre['inventor'].replace(' ', ', ', 1).title()
                    entryName = entryName.replace("'", "")
                    if entryName in Dones:
                        if Double.has_key(entryName):
                            Double[entryName] += 1
                        else:
                            Double[entryName] = 1
                        entryName+=str(Double[entryName])
                    if isinstance(bre['country'], list):
                        if len(bre['country']) ==1:
                            bre['country'] = bre['country'][0]
                    Dones.append(entryName)
                    resFic.write(u'@Patent{'+entryName+',\n')
                    resFic.write(u'\t author={' + Authors + '},\n')
                    resFic.write(u"\t title = {"+unicode(bre['title']).capitalize() +"},\n")
                    resFic.write(u"\t year = {" +str(Date.year)+ "},\n")
                    resFic.write(u"\t month = {" +str(Date.month)+ "},\n")
                    resFic.write(u"\t day = {" +str(Date.day)+ "},\n")
                    resFic.write(u"\t number = {" +str(bre['label'])+ "},\n")
                    resFic.write(u"\t location = {" +str(bre['country'])+ "},\n")
                    if isinstance(bre['IPCR11'], list):
                        resFic.write(u"\t IPC_class = {" + str(', '.join(bre['IPCR11'])) + "},\n")
                    else:
                        resFic.write(u"\t IPC_class = {" + str(bre['IPCR11']) + "},\n")
                    resFic.write(u"\t url = {" +"http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query="+str(bre['label'])+"&locale=en_EP&DB=EPODOC" + "},\n")
                    resFic.write(u"\t urlyear = {" +str(aujourd.year)+ "},\n")
                    resFic.write(u"\t urlmonth = {" +str(aujourd.month)+ "},\n")
                    resFic.write(u"\t urlday = {" +str(aujourd.day)+ "},\n")
                    resFic.write(u"}\n \n")
                
            compt +=1
        
print compt, ' bibliographic data added in ', ndf +'.bib file'
print "Other bibliographic entry aren't consistent nor A, B, C statuses" 



#os.system('start firefox -url '+ URLs.replace('//','/') )
