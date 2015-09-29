REM This script is use to deploy from my own directory to git-hub connected one
REM this is also a comment of different programs :-)
REM useful things
copy /y requete.cql ..\..\..\Development
copy /y cacert.pem ..\..\..\Development
copy /y CollecteEtTRaite.bat ..\..\..\Development
copy /y Compile.bat ..\..\..\Development
copy /y Cars.csv ..\..\..\Development
REM next is for publishing in github..this file
copy /y Deploy.bat ..\..\..\Development
REM HTML Formating : Datatable
copy /y ScriptSearch.js ..\..\..\Development
copy /y Modele.html ..\..\..\Development\Modele.html
REM special, next one is for families datatable
copy /y SearchScript.js ..\..\..\Development
copy /y ModeleFamille.html ..\..\..\Development\ModeleFamille.html
REM HTML Formating : Pivotable
copy /y Pivot.html ..\..\..\Development\Pivot.html
copy /y ModeleFamillePivot.html ..\..\..\Development\ModeleFamillePivot.html
REM HTML Formating : Cartography
copy /y countries.json ..\..\..\Development
copy /y ModeleCarto.html ..\..\..\Development
copy /y ModeleCartoDeposant.html ..\..\..\Development
copy /y NameCountryMap.csv ..\..\..\Development
REM HTML Formating : NetWorks
copy /y Graphe.html ..\..\..\Development
copy /y config.js ..\..\..\Development
REM HTML Formating : Launching firefox # Deprecated
copy /y OpenNav.bat ..\..\..\Development
REM HTML Formating : General index
REM THE MENU in root
copy /y ..\index.html dist
REM content of analyses
copy /y index.js dist 
REM Menus for each analyse
copy /y ModeleIndex.html ..\..\..\Development\ModeleIndex.html
copy /y ModeleContenuIndex.html ..\..\..\Development\ModeleContenuIndex.html
copy /y ModeleIndexRequete.html ..\..\..\Development\ModeleIndexRequete.html

REM HTML Formating : External libraries
mkdir ..\..\..\Development\extensions
mkdir ..\..\..\Development\media
echo off
xcopy /y /s media ..\..\..\Development\media\
xcopy /y /s extensions ..\..\..\Development\extensions\
echo on
REM Main programs

REM Main programs:Collectors
copy OPSGatherPatentsV2.py ..\..\..\Development
copy OPSGatherAugment-Families.py ..\..\..\Development
REM the buggy content iramuteq collector
REM copy OPSGatherContentsv1-Iramuteq.py ..\..\..\Development
REM the abstract content iramuteq collector (seems consistent !). Done by OPSGather
REM copy OPSGatherAbstracts-Iramuteq.py ..\..\..\Development
REM Cleaning after collect useless now
REM copy Cleaning.py ..\..\..\Development
REM Main programs:Networks productions
copy P2N-Authors.py ..\..\..\Development
copy P2N-AuthorsApplicants.py ..\..\..\Development
copy P2N-Applicants.py ..\..\..\Development
copy P2N-ApplicantsCrossTech.py ..\..\..\Development
copy P2N-CountryCrossTech.py ..\..\..\Development
copy P2N-InventorCrossTech.py ..\..\..\Development
copy P2N-CrossTech.py ..\..\..\Development
copy P2N-Families.py ..\..\..\Development
copy P2N-FamiliesHierarc.py ..\..\..\Development
copy P2N-V5.py ..\..\..\Development

REM Main programs:Formating exports
Rem oldest Iramuteq fusionner
REM copy FusionIramuteq.py ..\..\..\Development
Rem The new one. Works better for abstracts
copy FusionIramuteq2.py ..\..\..\Development
copy FormateExport.py ..\..\..\Development
copy FormateExportFamilies.py ..\..\..\Development
copy CartographyCountry.py ..\..\..\Development

REM Tools (fusioning two collects)
copy Fusion.py ..\..\..\Development
REM copy Interface.py ..\..\..\Development
REM previous is deprecated since interface2 version
copy Interface2.py ..\..\..\Development
REM Libraries (most need some cleaning)
REM copy /y Ops2.py ..\..\..\Development\
REM copy /y Ops3.py ..\..\..\Development\
REM copy /y Ops2NetUtils.py ..\..\..\Development
REM copy /y Ops2NetUtils2.py ..\..\..\Development
copy /y P2N_Lib.py ..\..\..\Development\

copy /y AttractivityCartography.py ..\..\..\Development
REM Externals Libraries

copy /y Networkx_functs.py ..\..\..\Development
REM next one is unused and buggy... sometime I'll try to implement nooverlap and a good force atlas algorithm
REM copy /y forceatlas.py ..\..\..\Development
