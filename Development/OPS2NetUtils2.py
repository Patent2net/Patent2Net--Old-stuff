# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 08:50:16 2014

@author: dreymond
"""
IPCRCodes = {'A':'HUMAN NECESSITIES', 'B':'PERFORMING OPERATIONS; TRANSPORTING', 'C':'CHEMISTRY; METALLURGY',
'D':'TEXTILES; PAPER', 'E':'FIXED CONSTRUCTIONS', 'F':'MECHANICAL ENGINEERING; LIGHTING; HEATING; WEAPONS; BLASTING',
'G':' PHYSICS', 'H':'ELECTRICITY'}
Status = [u'A', u'B', u'C', u'U', u'Y', u'Z', u'M', u'P', u'S', u'L', u'R', u'T', u'W', u'E', u'F', u'G', u'H', u'I', u'N', u'X']
#    A – First publication level
#    B – Second publication level
#    C – Third publication level
#Group 2 – Use for utility model documents having a numbering series other than the documents of Group 1:
#    U – First publication level
#    Y – Second publication level
#    Z – Third publication level
#Group 3 – Use for special series of patent documents as specified below:
#    M – Medicament patent documents (e.g., documents previously published by FR)
#    P – Plant patent documents (e.g., published by US)
#    S – Design patent documents (e.g., published by US)
#Group 4 – Use for special types of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 3, above, as specified below:
#    L – Documents, not covered by the letter code W, relating to patent documents and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
#    R – Separately published search reports
#    T – Publication, for information or other purposes, of the translation of the whole or part of a patent document already published by another office or organization
#    W – Documents relating to utility model documents falling in Group 2 and containing bibliographic information and only the text of an abstract and/or claim(s) and, where appropriate, a drawing
#Group 5 – Use for series of patent documents not covered by Groups 1 to 4, above:
#    E – First publication level
#    F – Second publication level
#    G – Third publication level
#Group 6 – Use for series of patent documents or documents derived from/relating to patent applications and not covered by Groups 1 to 5, above, according to the special requirements of each industrial property office:
#    H
#    I
#Group 7 – Other (see paragraph 2, above):
#    N – Non-patent literature documents
#    X ]

def quote(string):
    string=string.replace(u'\x80', '')
    string=string.replace(u'\x82', '')
    import urllib.quote
    return urllib.quote(string.replace(u'\u2002', ''), safe='/\\())')
    
def change(NomDeNoeud):
    if NomDeNoeud == 'classification':
        return 'IPCR'
    if NomDeNoeud == 'pays':
        return 'country'
    if NomDeNoeud == 'inventeur':
        return 'inventor'
    return NomDeNoeud

def ExtractClassification(data):
    #Brev['classification'] = data
    res = []
    if data is not None:
        if type(data) == type ([]):
            temp = dict()
            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
                temp[key] = []
            for classif in data:
                res.append(ExtractClassification(classif)[0])
                    
        elif type(data) == type ("") or type(data) == type (u""):
            Resultat = dict()
            Resultat['classification'] = data
            data = data.replace(' ', '', data.count(' '))
            Resultat['IPCR11'] = data
                     
            Resultat['IPCR1']=data[0]
            if len(data) > 2:
                Resultat['IPCR3']= data[0:3]
            else:
                Resultat['IPCR3'] = ''
            if len(data) > 4:            
                Resultat['IPCR4']= data[0:4]
                if not Resultat['IPCR4'][3].isalpha(): # consistency control
                    Resultat['IPCR4'] = ''
                    
            else:
                Resultat['IPCR4'] = ''
            if data.count('/') >0:
                Resultat['IPCR7']= data.split('/')[0]
            else:
                Resultat['IPCR7'] = ''
            Resultat['status'] = data[len(data)-1:]
            if Resultat['status'] not in Status or data[len(data)-2].isalpha():
                 Resultat['status']= data[len(data)-2:]
                 if Resultat['status'][0] not in Status:
                     Resultat['status'] = ''
                 else:
                     Resultat['IPCR11']= data[0:len(data)-2]
            else:
                Resultat['IPCR11']= data[0:len(data)-1]
            if Resultat['IPCR11'][len(Resultat['IPCR11'])-2:len(Resultat['IPCR11'])].count('0')>1:
                Resultat['IPCR11'] = 'N/A' # consistency check : if result endswith 0, means that is an IPCR7
            
            
            res.append(Resultat)
        else:
            print "should not be here, pb in classification content"
    else:
        resultat = dict()
        for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
            resultat[ipc] = ''
        res.append(resultat)
    return res

                
    
def Formate(chaine, pays):
    """formatte la chaine pour que ce soit un noeud correct pour Gephi et autres outils :
        notation hongroise (ou bulgare :-) : CeciEstUnePhrase.
        Vire le pays le cas échéant"""
    #mem = chaine
    if chaine is not None:
        if type(chaine) == type([]):
            res = []
            for ch in chaine:
                temp = Formate(ch, pays)
                res.append(temp)
            return res
        elif len(pays) >0:
            if chaine.count(' '+pays) >0 or chaine.count('[pays]') >0:
                temp = chaine.replace(pays, '')
                if temp.count('[]') >0:
                    temp = temp.replace('[]', '')
                chaine = temp.strip()
        chaine = chaine.lower()
        chaine = chaine.title()
        chaine = chaine.replace(' ', '', chaine.count(' '))
        chaine = chaine.replace(u'\xe2\x80\x82', '', chaine.count(u'\xe2\x80\x82'))
        chaine = chaine.replace(u'\xe2', '', chaine.count(u'\xe2'))
        chaine = chaine.replace(u'\x80', '', chaine.count(u'\x80'))
        chaine = chaine.replace(u'\x82', '', chaine.count(u'\x82'))
        chaine = chaine.replace(u'\xe9', '', chaine.count(u'\xe9'))
        
        chaine = chaine.replace(u'\u2002', '', chaine.count(u'\u2002'))
        #chaine = quote(chaine)
    #    table[chaine] = mem    
        import urllib
        chaine = urllib.quote(chaine.replace(u'\u2002', ''), safe='[]')
        return chaine
    else:
        return ''
        
def genereAppariement2(lstBrev, prop1, prop2, couleur = "grey" , label = ''):
    """sur la liste des brevets, génère et renvoie la liste des appariements 
    brev[prop1];brev[prop2]\n
    dans une liste de tuples"""
    
    res = []
    if lstBrev is not None:
        if prop1 in lstBrev[0].keys():
            if prop2 in lstBrev[0].keys():
                
                for Brev in lstBrev:
                    if Brev[prop1] is not None and Brev[prop2] is not None:
                        if type(Brev[prop1]) == type(u"") and type(Brev[prop2]) == type(u""):
                            temp = (str(Formate(Brev[prop1])), str(Formate(Brev[prop2])) , dict({'color':couleur,'cat':label}))
                            res.append(temp)
                        elif type(Brev[prop1]) == type([]) and type(Brev[prop2]) == type(u""):
                            for prop in Brev[prop1]:
                                temp = (str(Formate(prop)), str(Formate(Brev[prop2])), dict({'color':couleur,'cat':label}))
                                res.append(temp)
                        elif type(Brev[prop1]) == type(u"") and type(Brev[prop2]) == type([]):
                            for prop in Brev[prop2]:
                                temp = (str(Formate(Brev[prop1])), str(Formate(prop)), dict({'color':couleur,'cat':label}))
                                res.append(temp)
                        else:
                            for pro1 in Brev[prop1]:
                                for pro2 in Brev[prop2]:
                                    temp=(str(Formate(pro1)), str(Formate(pro2)), dict({'color':couleur,'cat':label}))
                                    res.append(temp) 
                return res
    else:
        return None

def genAppar (lstBrev, p1, p2):
    res = []
#    if p1 != p2:
    if lstBrev is not None:
            if p1 in lstBrev[0].keys() and p2 in lstBrev[0].keys():
                for Brev in lstBrev:

                    if Brev[p1] is not None and Brev[p2] is not None:
                        if Brev[p1] != 'N/A' and Brev[p2] != 'N/A':
                            if type(Brev[p1]) == type(u"") and type(Brev[p2]) == type(u""):
                                temp = [Brev[p1], Brev[p2], Brev['date']]
                                res.append(temp)
                            elif type(Brev[p1]) == type(u"") and type(Brev[p2]) == type([]):
                                for k in Brev[p2]:
                                    temp = [Brev[p1], k, Brev['date']]
                                    res.append(temp)
                            elif type(Brev[p1]) == type([]) and type(Brev[p2]) == type(u""):
                                for k in Brev[p1]:
                                    temp = [k, Brev[p2], Brev['date']]
                                    res.append(temp)
                            else:
                                for k1 in Brev[p1]:
                                    cpt = Brev[p1].index(k1)
                                    for i in range(cpt, len(Brev[p2])):
                                        if k1 != Brev[p2][i]:
                                            temp = [k1, Brev[p2][i], Brev['date']]
                                            res.append(temp)
#    else:
#        if lstBrev is not None:
#            if p1 in lstBrev[0].keys():
#                for Brev in lstBrev:
#                    if Brev[p1] is not None:
#                        if type(Brev[p1]) == type(u""):
#                            temp = [Brev[p1], Brev[p2], Brev['date']]
#                            res.append(temp)
#                        else:
#                            for k in Brev[p1]:
#                                for k2 in Brev[p1]:
#                                    if k != k2:
#                                        temp = [k, k2, Brev['date']]
#                                        res.append(temp)
    return res

def GenereReseaux3(G, ListeNode, PatentList, apparie, dynamic):
    reseau = []    
    
    import datetime
    today = datetime.datetime.now().date().isoformat()
    for appar in apparie.keys():
        tempo = [appar]
        reseautemp = [(u+tempo) for u in genAppar(PatentList, apparie[appar][0], apparie[appar][1])]
        for k in reseautemp:
            if k[0] != k[1] : #on évite les boucles
                reseau.append(k)
        
    Pondere = dict()
    Prop = dict()
    DateLien = dict()
    for pair in reseau:
        if DateLien.has_key(pair[2]):
            DateLien[pair[2]].append((pair[0], pair[1], pair[3]))
        else:
            DateLien[pair[2]] = [(pair[0], pair[1], pair[3])]
    lstDate = DateLien.keys()
    lstDate.sort()
    for Date in lstDate:
        for pair in DateLien[Date]:
            if (pair[0], pair[1]) in Pondere.keys():
                Pondere[(Date, pair[0], pair[1])] +=1
            else:
                if pair[0] != pair[1]:
                    Pondere[(Date, pair[0], pair[1])] = 1
                    Prop[(pair[0], pair[1])] = (Date, pair[2])
                else:
                    reseau.remove(pair)
                
    for k in Pondere.keys():
        source = k[1] 
        target = k[2]
        try:
            G.add_edge(ListeNode.index(source), ListeNode.index(target), attr_dict = {'weight' : Pondere[k]})
        except:
            pass
    for ed in G.edges():
        if (ListeNode[ed[0]], ListeNode[ed[1]]) in Prop.keys():
            date = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][0]
            G.edge[ed[0]][ed[1]] ['rel'] = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]
            #G.edge[ed[0]][ed[1]] ['time'] = [(1, date.isoformat(), today)] #version simple
            #number = len([u for u in Prop.keys() if u[0] == ListeNode[ed[0]] and u[1] == ListeNode[ed[1]] and Prop[(date, ListeNode[ed[0]], ListeNode[ed[1]])][0] <= date])
            liste = [u for u in Prop.keys() if u[0] == ListeNode[ed[0]] and u[1] == ListeNode[ed[1]]]
            lienExist = [u for u in liste if Prop[u][0] <= date]
           
            G.edge[ed[0]][ed[1]] ['time'] = [(len(lienExist), date.isoformat(), today)] #version simple          
            G.edge[ed[0]][ed[1]] ['deb'] = date.isoformat()
            G.edge[ed[0]][ed[1]] ['fin'] = today
#            # setting time weight attribute for each node           
#            #defining existing dates before current edge date
#            datesExists =[u for u in lstDate if u<date]
#            # retreiving node apparition in edges before current date
#            lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[0]] or u[1] == ListeNode[ed[0]] and Prop[u][0] in datesExists]
#            
#            #counting those relative to same kind of relation
#            numAppear = len([u for u in lstAppear if Prop[u][1] == Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]]) +1 #adding 1 for current occur
#            #should be divided by number of relation types in the network ????? 
#            # and how compute it here... 
#            #setting node time attribute 
#            if not G.node[ed[0]].has_key('time'):#source
#                G.node[ed[0]]['time'] = [(numAppear, date.isoformat(), today)]
#            else:
#                if (numAppear,  date.isoformat(), today) not in G.node[ed[0]]['time']:
#                    G.node[ed[0]]['time'].append((numAppear,  date.isoformat(), today))
#            #same process for target node
#            lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[1]] or u[1] == ListeNode[ed[1]] and Prop[u][0] in datesExists]
#            
#            #counting those relative to same king of relation
#            numAppear = len([u for u in lstAppear if Prop[u][1] == Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]])+1 #adding 1 for current occur
##           #setting node time attribute 
#            if not G.node[ed[1]].has_key('time'):#source
#                G.node[ed[1]]['time'] = [(numAppear, date.isoformat(), today)]
#            else:
#                if (numAppear, date.isoformat(), today) not in G.node[ed[1]]['time']:
#                    G.node[ed[1]]['time'].append((numAppear,  date.isoformat(), today))
        else:
            print "this should not append"
        datesExists = [u for u in lstDate if u < datetime.date.today()]
        lstAppear = [u for u in Prop.keys() if u[0] == ListeNode[ed[0]] or u[1] == ListeNode[ed[0]] and Prop[u][0] in datesExists]
        G.edge[ed[0]][ed[1]]['NormedWeight'] = float(G.edge[ed[0]][ed[1]]['weight']*100) / len(lstAppear)
    
            # updating datetime, endate is the next startdate
#            listDate = []
#            for entry in G.node[ed[0]]['time']:
#                listDate.append(entry[1])
#            if len(listDate) > 1:
#                listDate.sort()
#                tempoRes = []
#                for i in G.node[ed[0]]['time']:
#                    ind = listDate.index(i[1])
#                    if ind + 1 in range(len(listDate)):
#                        tempo = (i[0], i[1], listDate[ind + 1]) #end time is set to next one
#                    else:
#                        tempo = (i[0], i[1], today)
#                    tempoRes.append(tempo)
#                G.node[ed[0]]['time'] = tempoRes
                   
    return G, reseau, Prop


def genereAppariementSimple(lstBrev, prop1, prop2):
    """sur la liste des brevets, génère et renvoie la liste des appariements 
    brev[prop1];brev[prop2]\n 
    dans une liste de tuples sans données sur les arcs"""
    res = []
    if lstBrev is not None:
        if prop1 in lstBrev[0].keys():
            if prop2 in lstBrev[0].keys():
                for Brev in lstBrev:
                    if Brev[prop1] is not None and Brev[prop2] is not None:
                        if type(Brev[prop1]) == type(u"") and type(Brev[prop2]) == type(u""):
                            temp = (str(Formate(Brev[prop1])), str(Formate(Brev[prop2])))
                            res.append(temp)
                        elif type(Brev[prop1]) == type([]) and type(Brev[prop2]) == type(u""):
                            for prop in Brev[prop1]:
                                temp = (str(Formate(prop)), str(Formate(Brev[prop2])))
                                res.append(temp)
                        elif type(Brev[prop1]) == type(u"") and type(Brev[prop2]) == type([]):
                            for prop in Brev[prop2]:
                                temp = (str(Formate(Brev[prop1])), str(Formate(prop)))
                                res.append(temp)
                        else:
                            for pro1 in Brev[prop1]:
                                for pro2 in Brev[prop2]:
                                    temp=(str(Formate(pro1)), str(Formate(pro2)))
                                    res.append(temp) 
                return res
    else:
        return None
        
def Remplace(ListeBrev, prop, truc2, truc):
    """Remplace dans la liste des brevets pour la propriete "prop"
    le truc par le truc2.
    puis renvoie la listedes brevets modifée"""
    for brev in ListeBrev:
        if brev[prop] is not None:
            if type(brev[prop]) == type(''):
                if brev[prop] == truc:
                    brev[prop] = truc2.replace(u'\u2002', '')
            else:
                tempo =[]
                for k in brev[prop]:
                    if k == truc:
                        tempo.append(truc2.replace(u'\u2002', ''))
                    else:
                        tempo.append(k)
                brev[prop] = tempo
    return ListeBrev
    
def NettoieProprietes(LstBrev, prop):
    """détecte dans la liste des brevets pour la propriété prop en minimalisant la 
    chaine associée à la propriété par la chaine la plus petite inclue dans l'ensemble des chaines
    ex: si LstBrev[0][prop] = 'son nom à lui [fr]' et LstBrev[4][prop] = 'son nom à lui'
        alors LstBrev[0][prop] = 'son nom à lui' 
        """
    TrucANettoyer = []
    for brev in LstBrev:
        if brev[prop] is not None:
            if type(brev[prop]) == type(''):
                TrucANettoyer.append(brev[prop].replace(u'\u2002', ''))
            else:
                for k in brev[prop]:
                    TrucANettoyer.append(k.replace(u'\u2002', ''))
    for truc in TrucANettoyer:
        for truc2 in set(TrucANettoyer).difference(truc):
            if truc.count(truc2) > 0 and truc != truc2:
                if len(truc2) < len(truc):
                    LstBrev = Remplace(LstBrev, prop, truc2, truc)
                    
                    
    return LstBrev

def NettoiePays(ListeBrevet):
    """supprime les info entre [] si elles sont redondantes avec le contenu de 
Brevet['pays']"""
    lstCles = set(ListeBrevet[0].keys()).difference(set(['pays', 'date']))
    lstRes = []
    for brevet in ListeBrevet:
        for cle in lstCles:
            if cle is not 'date' and brevet[cle] is not None and brevet['pays'] is not None:
                if brevet[cle].count(brevet['pays'])>0:
                    brevet[cle]=brevet[cle].replace(brevet['pays'], "", brevet[cle].count('['))
                brevet['pays'] = brevet['pays'].replace('[','')
                brevet['pays'] = brevet['pays'].replace(']','')        
        lstRes.append(brevet)
    
    return lstRes

def GenereListe(ListeBrevet, prop, date = False):
    """renvoie la liste des données associées à la propriété pour la liste de dictionnaires"
    """
    res = []
    if date: #dynamic net case
        for brev in ListeBrevet:
            if type(brev[prop]) == type([]):
                for k in brev[prop]:
                    if [k, brev['date'].year] not in res:
                        res.append([k, brev['date'].year])
            elif [brev[prop], brev['date'].year] not in res:
                res.append([brev[prop], brev['date'].year])
        
    else:
        for brev in ListeBrevet:
            if type(brev[prop]) == type([]):
                for k in brev[prop]:
                    if [k, ''] not in res:
                        res.append([k, ''])
            elif [brev[prop], ''] not in res:
                res.append([brev[prop], ''])
    #res = set([u for u in res])   
    return res

def GenereListeSansDate(ListeBrevet, prop):
    """renvoie la liste des données associées à la propriété pour la liste de dictionnaires"
    """
    res = []
    
    for brev in ListeBrevet:
            if type(brev[prop]) == type([]):
                for k in brev[prop]:
                    if k not in res:
                        res.append(k)
            elif brev[prop] not in res:
                res.append(brev[prop])
    #res = set([u for u in res])   
    return res


def change(NomDeNoeud):
    if NomDeNoeud == 'classification':
        return 'IPCR'
    if NomDeNoeud == 'pays':
        return 'country'
    if NomDeNoeud == 'inventeur':
        return 'inventor'
    return NomDeNoeud
    
    
def genereAppariement(lstBrev, prop1, prop2, sep, couleur = "grey" , label = ''):
    """sur la liste des brevets, génère et renvoie la liste des appariements 
    brev[prop1];brev[prop2]\n
    dans une chaine de caractères"""
    res = ""
    if lstBrev is not None:
        if prop1 in lstBrev[0].keys():
            if prop2 in lstBrev[0].keys():
                for Brev in lstBrev:
                    if Brev[prop1] is not None and Brev[prop2] is not None:
                        if type(Brev[prop1]) == type(u"") and type(Brev[prop2]) == type(u""):
                            res += "(\'" + Formate(Brev[prop1]) +"\'" +sep + "\'" +Formate(Brev[prop2]) + "\'" +sep + "{ 'color' : "+ couleur+"','label':'"+label+"'})\n"
                        elif type(Brev[prop1]) == type([]) and type(Brev[prop2]) == type(u""):
                            for prop in Brev[prop1]:
                                res +=  "(\'" +Formate(prop) +"\'" + sep +"\'" + Formate(Brev[prop2]) + "\'" +sep +"{'color':'"+ couleur+"','label':'"+label+"'})\n"
                        elif type(Brev[prop1]) == type(u"") and type(Brev[prop2]) == type([]):
                            for prop in Brev[prop2]:
                                res +=  "(\'" +Formate(Brev[prop1]) + "\'" +sep + "\'" +Formate(prop) +"\'" + sep + "{'color':'"+ couleur +"','label':'"+label+"'})\n"
                        else:
                            for pro1 in Brev[prop1]:
                                for pro2 in Brev[prop2]:
                                    res+= "(\'" +  Formate(pro1) + "\'" +sep +"\'" + Formate(pro2) + "\'" +sep + "{'color':'"+ couleur+"','label':'"+label+ "'})\n" 
                return res
    else:
        return None

def ExtraitMinDate(noeud):
        if noeud.has_key('time'):
            for i in noeud['time']:
                mini = 3000
                if i[1] < mini:
                    mini = i[1]
        else:
            mini = dateDujour
        return mini
    
    
def getClassif(noeud, listeBrevet):
        for Brev in listeBrevet:
            if Brev['label'] == noeud:
                return Brev['classification']
        return 'NA'
    
def quote(string):
    import urllib
    string=string.replace(u'\x80', '')
    string=string.replace(u'\x82', '')

    return urllib.quote(string.replace(u'\u2002', ''), safe='/\\())')



#############
# tests unitaires
##################
#print ExtractClassification('C10B 01/123')

#DureeBrevet = 20
#SchemeVersion = '20140101'
#
#ListeBrevet = []
#import datetime, os
#today = datetime.datetime.now().date().isoformat()
#dateMini = today
#dateMax = datetime.datetime(1700, 1, 1).isoformat()
#import networkx as nx
#G = nx.DiGraph()
#ResultPath = 'BiblioPatents'
#ResultPathGephi = 'GephiFiles'
#
#Brev = dict()
#
#Brev ["pays"] = u"fr"
#Brev["inventor"] = [u"Me", u"My colleague"]
#Brev["applicant"]= [u'Universite de Toulon']
#Brev["classification"] = u'C101/24A1'
#Brev ["label"] = u'3209934'
#Brev ["date"] = datetime.date(2014,01, 01)
#
#
#if type(Brev['classification']) == type ([]):
#            temp = dict()
#            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
#                temp[key] = []
#            for classif in Brev['classification']:
#                temp['classification'].append(classif.replace(' ', '', classif.count(' ')))
#                temp['IPCR1'].append(classif[0])
#                if len(classif) > 2:
#                    temp['IPCR3'].append(unicode(classif[0:2]))
#                else:
#                    temp['IPCR3'].append('')
#                if len(classif) > 4:
#                    temp['IPCR4'].append(unicode(classif[0:3]))
#                else:
#                    temp['IPCR4'].append('')
#                if classif.count('/') > 0:
#                    temp['IPCR7'].append(unicode(classif.split('/')[0]))
#                else:
#                    temp['IPCR7'].append('')
#                temp['IPCR11'].append(unicode(classif[0:len(classif)-2]))
#                
#                temp['status'].append(unicode(classif[len(classif)-1]))
#                if temp['status'] not in Status:
#                     temp['status']=unicode(classif[len(Brev['classification'])-2])
#                     if temp['status'] not in Status:
#                         temp['status'] = 'N/A'
#            for key in ['classification', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:    
#                if type(temp[key]) == type([]):
#                    Brev[key] = list(set(temp[key]))
#                else:
#                    Brev[key] = temp[key]
#                    
#elif Brev['classification'] is not None:
#            Brev['classification'] = Brev['classification'].replace(' ', '', Brev['classification'].count(' '))
#                        
#            Brev['IPCR1']=(Brev['classification'][0])
#            if len(Brev['classification']) > 2:
#                Brev['IPCR3']=(Brev['classification'][0:3])
#            else:
#                Brev['IPCR3'] = ''
#            if len(Brev['classification']) > 4:            
#                Brev['IPCR4']=(Brev['classification'][0:4])
#            else:
#                Brev['IPCR4'] = ''
#            if Brev['classification'].count('/') >0:
#                Brev['IPCR7']=(Brev['classification'].split('/')[0])
#            else:
#                Brev['IPCR7'] = ''
#            Brev['IPCR11']=(Brev['classification'][0:len(Brev['classification'])-2])
#            Brev['status']=(Brev['classification'][len(Brev['classification'])-1:])
#            if Brev['status'] not in Status:
#                 Brev['status']=(Brev['classification'][len(Brev['classification'])-2])
#                 if Brev['status'] not in Status:
#                     Brev['status'] = 'N/A'
#                     
#else:
#            for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
#                Brev[ipc] = 'N/A'
#
#ListeBrevet.append(Brev)
#print 
#Pays = set([(u) for u in GenereListeSansDate(ListeBrevet, 'pays')])
#Inventeurs = set([(u) for u in GenereListeSansDate(ListeBrevet, 'inventor')])
#LabelBrevet = set([(u) for u in GenereListeSansDate(ListeBrevet, 'label')])
#Applicant = set([(u) for u in GenereListeSansDate(ListeBrevet, 'applicant')])
#Classification = set([(u) for u in GenereListeSansDate(ListeBrevet, 'classification')])
#IPCR1 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR1')])
#IPCR3 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR3')])
#IPCR4 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR4')])
#IPCR7 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR7')])
#IPCR11 = set([(u) for u in GenereListeSansDate(ListeBrevet, 'IPCR11')])
#status = set([(u) for u in GenereListeSansDate(ListeBrevet, 'status')])
#listelistes = []
#listelistes.append(list(Pays))
#listelistes.append(list(Inventeurs))
#listelistes.append(list(LabelBrevet))
#listelistes.append(list(Applicant))
#listelistes.append(Classification)
#listelistes.append(list(IPCR1))
#listelistes.append(list(IPCR3))
#listelistes.append(list(IPCR4))
#listelistes.append(list(IPCR7))
#listelistes.append(list(IPCR11))
#listelistes.append(list(status))
#
#ListeNoeuds =[]
#for liste in listelistes:
#        ListeNoeuds += [u for u in liste if u not in ListeNoeuds]
#try:
#    ListeNoeuds.remove('N/A')
#except:
#    pass
#    
# 
#    
#appariement = dict()
#print listelistes
#lstCrit= ['inventor', 'label', 'applicant', 'pays', 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']
#for i in lstCrit:
#        for j in lstCrit:
#            
#            appariement[change(i)+'-'+change(j)] = [i,j]
#            
#for Brev in ListeBrevet:
#        if 'date' not in Brev.keys():
#            print Brev
#            Brev['date'] = datetime.date(3000, 1, 1)
#            
#G, reseau = GenereReseaux3(G, ListeNoeuds, ListeBrevet, appariement, True)
#
#DateNoeud = dict()
#for lien in reseau:
#        n1, n2, dat, pipo = lien
#        if DateNoeud.has_key(n1):
#            DateNoeud[n1].append(dat)
#        else:
#            DateNoeud[n1] = [dat]
#        if DateNoeud.has_key(n2):
#            DateNoeud[n2].append(dat)
#        else:
#            DateNoeud[n2] = [dat]
#            
#print
#attr = dict()
#liendureseau = [(u, v) for u,v,b ,z in reseau]
#LinkedNodes = []
#for k in liendureseau:
#    LinkedNodes.append(k[0])
#    LinkedNodes.append(k[1])
#    
#for noeud in ListeNoeuds:
#
#    if noeud is not None:
#        if noeud in Pays:
#            attr['label'] = 'pays'
#            attr['url'] = ''
##            elif noeud in Classification:
##                attr['label'] = 'IPCR'
##                if noeud.count('/') > 0:
##                    ind = noeud[4:].index('/')
##                    mask = 4 - ind
##                    mask2 = len(noeud[5+ind:len(noeud)-2])
##                
##                    attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]+str(0)*mask+noeud[4:4+ind]+noeud[5+ind:len(noeud)-2]+'000' + (3-mask2)*str('0')
##                else:
##                    attr['url'] = "http://web2.wipo.int/ipcpub#lang=fr&menulang=FR&refresh=symbol&notion=scheme&version=20140101&symbol="+noeud[0:4]
#        elif noeud in Inventeurs:
#            
#            attr['label'] = 'Inventeur'
#            attr['url'] ='http://worldwide.espacenet.com/searchResults?compact=false&ST=advanced&IN='+quote(noeud)+'&locale=en_EP&DB=EPODOC'
#            #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=IN:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=38&viewOption=All'
#        elif noeud in LabelBrevet:
#            attr['label'] = 'Brevet'
#            attr['Class'] = getClassif(noeud, ListeBrevet)
#            if attr['Class'] is not None:
#                attr['ReductedClass'] = getClassif(noeud, ListeBrevet)[0:4]
#                tempotemp = "http://worldwide.espacenet.com/searchResults?compact=false&ST=singleline&query="+noeud+"&locale=en_EP&DB=EPODOC"
#            
#                attr['url'] = tempotemp
#            else:
#                attr['ReductedClass'] = ""
#        elif noeud in Applicant:
#            attr['label'] = 'Applicant'
#            attr['url'] ='http://worldwide.espacenet.com/searchResuldengue-grupos.jsonts?compact=false&ST=advanced&locale=en_EP&DB=EPODOC&PA='+quote(noeud)
#            #attr['url'] = 'http://patentscope.wipo.int/search/en/result.jsf?currentNavigationRow=2&prevCurrentNavigationRow=1&query=PA:'+quote(noeud)+'&office=&sortOption=Pub%20Date%20Desc&prevFilter=&maxRec=123897&viewOption=All'
#        elif noeud in IPCR1:
#            if noeud in IPCRCodes.keys():
#                attr['label'] = 'IPCR1'
#                attr['name'] = IPCRCodes[noeud]
#                attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#            else:
#                pass #node is may be a status node
#        elif noeud in IPCR7:
#            attr['label'] = 'IPCR7'
#            attr['url'] =  'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#    
#        elif noeud in IPCR3:
#            attr['label'] = 'IPCR3'
#            attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#        elif noeud in IPCR4:
#            attr['label'] = 'IPCR4'
#            attr['url'] = 'http://web2.wipo.int/ipcpub#lang=enfr&menulang=FR&refresh=page&notion=scheme&version='+SchemeVersion+'&symbol=' +noeud
#
#        elif noeud in IPCR11:
#            attr['label'] = 'IPCR11'
#            attr['url'] = ''
#        elif noeud in status:
#            attr['label'] = 'status'
#            
#        if noeud in ListeNoeuds:
#            G.add_node(ListeNoeuds.index(noeud))
#
#            G.node[ListeNoeuds.index(noeud)]['label'] = noeud
#            
#            G.node[ListeNoeuds.index(noeud)]['category'] = attr['label']
#            G.node[ListeNoeuds.index(noeud)]['url'] = attr['url']
#            G.node[ListeNoeuds.index(noeud)]['weight'] = LinkedNodes.count(noeud)
#            G.node[ListeNoeuds.index(noeud)]['start'] = min(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
#            G.node[ListeNoeuds.index(noeud)]['end'] = max(DateNoeud[G.node[ListeNoeuds.index(noeud)]['label']]).isoformat()
#            if dateMini > G.node[ListeNoeuds.index(noeud)]['start']:
#                dateMini = G.node[ListeNoeuds.index(noeud)]['start']
#            if dateMax < G.node[ListeNoeuds.index(noeud)]['end']:
#                dateMax = G.node[ListeNoeuds.index(noeud)]['end']
#            
#            if len(G.node[ListeNoeuds.index(noeud)]['time']) >1:
#                lst = [u[1] for u in G.node[ListeNoeuds.index(noeud)]['time']]
#                lst.sort()
#                lsttemp = []
#                cpt=0
#                for kk in range(len(lst)):
#                    for nb in range(len(G.node[ListeNoeuds.index(noeud)]['time'])):                 
#                        if G.node[ListeNoeuds.index(noeud)]['time'][nb][1] == lst[kk]:
#                            if G.node[ListeNoeuds.index(noeud)]['time'][nb] not in lsttemp:
#                                if cpt>0:
#                                    
#                                    lsttemp[cpt-1] = (lsttemp[cpt-1][0], lsttemp[cpt-1][1], G.node[ListeNoeuds.index(noeud)]['time'][nb][1] )#enddate is startdate of current datetime
#                                lsttemp.append(G.node[ListeNoeuds.index(noeud)]['time'][nb])
#                                cpt+=1
#                G.node[ListeNoeuds.index(noeud)]['time'] = lsttemp         
#            G.node[ListeNoeuds.index(noeud)]['deb'] = G.node[ListeNoeuds.index(noeud)]['start']
#            G.node[ListeNoeuds.index(noeud)]['fin']= dateMax#G.node[ListeNoeuds.index(noeud)]['end']
#            G.node[ListeNoeuds.index(noeud)]['val'] = sum([u[0] for u in G.node[ListeNoeuds.index(noeud)]['time']])
#            del(G.node[ListeNoeuds.index(noeud)]['end'])
#            del(G.node[ListeNoeuds.index(noeud)]['start'])
#            del(G.node[ListeNoeuds.index(noeud)]['weight'])               
#            if noeud not in IPCR1:
#                pass
#            else:
#                G.node[ListeNoeuds.index(noeud)]['label'] = noeud + '-' +attr['name']
#        else:
#            print "on devrait pas être là, never", noeud
#            #G.node[ListeNoeuds.index(noeud)]['end'] = ExtraitMinDate(G.node[ListeNoeuds.index(noeud)]) + DureeBrevet
#            #G.node[ListeNoeuds.index(noeud)]['start'] = 
#        G.graph['defaultedgetype'] = "directed"
#        G.graph['timeformat'] = "date"
#        G.graph['mode'] = "dynamic"
#        G.graph['start'] = dateMini
#        G.graph['end'] = dateMax
#
#
#ndf = 'test'
#nx.write_gexf(G, ResultPathGephi+'\\'+ndf + ".gexf", version='1.2draft')
#fic = open(ResultPathGephi+'\\'+ndf+'.gexf', 'r')
##
## Next is a hack to correct the bad writing of the header of the gexf file
## with dynamics properties
#fictemp=open(ResultPathGephi+'\\'+"Good"+ndf+'.gexf', 'w')
#fictemp.write("""<?xml version="1.0" encoding="utf-8"?><gexf version="1.2" xmlns="http://www.gexf.net/1.2draft" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3.org/2001/XMLSchema-instance">
#  <graph defaultedgetype="directed" mode="dynamic" timeformat="date">
#<attributes class="edge" mode="static">
#  <attribute id="6" title="deb" type="string" />
#  <attribute id="7" title="fin" type="string" />
#  <attribute id="8" title="rel" type="string" />
#	</attributes>
#	<attributes class="edge" mode="dynamic">
#  <attribute id="9" title="time" type="integer" />
#</attributes>
#<attributes class="node" mode="static">
#  <attribute id="0" title="category" type="string" />
#  <attribute id="1" title="val" type="integer" />
#  <attribute id="3" title="url" type="string" />
#  <attribute id="4" title="deb" type="string" />
#  <attribute id="5" title="fin" type="string" />
#</attributes>
#	<attributes class="node" mode="dynamic">
#		<attribute id="2" title="time" type="integer" />
#	</attributes>
#""")
#ecrit  =False
#for lig in fic.readlines():
#    if lig.count('<nodes>'):
#        ecrit = True
#    if ecrit:
#        fictemp.write(lig)
#fictemp.close()
#fic.close()
#os.remove(ResultPathGephi+'\\'+ndf+'.gexf')
#
#os.rename(ResultPathGephi+'\\'+"Good"+ndf+'.gexf', ResultPathGephi+'\\'+ndf+'.gexf')
#print "Network file writen in ",  ResultPathGephi+' directory.\n See file: '+ndf + ".gexf"