REM This script is use to deploy from my own directory to git-hub connected one
REM this is also a comment of different programs :-)
REM useful things
copy /y requete.cql ..\..\P2N-Git\Development
copy /y cacert.pem ..\..\P2N-Git\Development
copy /y CollecteEtTRaite.bat ..\..\P2N-Git\Development
copy /y Compile.bat ..\..\P2N-Git\Development
copy /y Cars.csv ..\..\P2N-Git\Development
REM next is for publishing in github..this file
copy /y Deploy.bat ..\..\P2N-Git\Development
REM HTML Formating : Datatable
copy /y ScriptSearch.js ..\..\P2N-Git\Development
copy /y Modele.html ..\..\P2N-Git\Development\Modele.html
REM special, next one is for families datatable
copy /y SearchScript.js ..\..\P2N-Git\Development
copy /y ModeleFamille.html ..\..\P2N-Git\Development\ModeleFamille.html
REM HTML Formating : Pivotable
copy /y Pivot.html ..\..\P2N-Git\Development\Pivot.html
copy /y ModeleFamillePivot.html ..\..\P2N-Git\Development\ModeleFamillePivot.html
REM HTML Formating : Cartography
copy /y countries.json ..\..\P2N-Git\Development
copy /y ModeleCarto.html ..\..\P2N-Git\Development
copy /y ModeleCartoDeposant.html ..\..\P2N-Git\Development
copy /y NameCountryMap.csv ..\..\P2N-Git\Development
REM HTML Formating : NetWorks
copy /y Graphe.html ..\..\P2N-Git\Development
copy /y config.js ..\..\P2N-Git\Development
REM HTML Formating : Launching firefox # Deprecated
copy /y OpenNav.bat ..\..\P2N-Git\Development
REM HTML Formating : General index
REM THE MENU in root
copy /y ..\index.html dist
REM content of analyses
copy /y index.js dist 
REM Menus for each analyse
copy /y ModeleIndex.html ..\..\P2N-Git\Development\ModeleIndex.html
copy /y P2N.css ..\..\P2N-Git\Development\P2N.css
copy /y ModeleContenuIndex.html ..\..\P2N-Git\Development\ModeleContenuIndex.html
copy /y ModeleIndexRequete.html ..\..\P2N-Git\Development\ModeleIndexRequete.html

REM HTML Formating : External libraries
mkdir ..\..\P2N-Git\Development\extensions
mkdir ..\..\P2N-Git\Development\media
mkdir ..\..\P2N-Git\Development\lib2to3
mkdir ..\..\P2N-Git\Development\root

echo off
xcopy /y /s media ..\..\P2N-Git\Development\media\
xcopy /y /s extensions ..\..\P2N-Git\Development\extensions\
xcopy /y /s lib2to3 ..\..\P2N-Git\Development\lib2to3
xcopy /y /s root ..\..\P2N-Git\Development\root

echo on
REM Main programs

REM Main programs:Gatherersrs
copy OPSGatherPatentsV2.py ..\..\P2N-Git\Development
copy OPSGatherContentsv2-Iramuteq.py ..\..\P2N-Git\Development
copy OPSGatherAugment-Families.py ..\..\P2N-Git\Development
xcopy /y P2N-Networks.py ..\..\P2N-Git\Development
xcopy /y P2N-PreNetworks.py ..\..\P2N-Git\Development
xcopy /y P2N-NetworksJS.py ..\..\P2N-Git\Development

REM Next are not ready yet
REM copy P2N-Families.py ..\..\P2N-Git\Development
REM copy P2N-FamiliesHierarc.py ..\..\P2N-Git\Development
REM copy P2N-V5.py ..\..\P2N-Git\Development

REM Main programs:Formating exports

copy FusionIramuteq2.py ..\..\P2N-Git\Development
copy FormateExportDataTable.py ..\..\P2N-Git\Development
copy FormateExportDataTableFamilies.py ..\..\P2N-Git\Development
copy FormateExportPivotTable.py ..\..\P2N-Git\Development
copy FormateExportBiblio.py ..\..\P2N-Git\Development
copy FormateExportFamilies.py ..\..\P2N-Git\Development
copy CartographyCountry.py ..\..\P2N-Git\Development
copy FusionCarrot2.py ..\..\P2N-Git\Development
copy P2N-FreePlane.py ..\..\P2N-Git\Development\
copy FormateExportCountryCartography.py ..\..\P2N-Git\Development\
copy FormateExportAttractivityCartography.py ..\..\P2N-Git\Development\

REM Version files
xcopy /y *.txt  ..\..\P2N-Git\Development
xcopy /y *.sh  ..\..\P2N-Git\Development
xcopy /y *.bat  ..\..\P2N-Git\Development

REM Tools (fusioning two collects)
copy FusionPatentList2.py ..\..\P2N-Git\Development
copy Interface2.py ..\..\P2N-Git\Development
copy /y P2N_Lib.py ..\..\P2N-Git\Development\
copy /y P2N_FreePlaneLib.py ..\..\P2N-Git\Development\
copy parallel3.py ..\..\P2N-Git\Development

REM Externals Libraries

copy /y Networkx_functs.py ..\..\P2N-Git\Development
