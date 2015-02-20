# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 07:53:30 2014

@author: dreymond
"""
import sys, os



with open("..//Requete.cql", "r") as fic:
    contenu = fic.readlines()
    for lig in contenu:
        #if not lig.startswith('#'):
            if lig.count('request:')>0:
                requete=lig.split(':')[1].strip()
            if lig.count('DataDirectory:')>0:
                ndf = lig.split(':')[1].strip()

Rep = '..//DONNEES//'+ndf+'//PatentContents'

def GenereListeFichiers(rep):
    """ prend un dossier en paramètre (chemin absolu) et génère la liste
    complète des fichiers TXT de l'arborescence"""
    import os
    listeFicFR = []
    listeFicEN = []
    listeFicUNK = []
    for root, subFolders, files in os.walk(rep):
        for fichier in files:
            if fichier.endswith('.txt') and fichier.startswith('FR'):
                listeFicFR.append(root+'//'+fichier)
            elif fichier.endswith('.txt') and fichier.startswith('EN'):
                listeFicEN.append(root+'//'+fichier)
            else:
                if fichier.endswith('.txt'):
                    listeFicUNK.append(root+'//'+fichier)
        if len(subFolders)>0:
            for sousRep in subFolders:
                tempo = GenereListeFichiers(rep+'//'+sousRep)
                listeFicFR.extend(tempo[0])
                listeFicEN.extend(tempo[0])
                listeFicUNK.extend(tempo[0])
                
    return (listeFicFR, listeFicEN, listeFicUNK)


tempo = GenereListeFichiers(Rep)


def Normalise(listeFic):
    """Necessary becaus in OPSGatentsPAtents, I didn't care about abstracts name,
    there is a missing '-' in name creation: should be LANG-PatentNum.txt"""
    cpt = 0    
    for fic in listeFic:
        if fic.count('Abstracts')>0:
            tmp = fic.split('//')
            nomDeFic = tmp[len(tmp)-1]
            NouveauNom = nomDeFic[0:2].replace('-', '')  +'-'+ nomDeFic[2:].replace('-', '')

            try:
                os.rename(fic, fic.replace(nomDeFic, NouveauNom))
                cpt+=1
            except:
                pass
    print cpt, " Abstracts files Names normalized" 


def coupeEnMots(texte):
    "renvoie une liste de mots propres des signes de ponctuation et autres cochonneries"
    texte= texte.lower()
    import re 
    res = re.sub('['+"[]?!"+']', ' ', texte) # on vire la ponctuation 
    res = re.sub('\d', ' ', res) # extraction des chiffres #numeric are avoided
    res = re.findall('\w+', res, re.UNICODE) # extraction des lettres seulement #only letters, no symbols
    return res
    
def LectureFichier(fic):
    """read the file, and return purged from coupeEnMots content if lenght is greater thar arbitrary value, here 5"""
    with open(fic) as fi:
            lect = fi.read()
            if len(' '.join(coupeEnMots(lect)))> 5: #arbitrary
                contenu =lect +'\n'
                return contenu
            else:
                return None
                
def complete(listeFic, lang):
   
    resum = [fi for fi in set(listeFic) if fi.count('Abstracts')>0]
    desc = [fi for fi in set(listeFic) if fi.count('description')>0]
    autres = [fi for fi in set(listeFic) if fi not in resum and fi not in desc]
    dejaVu = []
    Ignore = 0
    FicResume = ""
    Contenu = """"""
    for fichier in set(desc):
        dejaVu.append(fichier)
        if LectureFichier(fichier) is not None:
            Contenu+=LectureFichier(fichier)
        else:
            Ignore+=1
#            tmp = fichier.name.split('//')
            
            ## writing now abstracts (they have no iramtuteq tag)
        FicResume= fichier.replace('description', 'Abstracts')
        if FicResume in resum:
            dejaVu.append(FicResume)
            if LectureFichier(FicResume) is not None:
                Contenu+=LectureFichier(FicResume)
            else:
                Ignore+=1
        FicRevend= fichier.replace('description', 'claims')
        if FicRevend in autres:
            dejaVu.append(FicRevend)
            if LectureFichier(FicRevend) is not None:
                Contenu+=LectureFichier(FicRevend)
            else:
                Ignore+=1
                
    for fichier in set(autres):
        
        if fichier not in dejaVu:
            dejaVu.append(FicResume)
            if LectureFichier(fichier) is not None:
                Contenu+=LectureFichier(fichier)
            else:
                Ignore+=1
    print len(set(listeFic)), "fichiers à traiter en langage : ", lang
    print len(dejaVu), " fichiers traités et ", Ignore, " fichier(s) ignores"
    return Contenu

ind = 0
for lang in ['FR', 'EN', 'UNK']:
    NomResult = lang+'-'+ndf+'.txt'
    ficRes = open(Rep+'//'+lang+'_'+ndf+'.txt', "w")
    ficRes.write(complete(tempo[ind], lang))
    ind+=1
    ficRes.close()
    