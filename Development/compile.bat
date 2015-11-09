rmdir /S /Q dist\Patent2Net
REM pyinstaller -y OPSGatherAbstracts-Iramuteq.py
pyinstaller -y FormateExportAttractivityCartography.py
REM pyinstaller -y Cleaning.py
pyinstaller -y OPSGatherPatentsv2.py
REM pyinstaller -y OPSGatherContentsv1-Iramuteq.py
pyinstaller -y OPSGatherAugment-Families.py
pyinstaller -y P2N-networksMix.py

REM pyinstaller -y P2N-Families.py
REM pyinstaller -y P2N-FamiliesHierarc.py
pyinstaller -y FusionIramuteq2.py
pyinstaller -y Fusion.py
pyinstaller -y P2N-FreePlane.py

pyinstaller -y FormateExportDataTable.py
pyinstaller -y FormateExportPivotTable.py
pyinstaller -y FormateExportDataTableFamilies.py
pyinstaller -y FormateExportBiblio.py
REM pyinstaller -y FormateExportFamilies.py
pyinstaller -y FormateExportCountryCartography.py
pyinstaller -y FusionCarrot2.py

pyinstaller -y Interface2.py
pyinstaller -y OPSGatherPatentsv2.spec

pyinstaller -y FusionCarrot2.spec
pyinstaller -y OPSGatherAugment-Families.spec
pyinstaller -y FormateExportCountryCartography.spec
pyinstaller -y P2N-FreePlane.spec

pyinstaller -y P2N-networksMix.spec
REM pyinstaller -y P2N-Families.spec
pyinstaller -y FusionIramuteq2.spec

pyinstaller -y FormateExportDataTable.spec
pyinstaller -y FormateExportPivotTable.spec
pyinstaller -y FormateExportBiblio.spec
pyinstaller -y FormateExportFamilies.spec
pyinstaller -y FormateExportDataTableFamilies.spec
pyinstaller -y Fusion.spec
REM pyinstaller -y P2N-FamiliesHierarc.spec

pyinstaller -y Interface2.spec

pyinstaller -y FormateExportAttractivityCartography.spec

mkdir dist\Patent2Net\
copy /Y requete.cql dist
copy /y cacert.pem dist\Patent2Net\
copy /y countries.json dist\patent2Net
copy /y P2N.css dist\patent2Net
copy /y ModeleCarto.html dist\patent2Net
copy /y ModeleCartoDeposant.html dist\patent2Net
copy /y NameCountryMap.csv dist\Patent2Net\
copy /y scriptSearch.js dist\Patent2Net\
copy /y Searchscript.js dist\Patent2Net\
copy /y config.js dist\Patent2Net\
copy /y CollecteETRaite.bat dist
copy /y Modele.html dist\Patent2Net\Modele.html
copy /y Graphe.html dist\Patent2Net\Graphe.html
copy /y OpenNav.bat dist\Patent2Net\OpenNav.bat
copy /y ModeleFamille.html dist\Patent2Net\ModeleFamille.html
copy /y ModeleFamillePivot.html dist\Patent2Net\ModeleFamillePivot.html
copy /y Pivot.html dist\Patent2Net\Pivot.html
copy /y ModeleIndex.html dist\Patent2Net\ModeleIndex.html
copy /y ModeleContenuIndex.html dist\Patent2Net\ModeleContenuIndex.html
copy /y ModeleIndexRequete.html dist\Patent2Net\
copy /y cles-epo.txt dist
copy /y ..\index.html dist
copy /y ..\index.js dist
REM xcopy /S /Y dist\OPSGatherAbstracts-Iramuteq dist\Patent2Net\
xcopy /S /Y dist\FormateExportAttractivityCartography dist\Patent2Net\ 
REM xcopy /S /Y dist\Cleaning dist\Patent2Net\ 
xcopy /S /Y dist\OPSGatherPatentsv2 dist\Patent2Net\ 
xcopy /S /Y dist\P2N-FamiliesHierarc dist\Patent2Net\
REM xcopy /S /Y dist\OPSGatherContentsv1-Iramuteq dist\Patent2Net\
xcopy /S /Y dist\OPSGatherAugment-Families dist\Patent2Net\
xcopy /S /Y dist\P2N-NetworksMix dist\Patent2Net\

REM xcopy /S /Y dist\P2N-Families dist\Patent2Net\

xcopy /S /Y dist\FusionIramuteq2 dist\Patent2Net\
xcopy /S /Y dist\FusionCarrot2 dist\Patent2Net\

xcopy /S /Y dist\FormateExportDataTable dist\Patent2Net\
xcopy /S /Y dist\FormateExportPivotTable dist\Patent2Net\
xcopy /S /Y dist\FormateExportBiblio dist\Patent2Net\
xcopy /S /Y dist\FormateExportDataTableFamilies dist\Patent2Net\
xcopy /S /Y dist\Fusion dist\Patent2Net\
xcopy /S /Y dist\P2N-FreePlane dist\Patent2Net\
mkdir dist\Patent2Net\lib2to3
xcopy /S /Y lib2to3 dist\Patent2Net\lib2to3

xcopy /S /Y dist\FormateExportCountryCartography dist\Patent2Net\

xcopy /S /Y dist\Interface2 dist\Patent2Net\
mkdir dist\Patent2Net\extensions
mkdir dist\Patent2Net\media
xcopy /S /Y extensions dist\Patent2Net\extensions
xcopy /S /Y media dist\Patent2Net\media
rmdir /S /Q dist\OPSGatherAbstracts-Iramuteq
rmdir /S /Q dist\FormateExportAttractivityCartography
rmdir /S /Q dist\FormateExportCountryCartography

rmdir /S /Q dist\OPSGatherPatentsv2
rmdir /S /Q dist\OPSGatherContentsv1-Iramuteq
rmdir /S /Q dist\P2N-NetworksMix
rmdir /S /Q dist\P2N-FreePlane
rmdir /S /Q dist\OPSGatherAugment-Families
REM rmdir /S /Q dist\P2N-Families
rmdir /S /Q dist\FusionIramuteq2
rmdir /S /Q dist\FusionCarrot2 
rmdir /S /Q dist\Fusion
REM rmdir /S /Q dist\P2N-V5
REM rmdir /S /Q dist\FormateExport
rmdir /S /Q dist\FormateExportDataTable
rmdir /S /Q dist\FormateExportPivotTable
rmdir /S /Q dist\FormateExportBiblio
rmdir /S /Q dist\FormateExportDataTableFamilies
rmdir /S /Q dist\P2N-FamiliesHierarc
rmdir /S /Q dist\CartographyCountry
REM rmdir /S /Q dist\Interface
rmdir /S /Q dist\Interface2
REM rmdir /S /Q dist\Cleaning