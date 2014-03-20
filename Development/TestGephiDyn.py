# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 13:45:03 2014

@author: dreymond
"""

import networkx

ndf = '3Dprint2Dyn.gexf'

G = networkx.read_gexf('GephiFiles\\3DPrintDyn.gexf')

for n in G.nodes():
    print n
    