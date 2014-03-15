# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 07:53:50 2014

@author: dreymond
"""




from Ops2 import *
#import datetime
import sys, os

# construction de la liste de Brevets associés à des mots clés
nb = len(sys.argv)
request = ""
for u in sys.argv[1:nb]:
    request += u.strip() # #sys.argv[1]#

tempoPath = 'PatentLists'
ClaimPath = 'Claims'

if os.listdir('.').count(tempoPath) ==0:
    os.mkdir(tempoPath)
    

if os.listdir('.').count(ClaimPath) ==0:
    os.mkdir(ClaimPath)

ListeBrevet = list() # results
import pickle

ndf = sys.argv[1]
if not ndf.endswith(".dump"):
    print "fichier incorrect"
    print "GatherOPS nom_de_fichier.dump keyword OPERATOR keyword..."

try:
    ndfLstBrev = open(tempoPath+'//'+ndf, 'r')
    Brevets = pickle.load(ndfLstBrev)
    ndfLstBrev.close()
    print "Patent list loaded from file: '"+ndf+"'."
    print len(Brevets), " patents found. Gatherind claims from OPS."
    print "The program will try to gather from OPS db in this order: priority, application, publication."
    ListeOk = True
except:
    print "Please use Ops-Gather-PatentList before this program."
    ListeOk = False
    
if ListeOk:
    fic = open(ClaimPath + '\\' + ndf +'.txt', 'w')
    cpt = 0
    StatGatClaims = dict()
    for Brevet in Brevets:
       # try:
            PatentData = dict() #the dictionnary will content the list of patent data extrated 
            NumBrevet = Brevet[u'exchange-document'][u'@country']+Brevet[u'exchange-document'][ u'@doc-number']
            PatentData['label'] =  NumBrevet
            
            #building the url request to retreive patent bibliography
            #print "numéro de Brevet ", NumBrevet        
            
            ClaimBrevet = ExtraitClaim('priority', NumBrevet)
            time.sleep(6)
            if ClaimBrevet is None:
                ClaimBrevet = ExtraitClaim('application', NumBrevet)
                #print "trying application"
                time.sleep(6)
                if ClaimBrevet is None:
                    ClaimBrevet = ExtraitClaim('publication', NumBrevet)
                    #print 'trying publication'
                    time.sleep(6)
            
            # in some cases OPS return more than one document...
            # we copy the structure so as they come as they where from separates requests
     
                # printing to reassure the user  
            if ClaimBrevet is not None:
                print "claim gathered, storing..."
                        
                fic.write('**** *Claims_'+NumBrevet+'\n')
                fic.write(ClaimBrevet)
                fic.write('\n\n')
                StatGatClaims[NumBrevet] = len(ClaimBrevet.split(' '))
                cpt +=1
            else:
                StatGatClaims[NumBrevet] = "Null"
                
    print "Claim gathering results"
    ficEchoues = open('NoClaims'+ndf+'csv', 'w')
    print "claims collected pour ", cpt, " patents over ", len(Brevets)
    for brev in StatGatClaims:
        if StatGatClaims[brev] == 'Null':
            print 'patent, ', brev, "without claims ?"
            ficEchoues.write(brev+';')
        else:
            print StatGatClaims[brev], ' words collected for patent:', brev
    #saving data gathered in a file   
    fic.close()
    ficEchoues.close()