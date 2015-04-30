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

import re, Ops3

def isMaj(car):
    if car.lower() != car:
        return True
    else:
        return False

def ReturnBoolean(string):
    if string.count('True')>0 or string.count('true')>0:
        return True # to gather contents
    else:
        return False

def CleanPatent(dico):
    lstCle=dico.keys()
    res = dict()
    for cle in lstCle:
        if isinstance(dico[cle], list):
            if len(dico[cle])==1:
                if isinstance(dico[cle][0], list):
                    if len(dico[cle][0]) >1:
                        res[cle] = dico[cle][0]
                    else:
                        res[cle] = dico[cle][0][0]
                else:
                    res[cle] = dico[cle][0]
            elif len(dico[cle])>1:
                res[cle] = dico[cle] #print "hum"
            else:
                res[cle] = ''
        elif dico[cle] =='N/A':
            res[cle] = ''
        else:
            res[cle] = dico[cle]
    
    return res
def Decoupe(dico):
    """will return a list of dictionnary patents monovaluated as long as the product of multivalued entries"""
    Res = dict()
    remp  = dict()
    lstCle = dico.keys()
    for cle in lstCle:
        if isinstance(dico[cle], list):
            temp = [k for k in dico[cle] if k != 'N/A' and k != None and k!='']
            if len(temp) ==1:
                if isinstance(temp[0], list) and len(temp[0])>1:
                    remp[cle] = temp[0]
                else:
                    pass
            if len(temp) ==0:
                pass
            else:
                remp[cle] = temp
        else:
            pass
    i=1
    #calculating combinatory results. Each list multiplies others...
    nombre = prod([i*len(remp[cle]) for cle in remp.keys() if isinstance(remp[cle], list)  and len(remp[cle])!=0])
    #preparing result dictionnary    
    for num in range(nombre):
        Res[num] = dict()
        for cle in lstCle:   
            if cle not in remp.keys():  # unique content, not list for these keys
                Res[num][cle] = dico[cle]
    # for keys that dico[keys] are lists
    for cle2 in remp.keys():    
        cpt=0
        for content in remp[cle2]* (nombre /len(remp[cle2])):
            #for each content, write it this entry
            Res[cpt][cle2] = content
            #copy also others content for each content from different key 
            #for this entry (cpt)
            for cle3 in remp.keys():
                if cle3 != cle2:      
                    for content2 in remp[cle3]:
                        Res[cpt][cle3] = content2
            #next entry # this should stop at en end of resultset
            cpt+=1
    
#            elif len(remp[cle])>0:         
#                Res[num][cle] = remp[cle][num % len(remp[cle])]
#            else:
#                Res[num][cle] = dico[cle]
#    retour=[]
#    for k in Res.keys():
#        if Res[k] not in retour:
#            retour.append(Res[k]) 
        
    return Res
    
def SeparateCountryField(pat):
    PaysInv= [] #new field
    PaysApp = []
    brev = pat
    if not isinstance(pat, dict):
        print "pas gloup"
    if brev['inventeur'] is not None:
        
        if isinstance(brev['inventeur'], list):
            tempoInv = []
            for inv in brev['inventeur']:
                tempPaysInv = inv.split('[')
                if isinstance(tempPaysInv, list):
                    for kk in range(1, len(tempPaysInv), 2):
                        PaysInv.append(tempPaysInv[kk].replace(']',''))
                    tempoInv.append(tempPaysInv[0].strip())
                else:
                    tempoInv.append(tempPaysInv.strip())
            brev["inventeur"] = tempoInv
                
        else:
            tempPaysInv = brev['inventeur'].split('[')
            if isinstance(tempPaysInv, list):
                for kk in range(1, len(tempPaysInv), 2):
                    PaysInv.append(tempPaysInv[kk].replace(']',''))
                brev["inventeur"] = tempPaysInv[0].strip()
            else:
                tempoInv.append(tempPaysInv.strip())
    if brev['applicant'] is not None:
        
        if isinstance(brev['applicant'], list):
            tempoApp = []
            for APP in brev['applicant']:
                tempPaysApp = APP.split('[')
                if isinstance(tempPaysApp, list):
                    for kk in range(1, len(tempPaysApp), 2):
                        PaysApp.append(tempPaysApp[kk].replace(']',''))
                    tempoApp.append(tempPaysApp[0].strip())
                else:
                    tempoApp.append(tempPaysApp.strip())
            brev["applicant"] = tempoApp
        else:

            tempPaysApp = brev['applicant'].split('[')
            if isinstance(tempPaysApp, list):
                for kk in range(1, len(tempPaysApp), 2):
                    PaysApp.append(tempPaysApp[kk].replace(']',''))
                brev["applicant"] = tempPaysApp[0].strip()
            else:
                brev["applicant"] = tempPaysApp.strip()
    brev["Inventor-Country"] = list(set(PaysInv))
    brev["Applicant-Country"] = list(set(PaysApp))
    if len(brev["Inventor-Country"]) == 1:
            brev["Inventor-Country"] = brev["Inventor-Country"][0]
    if len(brev["Applicant-Country"]) == 1:
        brev["Applicant-Country"] = brev["Applicant-Country"][0]
    if isinstance(brev["Inventor-Country"], list) and len(brev["Inventor-Country"]) == 0:
        brev["Inventor-Country"] = ""
    if isinstance(brev["Applicant-Country"], list) and len(brev["Applicant-Country"]) == 0: 
        brev["Applicant-Country"] = ""
    return brev    

def CleanDate(lst):
    Res = []
    import dateutil.parser
    for tple in lst:
        deb = dateutil.parser.parse(tple[1])
        fin = dateutil.parser.parse(tple[2])
        if deb < fin:
            Res.append(tple)
        else:
            pass #avoiding unconsitents entries 
    return Res
def CleanPatentOthers(brev):
    tempo = dict()
    import bs4
    for cle in brev.keys():
        if brev[cle] is not None and brev[cle] != 'N/A' and brev[cle] != 'UNKNOWN':
            if isinstance(brev[cle], list):
                if cle == 'classification':
                    for classif in brev['classification']:
                        tempoClass = ExtractClassificationSimple2(classif)
                        for cle2 in tempoClass.keys():
                            if cle2 == 'classification':
                                if tempo.has_key(cle2) and not isinstance(tempo[cle2], list) and tempoClass[cle2] != tempo[cle]:
                                    tempo[cle2] = [tempo[cle2]]
                                    tempo[cle2].append(tempoClass[cle2])
                                elif tempo.has_key(cle2) and isinstance(tempo[cle2], list) and tempoClass[cle2] not in tempo[cle]:
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    tempo[cle2] = [tempoClass[cle2]]
                            elif cle2 in tempo.keys():
                                if tempoClass[cle2] not in tempo[cle2]:
                                    #tempo[cle] = []
                                    tempo[cle2].append(tempoClass[cle2])
                                else:
                                    pass
#                                if tempoClass[cle2] not in tempo2[cle2]:   
#                                    tempo2[cle2].append(tempoClass[cle2])
#                                else:
#                                    pass
                            else:
                                tempo[cle2] = []
#                                tempo[cle2].append(tempoClass[cle2])
#                                tempo2[cle2].append(tempoClass[cle2])

                else:                
                    temp = [unicode(a) for a in brev[cle]]
                    tempo[cle] = temp
                    
            elif cle =='titre':
                temp = unicode(brev[cle]).replace('[','').replace(']', '').lower().capitalize()
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp
                #tempo2 [cle] = temp
            elif cle =='date':
                try:
                    tempo[cle] = str(brev['date'].year) +'-' +  str(brev['date'].month) +'-' + str(brev['date'].day)
                except:
                    tempo[cle] = brev['date']
                #tempo2[cle] = str(brev['date'].year) # just the year in Pivottable
            elif cle =='classification' and brev['classification'] != u'':
                tempoClass = ExtractClassificationSimple2(brev['classification'])
                for cle in tempoClass.keys():
                    if cle in tempo.keys() and tempoClass[cle] not in tempo[cle]:
                        tempo[cle].append(tempoClass[cle])
                    else:
                        tempo[cle] = []
                        tempo[cle].append(tempoClass[cle])
            elif isinstance(brev[cle], dict):
                temp[cle] = brev[cle]
                            
            else:
                temp = unicode(brev[cle]).replace('[','').replace(']', '')
                soup = bs4.BeautifulSoup(temp)
                temp = soup.text
                tempo[cle] = temp

                
        else:
            tempo[cle] = ''
    
    return tempo

def prod(liste):
    Res = 1
    for k in liste:
        Res = Res * k
    return Res
    
def change(NomDeNoeud):
    if NomDeNoeud == 'classification':
        return 'IPCR'
    if NomDeNoeud == 'pays':
        return 'country'
    if NomDeNoeud == 'inventeur':
        return 'inventor'
    return NomDeNoeud

def symbole(IPC):
    if len(IPC) == 1:
        return IPC
    if len(IPC) == 3:
        return IPC
    if len(IPC) == 4:
        return IPC
    
    subclass = IPC[0:4]
    if IPC.count('/')>0:
        maingroup = IPC[4:].split('/')[0] 
        subgroup = IPC[4:].split('/')[1]
    elif len(IPC) ==14:
        maingroup = IPC[4:8]
        subgroup = IPC[8:]
    elif len(IPC) >4 and len(IPC)<14:
        maingroup = IPC[4:]
        subgroup = ''
    else:
        print "not good symbol", IPC
    
    maingroup = re.sub("^0+", "", maingroup)
    maingroup = (4-len(maingroup))*'0' + maingroup
    subgroup = subgroup + (6 - len(subgroup)) * '0'
    return subclass+maingroup+subgroup
        
def ExtraitMinDate(noeud):
    import datetime.date.today as auj
    if noeud.has_key('time'):
        for i in noeud['time']:
            mini = 3000
            if i[1] < mini:
                mini = i[1]
    else:
        mini = auj()
    return mini


def getClassif(noeud, listeBrevet):
    for Brev in listeBrevet:
        if Brev['label'] == noeud:
            return Brev['classification']
    return 'NA'

def ContractList(liste):
    
    res = []
    for Ens in liste:
        if isinstance(Ens, list):
            for u in Ens:
                if u not in res:
                    res.append(u)
        elif isinstance(Ens, unicode):
            if Ens not in res:
                res.append(Ens)
        else:
            return liste
    return res
    
def ExtractClassificationSimple(data):
    res = []
    if data is not None:
        if isinstance(data, list) and len(data) ==1:
            data = data[0]
        elif isinstance(data, list):
            print "paté"
        if type(data) == type ("") or type(data) == type (u""):
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
            
            
            res = Resultat
        else:
            print "should not be here, pb in classification content"
    else:
        print "should not be here, pb in classification content"
    return res
    
def ExtractClassificationSimple2(data):
    res = []
    if data is not None:
        if isinstance(data, list) and len(data) ==1:
            data = data[0]
        elif isinstance(data, list):
            print "paté" #assert isinstance(data, list)
        if type(data) == type ("") or type(data) == type (u""):
            Resultat = dict()
            
            data = data.replace(' ', '', data.count(' '))
            if data[len(data)-2].isalpha():#checking last two caracter some contains status data... 
                Resultat['IPCR11'] = data[0:len(data)-2]
            elif data[len(data)-1].isalpha():
                Resultat['IPCR11'] = data[0:len(data)-1]
            else:
                Resultat['IPCR11'] = data

           #Resultat['classification'] = Resultat['IPCR11']
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
            if Resultat['IPCR11'][len(Resultat['IPCR11'])-2:len(Resultat['IPCR11'])].count('0')>1:
                Resultat['IPCR11'] = 'N/A' # consistency check : if result endswith 0, means that is an IPCR7
            
            
            res = Resultat
        else:
            print "should not be here, pb in classification content"
    else:
        print "should not be here, pb in classification content"
    return res


def ExtractClassification2(data):
    #Brev['classification'] = data
    res = dict()
    if data is not None:
        if isinstance(data, list):
            data2 = []
            data2 = [u for u in data if u not in data2]
            data = data2
    if data is not None:
        if isinstance(data, list):
            for classif in data:
                if isinstance(classif, list):
                    for te in classif:
                        tempo = ExtractClassificationSimple2(te)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])

                else:
                    tempo = ExtractClassificationSimple2(classif)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])
        elif isinstance(data, unicode) or isinstance(data, str):
            tempo = ExtractClassificationSimple2(data)
            for cle in tempo.keys():
                    if res.has_key(cle):
                        if tempo[cle] not in res[cle]:
                            res[cle].append(tempo[cle])
                    else:
                        res[cle] = []
                        res[cle].append(tempo[cle])
        else:
            print "should not be here, pb in classification content"
    else:
        resultat = dict()
        for ipc in ['IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11']:
            resultat[ipc] = []
        res = resultat
#    if isinstance(res, list):
#        
#        resu = dict()
#        if isinstance(res[0], dict):
#            for cle in res[0].keys():
#                resu[cle] = []
#            for dic in res:
#                for cle in dic.keys():
#                    resu[cle].append(dic[cle])
#            for cle in resu.keys():
#                if isinstance(resu[cle], list):
#                    temp = []
#                    temp = [u for u in resu[cle] if u not in temp]
#                    resu[cle] = temp
#        else:
#            print "should nto be here"
##            if isinstance(res[0], list) and len(res[0]) == 1:
##                res[0] = res[0][0]
##                for cle in res[0].keys():
##                    resu[cle] = []
##                for dic in res:
##                    for cle in dic.keys():
##                        resu[cle].append(dic[cle])
##                for cle in resu.keys():
##                    if isinstance(resu[cle], list):
##                        temp = [u for u in resu[cle] if u not in temp]
##                        resu[cle] = temp

    return res


    
    
def ExtractClassification(data):
    #Brev['classification'] = data
    res = dict()
    if data is not None:
        if isinstance(data, list):
            data2 = []
            data2 = [u for u in data if u not in data2]
            data = data2
    if data is not None:
        if isinstance(data, list):
            for classif in data:
                if isinstance(classif, list):
                    for te in classif:
                        tempo = ExtractClassificationSimple(te)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])

                else:
                    tempo = ExtractClassificationSimple(classif)
                    for cle in tempo.keys():
                        if res.has_key(cle):
                            if tempo[cle] not in res[cle]:
                                res[cle].append(tempo[cle])
                        else:
                            res[cle] = []
                            res[cle].append(tempo[cle])
        elif isinstance(data, unicode) or isinstance(data, str):
            tempo = ExtractClassificationSimple(data)
            for cle in tempo.keys():
                    if res.has_key(cle):
                        if tempo[cle] not in res[cle]:
                            res[cle].append(tempo[cle])
                    else:
                        res[cle] = []
                        res[cle].append(tempo[cle])
        else:
            print "should not be here, pb in classification content"
    else:
        resultat = dict()
        for ipc in ["classification", 'IPCR1', 'IPCR3', 'IPCR4', 'IPCR7', 'IPCR11', 'status']:
            resultat[ipc] = []
        res = resultat
#    if isinstance(res, list):
#        
#        resu = dict()
#        if isinstance(res[0], dict):
#            for cle in res[0].keys():
#                resu[cle] = []
#            for dic in res:
#                for cle in dic.keys():
#                    resu[cle].append(dic[cle])
#            for cle in resu.keys():
#                if isinstance(resu[cle], list):
#                    temp = []
#                    temp = [u for u in resu[cle] if u not in temp]
#                    resu[cle] = temp
#        else:
#            print "should nto be here"
##            if isinstance(res[0], list) and len(res[0]) == 1:
##                res[0] = res[0][0]
##                for cle in res[0].keys():
##                    resu[cle] = []
##                for dic in res:
##                    for cle in dic.keys():
##                        resu[cle].append(dic[cle])
##                for cle in resu.keys():
##                    if isinstance(resu[cle], list):
##                        temp = [u for u in resu[cle] if u not in temp]
##                        resu[cle] = temp

    return res

def smart_colormap(vmin, vmax, color_high='#b11902', hue_low=0.6):
    import matplotlib.colors 
    import colorsys
    """
    Creates a "smart" colormap that is centered on zero, and accounts for
    asymmetrical vmin and vmax by matching saturation/value of high and low
    colors.

    It works by first creating a colormap from white to `color_high`.  Setting
    this color to the max(abs([vmin, vmax])), it then determines what the color
    of min(abs([vmin, vmax])) should be on that scale.  Then it shifts the
    color to the new hue `hue_low`, and finally creates a new colormap with the
    new hue-shifted as the low, `color_high` as the max, and centered on zero.

    :param color_high: a matplotlib color -- try "#b11902" for a nice red
    :param hue_low: float in [0, 1] -- try 0.6 for a nice blue
    :param vmin: lowest value in data you'll be plotting
    :param vmax: highest value in data you'll be plotting
    """
    # first go from white to color_high
    orig_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'test', ['#FFFFFF', color_high], N=2048)

    # For example, say vmin=-3 and vmax=9.  If vmin were positive, what would
    # its color be?
    vmin = float(vmin)
    vmax = float(vmax)
    mx = max([vmin, vmax])
    mn = min([vmin, vmax])
    frac = abs(mn / mx)
    rgb = orig_cmap(frac)[:-1]

    # Convert to HSV and shift the hue
    hsv = list(colorsys.rgb_to_hsv(*rgb))
    hsv[0] = hue_low
    new_rgb = colorsys.hsv_to_rgb(*hsv)
    new_hex = matplotlib.colors.rgb2hex(new_rgb)

    zeropoint = vmin / (vmax - vmin)

    # Create a new colormap using the new hue-shifted color as the low end
    new_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'test', [(0, new_hex), (zeropoint, '#FFFFFF'), (1, color_high)],
        N=2048)

    return new_cmap
    
def cmap_discretize(cmap, N):
   
    """Return a discrete colormap from the continuous colormap cmap.
    
        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.
    
    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """
    import matplotlib
    import numpy as np
    if type(cmap) == str:
        cmap = matplotlib.colors.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in xrange(N+1) ]
    # Return colormap object.

    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)

def FormateGephi(chaine):
    """formatte la chaine pour que ce soit un noeud correct pour Gephi et autres outils :
        notation hongroise (ou bulgare :-) : CeciEstUnePhrase."""
    #mem = chaine
    assert(isinstance(chaine, unicode))
    
    if chaine is not None:
        if type(chaine) == type([]):
            res = []
            for ch in chaine:
                temp = FormateGephi(ch)
                res.append(temp)
            return res
        else:
            chaine = chaine.title()
            chaine = chaine.replace(' ', '', chaine.count(' '))
            try:
                chaine = chaine.decode('latin1')
                chaine = chaine.encode('utf8')
                return chaine
            except:
                try:
                    chaine = chaine.decode('cp1252')
                    chaine = chaine.encode('utf8')
                    return chaine
                except:
                    #print "unicode problem in formate"
    #                print chaine
                    pass
            if chaine.count('[')>0:
                return chaine.split('[')[0]
            else:
                return chaine
    else:
        return u''
           
    
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
#        elif len(pays) >0:
#            if chaine.count(' '+pays) >0 or chaine.count('[pays]') >0:
#                temp = chaine.replace(pays, '')
#                if temp.count('[]') >0:
#                    temp = temp.replace('[]', '')
#                chaine = temp.strip()
#        chaine = chaine.lower()
#        chaine = chaine.encode('utf8')
#        chaine = chaine.title()
#        chaine = chaine.replace(' ', '', chaine.count(' '))
#        chaine = chaine.replace(u'\xe2\x80\x82', '', chaine.count(u'\xe2\x80\x82'))
#        chaine = chaine.replace(u'\xe2', '', chaine.count(u'\xe2'))
#        chaine = chaine.replace(u'\x80', '', chaine.count(u'\x80'))
#        chaine = chaine.replace(u'\x82', '', chaine.count(u'\x82'))
#        chaine = chaine.replace(u'\xe9', '', chaine.count(u'\xe9'))
#        chaine = chaine.replace(u'\xd6', '', chaine.count(u'\xd6'))
#        chaine = chaine.replace(u'\xd2', '', chaine.count(u'\xd2'))
#        chaine = chaine.replace(u'\xf6', '', chaine.count(u'\xf6'))
#        chaine = chaine.replace(u'\xfc', '', chaine.count(u'\xfc'))
#        chaine = chaine.replace(u'\u2002', '', chaine.count(u'\u2002'))
#        chaine = chaine.replace(u'\xe1', '', chaine.count(u'\xe1'))
#        chaine = chaine.replace(u'\xf3', '', chaine.count(u'\xf3'))
#        chaine = chaine.replace(u'\xed', '', chaine.count(u'\xed'))
#        chaine = chaine.replace(u'\xe4', '', chaine.count(u'\xe4'))
#        chaine = chaine.replace(u'\xe7', '', chaine.count(u'\xe7'))
#        chaine = chaine.replace(u'\xfa', '', chaine.count(u'\xfa'))
#        chaine = chaine.replace(u'\xf1', '', chaine.count(u'\xf1'))
        
        try:
            chaine = chaine.decode('latin1')
            chaine = chaine.encode('utf8')
            return chaine
        except:
            try:
                chaine = chaine.decode('cp1252')
                chaine = chaine.encode('utf8')
                return chaine
            except:
#                print "unicode problem in formate"
#                print chaine
                pass
        #chaine = quote(chaine)
    #    table[chaine] = mem    
#        import urllib
#        chaine = urllib.quote(chaine.replace(u'\u2002', ''), safe='[]')
        return unicode(chaine, 'utf8', 'ignore')
    else:
        return u''
        
def Formate2(chaine, pays):
    """Nettoie la chaine. 
        Vire le pays le cas échéant"""
    #mem = chaine
    if chaine is not None:
        chaine = chaine.lower()
        chaine = chaine.title()
        chaine = chaine.replace('  ', ' ', chaine.count('  '))
#        chaine = chaine.replace(u'\xe2\x80\x82', '', chaine.count(u'\xe2\x80\x82'))
#        chaine = chaine.replace(u'\xe2', '', chaine.count(u'\xe2'))
#        chaine = chaine.replace(u'\x80', '', chaine.count(u'\x80'))
#        chaine = chaine.replace(u'\x82', '', chaine.count(u'\x82'))
#        chaine = chaine.replace(u'\xe9', '', chaine.count(u'\xe9'))
#        chaine = chaine.replace(u'\xd6', '', chaine.count(u'\xd6'))
#        chaine = chaine.replace(u'\xfa', '', chaine.count(u'\xfa'))
#        chaine = chaine.replace(u'\xd2', '', chaine.count(u'\xd2'))
#        chaine = chaine.replace(u'\xf6', '', chaine.count(u'\xf6'))
#        chaine = chaine.replace(u'\xfc', '', chaine.count(u'\xfc'))
#        chaine = chaine.replace(u'\xe1', '', chaine.count(u'\xe1'))
#        chaine = chaine.replace(u'\xf3', '', chaine.count(u'\xf3'))
#        chaine = chaine.replace(u'\xed', '', chaine.count(u'\xed'))
#        chaine = chaine.replace(u'\xe7', '', chaine.count(u'\xe7'))
#        chaine = chaine.replace(u'\u2002', '', chaine.count(u'\u2002'))
#        chaine = chaine.replace('%20', ' ', chaine.count('%20'))
        #chaine = quote(chaine)
    #    table[chaine] = mem    
#        import urllib
        #chaine = urllib.quote(chaine.replace(u'\u2002', ''), safe='[]')
#        if chaine.count('['+pays+']')>0:
#            chaine = chaine.replace('['+pays+']', '')
#        if chaine.count('[') >0:
#            chaine = chaine.split('[')[0] 
        try:
            chaine = chaine.decode('latin1')
            chaine = chaine.encode('utf8')
        except:
            try:
                chaine = chaine.decode('cp1252')
                chaine = chaine.encode('utf8')
            except:
                pass
                #print "unicode problem"
            
        return chaine
    else:
        return u''



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
                                    try:
                                        temp = [Brev[p1], k, Brev['date']]
                                        res.append(temp)
                                    except:
                                        try:
                                            temp = [Brev[p1], unicode(k, 'cp1252', "replace"), Brev['date']]
                                            res.append(temp)
                                        except:
                                            try:
                                                temp = [Brev[p1], unicode(k, 'latin1', "replace"), Brev['date']]
                                                res.append(temp)
                                            except:
                                                try:
                                                    temp = [Brev[p1], unicode(k, 'utf8', "replace"), Brev['date']]
                                                    res.append(temp)
                                                except:
                                                    print "first unicode exception in genAppar"
                            elif type(Brev[p1]) == type([]) and type(Brev[p2]) == type(u""):
                                for k in Brev[p1]:
                                    try:
                                        temp = [k, Brev[p2], Brev['date']]
                                        res.append(temp)
                                    except:
                                        try:
                                            temp = [unicode(k, 'utf8', "replace"), Brev[p2], Brev['date']]
                                            res.append(temp)
                                        except:
                                            try:
                                                temp = [unicode(k, 'latin1', "replace"), Brev[p2], Brev['date']]
                                                res.append(temp)
                                            except:
                                                try:
                                                    temp = [unicode(k, 'cp1252', "replace"), Brev[p2], Brev['date']] 
                                                    res.append(temp)
                                                except:
                                                    print "unicode exception"
                                    
                            else:
                                for k1 in Brev[p1]:
                                    cpt = Brev[p1].index(k1)
                                    for i in range(cpt, len(Brev[p2])):
                                        #if k1 != Brev[p2][i]:
                                        try:
                                            temp = [k1, Brev[p2][i], Brev['date']]
                                            res.append(temp)
                                        except:  #cases of k1 is unicode and Brev not and vice et versa not TREATEN !!!
                                            try:
                                                temp = [unicode(k1, 'utf8', "replace"), unicode(Brev[p2][i], 'utf8', "replace"), Brev['date']]
                                                res.append(temp)
                                            except:
                                                try:
                                                    temp = [unicode(k1, 'latin1', "replace"), unicode(Brev[p2][i], 'latin1', "replace"), Brev['date']]
                                                    res.append(temp)
                                                except:
                                                    try:
                                                        temp = [unicode(k1, 'cp1252', "replace"), unicode(Brev[p2][i], 'cp1252', "replace"), Brev['date']]
                                                        res.append(temp)
                                                    except:
                                                        print "another unicode exception"

                                            
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

def MakePonderateAndProp(pair, Date, propo, pondere, destroy):
    
    if isinstance(pair[0], list):
        for u in pair[0]:
            propo, pondere, destroy = MakePonderateAndProp((u, pair[1], pair[2]), Date, propo, pondere, destroy)
    elif isinstance(pair[1], list):
        for u in pair[1]:
            propo, pondere, destroy = MakePonderateAndProp((pair[0], u, pair[2]), Date, propo, pondere, destroy)
    elif (Date, pair[0], pair[1]) in pondere.keys():
        pondere[(Date, pair[0], pair[1])] +=1
    elif pair[0] != pair[1]:
        pondere[(Date, pair[0], pair[1])] = 1
        propo[(pair[0], pair[1])] = (Date, pair[2])
    else:
        destroy.append((Date,pair))

    return propo, pondere, destroy

def GenereReseaux3(G, ListeNode, PatentList, apparie, dynamic):
    reseau = []    
    
    import datetime
    today = datetime.datetime.now().date().isoformat()
    for appar in apparie.keys():
        tempo = [appar]
        reseautemp = [(u+tempo) for u in genAppar(PatentList, apparie[appar][0], apparie[appar][1])]
        for k in reseautemp:
            if k not in reseau:
                reseau.append(k)
    Pondere = dict()
    Prop = dict()
    destroy = []
    DateLien = dict()
    ##cleaning
    tempo = []
    for pair in reseau:
        
        if isinstance(pair[0], list):
            if not isinstance(pair[1], list):
                for ll in pair[0]:
                    if ll != 'N/A' and ll != 'UNKNOWN':
                        tempo.append( [ll, pair[1], pair[2]])
            else:
                for ll in pair[0]:
                    if ll != 'N/A' and ll != 'UNKNOWN':
                        for uu in pair[1]:
                            if uu != 'N/A' and uu != 'UNKNOWN':
                                tempo.append( [ll, uu, pair[2]])
        elif isinstance(pair[1], list):
            for ll in pair[1]:
                    if ll != 'N/A' and ll != 'UNKNOWN':
                        tempo.append( [pair[0], ll, pair[2]])
        else:
            tempo.append(pair)
            
    # unnesting things
    for pair in reseau:
        for ind in range(len(pair)):
            if isinstance(pair[ind], list):
                if len(pair[ind]) ==1:
                    pair[ind] = pair[ind][0]
                else:
                    #print "paté pair ", pair 
                    pass
                    
        if DateLien.has_key(pair[2]):
            DateLien[pair[2]].append((pair[0], pair[1], pair[3]))
        else:
            DateLien[pair[2]] = [(pair[0], pair[1], pair[3])]
    lstDate = DateLien.keys()
    lstDate.sort()
    
    
    cmt = 0
    for Date in lstDate:
        for pair in DateLien[Date]:
            Prop, Pondere, destroy = MakePonderateAndProp(pair, Date, Prop, Pondere, destroy)
        if len(destroy) > 0:
            for uu in destroy:
                try:
                    DateLien[uu[0]].remove(uu[1])
                except:
                    cmt += 1
                    #print uu[1]
    #print "compteur des exceptions = ", cmt
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
           
            G.edge[ed[0]][ed[1]] ['time'] = [(len(lienExist), date, today)] #version simple          
            G.edge[ed[0]][ed[1]] ['deb'] = date #.isoformat()
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
        datesExists = [u for u in lstDate if datetime.datetime.strptime(u, "%Y-%m-%d") < datetime.datetime.today()]
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

def FindFather(noeud, liste):
    for k in liste:
        if noeud.count(k)>0:
            return k
    print noeud
    return 

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

    
def quote(string):
    import urllib
    try:
        return urllib.quote(string.replace(u'\u2002', ''), safe='/\\())')
    except:
        string=string.replace(u'\x80', '')
        string=string.replace(u'\x82', '')
        string=string.replace(u'\xf6', '')
        string = string.replace(u'\xe2', '', string.count(u'\xe2'))
        string = string.replace(u'\x80', '', string.count(u'\x80'))
        string = string.replace(u'\x82', '', string.count(u'\x82'))
        string = string.replace(u'\xe9', '', string.count(u'\xe9'))
        string = string.replace(u'\xd6', '', string.count(u'\xd6'))
        string = string.replace(u'\xd2', '', string.count(u'\xd2'))
        string = string.replace(u'\xf6', '', string.count(u'\xf6'))
        string = string.replace(u'\xe4', '', string.count(u'\xe4'))
        string = string.replace(u'\xe7', '', string.count(u'\xe7'))
        string = string.replace(u'\xfa', '', string.count(u'\xfa'))
        string = string.replace(u'\xe1', '', string.count(u'\xe1'))
        string = string.replace(u'\xf3', '', string.count(u'\xf3'))
        string = string.replace(u'\xed', '', string.count(u'\xed'))
        string = string.replace(u'\xe7', '', string.count(u'\xe7'))  
        string = string.replace(u'\xf1', '', string.count(u'\xf1')) 
        string = string.replace(u'\xf2', '', string.count(u'\xf2'))    
        string = string.replace(u'\xf3', '', string.count(u'\xf3')) 
        string = string.replace(u'\xf4', '', string.count(u'\xf4'))    
        string = string.replace(u'\xf5', '', string.count(u'\xf5')) 
        string = string.replace(u'\xf6', '', string.count(u'\xf6'))    
        string = string.replace(u'\xf7', '', string.count(u'\xf7')) 
        string = string.replace(u'\xf8', '', string.count(u'\xf8'))
        string = string.replace(u'\xf9', '', string.count(u'\xf9')) 
        string = string.replace(u'\xfa', '', string.count(u'\xfa'))
        string = string.replace(u'\xfb', '', string.count(u'\xfb')) 
        string = string.replace(u'\xfc', '', string.count(u'\xfc'))
        string = string.replace(u'\xfd', '', string.count(u'\xfd')) 
        string = string.replace(u'\xfe', '', string.count(u'\xfe'))     
        string = string.replace(u'\xeb', '', string.count(u'\xeb'))
        string = string.replace(u'\xef', '', string.count(u'\xef'))
        string = string.replace(u'\xc9', '', string.count(u'\xc9'))
        try:
            string = string.decode('latin1')
            string = string.encode('utf8')
        except:
            try:
                string = string.decode('cp1252')
                string = string.encode('utf8')
            except:
                        #print "unicode problem in formate"
        #                print string
                        pass
        
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
#    </attributes>
#    <attributes class="edge" mode="dynamic">
#  <attribute id="9" title="time" type="integer" />
#</attributes>
#<attributes class="node" mode="static">
#  <attribute id="0" title="category" type="string" />
#  <attribute id="1" title="val" type="integer" />
#  <attribute id="3" title="url" type="string" />
#  <attribute id="4" title="deb" type="string" />
#  <attribute id="5" title="fin" type="string" />
#</attributes>
#    <attributes class="node" mode="dynamic">
#        <attribute id="2" title="time" type="integer" />
#    </attributes>
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