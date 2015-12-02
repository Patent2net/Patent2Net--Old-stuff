# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 07:45:45 2015

@author: dreymond
"""

from multiprocessing import Process, Pool, Queue, Lock, JoinableQueue, freeze_support
import os

RequeteFolder = "..\\REQUESTS"
TempoFolderReq = "TEMPOREQ"




#def GenereProcessSuite(cmds):

        

#lstPrg = ["FormateExportAttractivityCartography.exe", "FormateExportCountryCartography.exe", "FormateExportBiblio.exe", "FormateExportDataTable.exe",
 #                 "FormateExportDataTableFamilies.exe", "FormateExportPivotTable.exe", "FusionCarrot2.exe", "FusionIramuteq2.exe",
  #                "P2N-networksCit.exe", "P2N-FreePlane.exe", "P2N-networksMix.exe", "Interface2.exe"]


def SafeOpenWriteRequests(FileName, SavReq, TempoForderReq):
    #saving current file
    command = "copy /Y  ..\\requete.cql " + TempoForderReq+'\\' + SavReq
    os.system(command)
    try:    
        os.remove('..\\requete.cql')
    except:
        "print should put a request in folder... doing it for you"
    command = 'copy /Y ' +FileName +' ..\\requete.cql'
    os.system(command)
    print "done saving requete, replaced by", FileName    


def RestoreRequests(FileName, SavReq, TempoForderReq):
    #saving current file
    command = "copy /Y "+ TempoForderReq+'\\' + SavReq + ' ..\\requete.cql' 
    os.system(command)     
    os.remove(TempoForderReq+'\\' + SavReq)
    
    print "done restoring " , FileName," replacing by previous"   
    
def Collecteurs(QueueCollecteur):
    cmd = QueueCollecteur.get()
    command = os.system(cmd)
    p = Process(target=command, args=(lock))
    p.start()
    p.join()
if TempoFolderReq not in os.listdir('.'):
    os.makedirs(TempoFolderReq)
    
lstReq = [fic for fic in os.listdir(RequeteFolder) if fic.endswith('cql')] 
    
#    
#STEPS = dict()
#
#STEPS = { 1:"OPSGatherPatentsv2.exe", 
#            1.1: ["FormateExportDataTable.exe", "P2N-networksCit.exe", "P2N-networksMix.exe",
#                  "P2N-FreePlane.exe", "FormateExportBiblio.exe", "FormateExportAttractivityCartography.exe",
#                  "FormateExportCountryCartography.exe"],
#        2: "OPSGatherAugment-Families.exe",
#            2.1: ["FormateExportDataTableFamilies.exe", "FormateExportPivotTable.exe"],
#        3 :"OPSGatherContentsv2-Iramuteq.exe",
#            3.1: ["FusionCarrot2.exe", "FusionIramuteq2.exe"],
#        4:"Interface2.exe"
#        }
gatherers = ["OPSGatherPatentsv2.exe","OPSGatherAugment-Families.exe", "OPSGatherContentsv2-Iramuteq.exe"]
traite1 = ["FormateExportDataTable.exe", "P2N-networksCit.exe", "P2N-networksMix.exe",
                  "P2N-FreePlane.exe", "FormateExportBiblio.exe", "FormateExportAttractivityCartography.exe",
                  "FormateExportCountryCartography.exe"]
traite2 = ["FormateExportDataTableFamilies.exe", "FormateExportPivotTable.exe"]
traite3 = ["FusionCarrot2.exe", "FusionIramuteq2.exe"]

#def pool_func(q):
#    while True:
#        allRenderArg, otherArg = q.get() # blocks until the queue has an item
#        try:
#            render(allRenderArg, otherArg)
#        finally: q.task_done()


def Gatherer (request):
    QueueGatherer = Pool (processes = 1)
    SafeOpenWriteRequests(RequeteFolder+"\\" +request, "requeteOld"+request, TempoFolderReq)    
    iterat = QueueGatherer.imap(os.system, gatherers)
    iterat.next()
    QueueNets = Pool (processes = 4)
    QueueNets.map(os.system, traite1)
    iterat.next()
    QueueNets2 = Pool (processes = 2)
    QueueNets2.map(os.system, traite2)
    iterat.next()
    QueueNets3 = Pool (processes = 2)
    QueueNets3.map(os.system, traite3)
    command = os.system(".\\Interface2.exe")
    p = Process(target=command)
    p.start()
    p.join()
    
    
if __name__ == '__main__':
    lock = Lock()
    freeze_support()
     # no max size for the moment
    QueueP2N = Pool (processes = 3)
    for req in lstReq:
        QueueP2N.apply(Gatherer (req)) # asynchronous mode impossible as  all programms uses requete.cql...
        # if this las point is modified in order to use any file as parameter the parrallised process could be started
        
#