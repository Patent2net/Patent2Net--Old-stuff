# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 08:50:16 2014

@author: dreymond
"""

def Formate(chaine):
    """formatte la chaine pour que ce soit un noeud correct pour Gephi et autres outils :
        notation hongroise (ou bulgare :-) : CeciEstUnePhrase"""
    #mem = chaine
    chaine = chaine.lower()
    chaine = chaine.title()
    chaine = chaine.replace(' ', '', chaine.count(' '))
    chaine = chaine.replace(u'\u2002', '', chaine.count(u'\u2002'))
#    table[chaine] = mem    
    return chaine
 
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
    for pair in reseau:
            if (pair[0], pair[1]) in Pondere.keys():
                Pondere[(pair[0], pair[1])] +=1
            else:
                if pair[0] != pair[1]:
                    Pondere[(pair[0], pair[1])] = 1
                    Prop[(pair[0], pair[1])] = (pair[2] , pair[3])
                else:
                    reseau.remove(pair)
                
 
    for k in Pondere.keys():
        source = k[0] 
        target = k[1]
        try:
            G.add_edge(ListeNode.index(source), ListeNode.index(target), attr_dict = {'weight' : Pondere[k]})
        except:
            pass
    for ed in G.edges():
        if (ListeNode[ed[0]], ListeNode[ed[1]]) in Prop.keys():
            date = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][0]
            G.edge[ed[0]][ed[1]] ['rel'] = Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][1]
            G.edge[ed[0]][ed[1]] ['time'] = [(1, date.isoformat(), today)] #version simple
            G.edge[ed[0]][ed[1]] ['deb'] = date.isoformat()
            G.edge[ed[0]][ed[1]] ['fin'] = today
            
            if not G.node[ed[0]].has_key('time'):
                G.node[ed[0]]['time'] = [(1, date.isoformat(), today)]
            else:
                match = False
                for Couple in  G.node[ed[0]]['time']:
                    maxi = 0 # on cherche la valeur max du lien
                    if maxi < Couple[0]:
                        maxi = Couple[0]
                    if Couple[1] == date.isoformat() and Couple[2] == today:
                        match = True
                        ind = G.node[ed[0]]['time'].index(Couple)
                        nb = Couple[0]
                if match:
                    #G.node[ed[0]]['time'].append((maxi +1, float(Prop[(ListeNode[ed[0]], ListeNode[ed[1]])][0].year), float(2014)))
                    G.node[ed[0]]['time'][ind] = ( nb +1, date.isoformat(), today)
                        
                else:
                    G.node[ed[0]]['time'].append((1, date.isoformat(), today))
        else:          
            if not G.node[ed[1]].has_key('time'):            
                G.node[ed[1]]['time'] = [(1, date.isoformat(), today)]
            else:
                match = False
                for Couple in  G.node[ed[1]]['time']:
                    maxi = 0 # on cherche la valeur max du lien
                    if maxi < Couple[0]:
                        maxi = Couple[0]
                    if Couple[1] == date.isoformat() and Couple[2] == today:
                        match = True
                        ind = G.node[ed[1]]['time'].index(Couple)
                        nb = Couple[0]
                if match:
                    G.node[ed[1]]['time'][ind] = (nb+1, date.isoformat(), today)
                else:
                    G.node[ed[1]]['time'].append((1, date.isoformat(), today))
            
            
    return G, reseau


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




