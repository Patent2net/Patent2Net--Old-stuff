rmdir /S /Q dist\Patent2Net

pyinstaller -y --noupx --specpath=specs --clean FormateExportAttractivityCartography.py
pyinstaller -y --noupx --specpath=specs --clean OPSGatherPatentsv2.py
pyinstaller -y --noupx --specpath=specs --clean OPSGatherContentsv2-Iramuteq.py
pyinstaller -y --noupx --specpath=specs --clean OPSGatherAugment-Families.py
pyinstaller -y --noupx --specpath=specs --clean P2N-networksMix.py
pyinstaller -y --noupx --specpath=specs --clean P2N-networksCit.py
pyinstaller -y --noupx --specpath=specs --clean FusionIramuteq2.py
pyinstaller -y --noupx --specpath=specs --clean Fusion.py
pyinstaller -y --noupx --specpath=specs --clean P2N-FreePlane.py
pyinstaller -y --noupx --specpath=specs --clean FormateExportDataTable.py
pyinstaller -y --noupx --specpath=specs --clean FormateExportPivotTable.py
pyinstaller -y --noupx --specpath=specs --clean FormateExportDataTableFamilies.py
pyinstaller -y --noupx --specpath=specs --clean FormateExportBiblio.py
pyinstaller -y --noupx --specpath=specs --clean FormateExportCountryCartography.py
pyinstaller -y --noupx --specpath=specs --clean FusionCarrot2.py
pyinstaller -y --noupx --specpath=specs --clean Interface2.py

pyinstaller -y --noupx --specpath=specs FormateExportAttractivityCartography.spec
pyinstaller -y --noupx --specpath=specs OPSGatherPatentsv2.spec
pyinstaller -y --noupx --specpath=specs OPSGatherContentsv2-Iramuteq.spec
pyinstaller -y --noupx --specpath=specs OPSGatherAugment-Families.spec
pyinstaller -y --noupx --specpath=specs P2N-networksMix.spec
pyinstaller -y --noupx --specpath=specs P2N-networksCit.spec
pyinstaller -y --noupx --specpath=specs FusionIramuteq2.spec
pyinstaller -y --noupx --specpath=specs Fusion.spec
pyinstaller -y --noupx --specpath=specs P2N-FreePlane.spec
pyinstaller -y --noupx --specpath=specs FormateExportDataTable.spec
pyinstaller -y --noupx --specpath=specs FormateExportPivotTable.spec
pyinstaller -y --noupx --specpath=specs FormateExportDataTableFamilies.spec
pyinstaller -y --noupx --specpath=specs FormateExportBiblio.spec
pyinstaller -y --noupx --specpath=specs FormateExportCountryCartography.spec
pyinstaller -y --noupx --specpath=specs FusionCarrot2.spec
pyinstaller -y --noupx --specpath=specs Interface2.spec

mkdir dist\Patent2Net\

xcopy /S /Y dist\FormateExportAttractivityCartography dist\Patent2Net\ 
xcopy /S /Y dist\OPSGatherPatentsv2 dist\Patent2Net\ 
xcopy /S /Y dist\OPSGatherContentsv2-Iramuteq dist\Patent2Net\
xcopy /S /Y dist\OPSGatherAugment-Families dist\Patent2Net\
xcopy /S /Y dist\P2N-NetworksMix dist\Patent2Net\
xcopy /S /Y dist\P2N-NetworksCit dist\Patent2Net\
xcopy /S /Y dist\FusionIramuteq2 dist\Patent2Net\
xcopy /S /Y dist\Fusion dist\Patent2Net\
xcopy /S /Y dist\P2N-FreePlane dist\Patent2Net\
xcopy /S /Y dist\FormateExportDataTable dist\Patent2Net\
xcopy /S /Y dist\FormateExportPivotTable dist\Patent2Net\
xcopy /S /Y dist\FormateExportDataTableFamilies dist\Patent2Net\
xcopy /S /Y dist\FormateExportBiblio dist\Patent2Net\
xcopy /S /Y dist\FormateExportCountryCartography dist\Patent2Net\
xcopy /S /Y dist\FusionCarrot2 dist\Patent2Net\
xcopy /S /Y dist\Interface2 dist\Patent2Net\


rmdir /S /Q dist\FormateExportAttractivityCartography
rmdir /S /Q dist\OPSGatherPatentsv2
rmdir /S /Q dist\OPSGatherContentsv2-Iramuteq
rmdir /S /Q dist\OPSGatherAugment-Families
rmdir /S /Q dist\P2N-NetworksMix
rmdir /S /Q dist\P2N-NetworksCit
rmdir /S /Q dist\FusionIramuteq2
rmdir /S /Q dist\Fusion
rmdir /S /Q dist\P2N-FreePlane
rmdir /S /Q dist\FormateExportDataTable
rmdir /S /Q dist\FormateExportPivotTable
rmdir /S /Q dist\FormateExportDataTableFamilies
rmdir /S /Q dist\FormateExportBiblio
rmdir /S /Q dist\FormateExportCountryCartography
rmdir /S /Q dist\FusionCarrot2 
rmdir /S /Q dist\Interface2



REM xcopy /S /Y dist\P2N-FamiliesHierarc dist\Patent2Net\

xcopy /Y root\* dist\

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
mkdir dist\Patent2Net\lib2to3
xcopy /S /Y lib2to3 dist\Patent2Net\lib2to3
mkdir dist\Patent2Net\extensions
mkdir dist\Patent2Net\media
xcopy /S /Y extensions dist\Patent2Net\extensions
xcopy /S /Y media dist\Patent2Net\media
