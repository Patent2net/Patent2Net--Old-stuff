# Patent2Net configuration file
##############################
# request
# insert below your request in cql format as done in the example
request: TI=Respirator AND IPC= A61M1

##############################
# Directory to use
# insert a compliant name (no space or special characters) for the "Patent Universe" (PU)
DataDirectory: Respirator

###############################
#Patent2Net options : Set to *True* or False
###############################
# Collecting
# patents list corresponding to the request. e.g the "Patent Universe" (PU)
GatherPatent: True

# patents bibliographic data corresponding to patent list
GatherBiblio: True

# patent content (description, abstract, claims) completing patents bibliographic data
GatherContent: True
OPSGatherContentsv2-Iramuteq: False

#patents families extending the PU to families
GatherFamilly: True

###############################
# Networks. Produce both online and for download and local use of Gephi
# Inventors' network 
InventorNetwork: True

# Applicants' network
ApplicantNetwork: True

# IPCs' network
CrossTechNetwork: True

# Applicants and Inventors network
ApplicantInventorNet: True

# Applicants and IPCs' network
ApplicantCrossTechNetwork: True

# Inventors and IPCs' network 
InventorCrossTechNetwork: True

# Countries and IPCs' network
CountryCrossTechNetwork: True

# Network of references for the PU (each reference cited by each patent within the PU, includes external bibliographic refs) 
ReferencesNetwork: True

# Network of citation for the PU (each patent cited within the PU cited in the rest of the patents world) 
CitationsTechNetwork: True

# Network of equivalent patents for each patent within the PU
EquivalentsTechNetwork: True

# The total network
CompleteNetwork: True

# Complete families network
FamiliesNetwork: True
FamiliesHierarchicNetwork: True

###############################
#  Mindmaps of IPCs both online and for download and local use of freeplane
P2N-FreePlane: True

###############################
# export patents as a bibligraphic file in bibTex format
FormateExportBiblio: True

###############################
# Produce the world maps of inventors, applicants, deposit country
FormateExportAttractivityCartography: False
FormateExportCountryCartography: True

###############################
# Patents as a table
FormateExportDataTable: True
FormateExportDataTableFamilies: True

###############################
# Prepare interactive pivottable
FormateExportPivotTable: True

###############################
# prepare Abstracts, descriptions, claims for text analysis
# for download and local use of Carrot2 and Iramuteq
FusionCarrot2: True
FusionIramuteq2: True

