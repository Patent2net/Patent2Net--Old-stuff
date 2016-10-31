rmdir /S /Q dist\Patent2Net64

pyinstaller -y --noupx --specpath=specs --clean  --version-file=version-FormateExportAttractivityCartography.txt FormateExportAttractivityCartography.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-OPSGatherPatentsv2.txt OPSGatherPatentsv2.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-OPSGatherContentsv2-Iramuteq.txt OPSGatherContentsv2-Iramuteq.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-OPSGatherAugment-Families.txt OPSGatherAugment-Families.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-Compatibilizer.txt  Compatibilizer.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-P2N-PreNetworks.txt P2N-PreNetworks.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-P2N-Networks.txt P2N-Networks.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-P2N-NetworksJS.txt P2N-NetworksJS.py


pyinstaller -y --noupx --specpath=specs --clean --version-file=version-FusionIramuteq2.txt FusionIramuteq2.py
REM DEPRECATED pyinstaller -y --noupx --specpath=specs --clean --version-file=version-Fusion.txt Fusion.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-Fusion.txt FusionPatentList2.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-P2N-FreePlane.txt P2N-FreePlane.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-FormateExportDataTable.txt FormateExportDataTable.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-FormateExportPivotTable.txt FormateExportPivotTable.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-FormateExportDataTableFamilies.txt FormateExportDataTableFamilies.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-FormateExportBiblio.txt FormateExportBiblio.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-FormateExportCountryCartography.txt FormateExportCountryCartography.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-FusionCarrot2.txt FusionCarrot2.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-Interface2.txt Interface2.py
pyinstaller -y --noupx --specpath=specs --clean --version-file=version-Parallel3.txt Parallel3.py

pyinstaller -y --noupx --version-file=version-FormateExportAttractivityCartography.txt specs\FormateExportAttractivityCartography.spec
pyinstaller -y --noupx --version-file=version-OPSGatherPatentsv2.txt specs\OPSGatherPatentsv2.spec
pyinstaller -y --noupx --version-file=version-OPSGatherContentsv2-Iramuteq.txt specs\OPSGatherContentsv2-Iramuteq.spec
pyinstaller -y --noupx --version-file=version-OPSGatherAugment-Families.txt specs\OPSGatherAugment-Families.spec
pyinstaller -y --noupx --version-file=version-Compatibilizer.txt specs\Compatibilizer.spec

pyinstaller -y --noupx --version-file=version-P2N-Networks.txt specs\P2N-Networks.spec
pyinstaller -y --noupx --version-file=version-P2N-PreNetworks.txt specs\P2N-PreNetworks.spec
pyinstaller -y --noupx --version-file=version-P2N-NetworksJS.txt specs\P2N-NetworksJS.spec

pyinstaller -y --noupx --version-file=version-FusionIramuteq2.txt specs\FusionIramuteq2.spec
REM pyinstaller -y --noupx --version-file=version-Fusion.txt specs\Fusion.spec
pyinstaller -y --noupx --version-file=version-Fusion.txt specs\FusionPatentList2.spec
pyinstaller -y --noupx --version-file=version-P2N-FreePlane.txt specs\P2N-FreePlane.spec
pyinstaller -y --noupx --version-file=version-FormateExportDataTable.txt specs\FormateExportDataTable.spec
pyinstaller -y --noupx --version-file=version-FormateExportPivotTable.txt specs\FormateExportPivotTable.spec
pyinstaller -y --noupx --version-file=version-FormateExportDataTableFamilies.txt specs\FormateExportDataTableFamilies.spec
pyinstaller -y --noupx --version-file=version-FormateExportBiblio.txt specs\FormateExportBiblio.spec
pyinstaller -y --noupx --version-file=version-FormateExportCountryCartography.txt specs\FormateExportCountryCartography.spec
pyinstaller -y --noupx --version-file=version-FusionCarrot2.txt specs\FusionCarrot2.spec
pyinstaller -y --noupx --version-file=version-Interface2.txt specs\Interface2.spec
pyinstaller -y --noupx --version-file=version-Parallel3.txt specs\Parallel3.spec

mkdir dist\Patent2Net64\

xcopy /S /Y dist\FormateExportAttractivityCartography dist\Patent2Net64\ 
xcopy /S /Y dist\OPSGatherPatentsv2 dist\Patent2Net64\ 
xcopy /S /Y dist\OPSGatherContentsv2-Iramuteq dist\Patent2Net64\
xcopy /S /Y dist\OPSGatherAugment-Families dist\Patent2Net64\
xcopy /S /Y dist\Compatibilizer dist\Patent2Net64\


xcopy /S /Y dist\P2N-Networks dist\Patent2Net64\
xcopy /S /Y dist\P2N-PreNetworks dist\Patent2Net64\
xcopy /S /Y dist\P2N-NetworksJS dist\Patent2Net64\

xcopy /S /Y dist\FusionIramuteq2 dist\Patent2Net64\
xcopy /S /Y dist\FusionPatentList2 dist\Patent2Net64\
xcopy /S /Y dist\P2N-FreePlane dist\Patent2Net64\
xcopy /S /Y dist\FormateExportDataTable dist\Patent2Net64\
xcopy /S /Y dist\FormateExportPivotTable dist\Patent2Net64\
xcopy /S /Y dist\FormateExportDataTableFamilies dist\Patent2Net64\
xcopy /S /Y dist\FormateExportBiblio dist\Patent2Net64\
xcopy /S /Y dist\FormateExportCountryCartography dist\Patent2Net64\
xcopy /S /Y dist\FusionCarrot2 dist\Patent2Net64\
xcopy /S /Y dist\Interface2 dist\Patent2Net64\
xcopy /S /Y dist\Parallel3 dist\Patent2Net64\

rmdir /S /Q dist\FormateExportAttractivityCartography
rmdir /S /Q dist\OPSGatherPatentsv2
rmdir /S /Q dist\OPSGatherContentsv2-Iramuteq
rmdir /S /Q dist\OPSGatherAugment-Families
rmdir /S /Q dist\Compatibilizer
rmdir /S /Q  dist\P2N-Networks
rmdir /S /Q  dist\P2N-PreNetworks
rmdir /S /Q  dist\P2N-NetworksJS

rmdir /S /Q dist\FusionIramuteq2
rmdir /S /Q dist\FusionPatentList2
rmdir /S /Q dist\P2N-FreePlane
rmdir /S /Q dist\FormateExportDataTable
rmdir /S /Q dist\FormateExportPivotTable
rmdir /S /Q dist\FormateExportDataTableFamilies
rmdir /S /Q dist\FormateExportBiblio
rmdir /S /Q dist\FormateExportCountryCartography
rmdir /S /Q dist\FusionCarrot2 
rmdir /S /Q dist\Interface2
rmdir /S /Q dist\Parallel3



REM xcopy /S /Y dist\P2N-FamiliesHierarc dist\Patent2Net64\

xcopy /Y root\* dist\

copy /Y requete.cql dist
copy /y cacert.pem dist\Patent2Net64\
copy /y countries.json dist\Patent2Net64
copy /y P2N.css dist\Patent2Net64
copy /y ModeleCarto.html dist\Patent2Net64
copy /y ModeleCartoDeposant.html dist\Patent2Net64
copy /y NameCountryMap.csv dist\Patent2Net64\
copy /y scriptSearch.js dist\Patent2Net64\
copy /y Searchscript.js dist\Patent2Net64\
copy /y config.js dist\Patent2Net64\
copy /y CollecteETRaite.bat dist
copy /y Modele.html dist\Patent2Net64\Modele.html
copy /y Graphe.html dist\Patent2Net64\Graphe.html
copy /y OpenNav.bat dist\Patent2Net64\OpenNav.bat
copy /y ModeleFamille.html dist\Patent2Net64\ModeleFamille.html
copy /y ModeleFamillePivot.html dist\Patent2Net64\ModeleFamillePivot.html
copy /y Pivot.html dist\Patent2Net64\Pivot.html
copy /y ModeleIndex.html dist\Patent2Net64\ModeleIndex.html
copy /y ModeleContenuIndex.html dist\Patent2Net64\ModeleContenuIndex.html
copy /y ModeleIndexRequete.html dist\Patent2Net64\
copy /y cles-epo.txt dist
mkdir dist\Patent2Net64\lib2to3
xcopy /S /Y lib2to3 dist\Patent2Net64\lib2to3
mkdir dist\Patent2Net64\extensions
mkdir dist\Patent2Net64\media
xcopy /S /Y extensions dist\Patent2Net64\extensions
xcopy /S /Y media dist\Patent2Net64\media
copy /y Process.bat
copy /y GatherProcess.bat
copy /y NetsProcess.bat
copy /y FormatingProcess.bat

