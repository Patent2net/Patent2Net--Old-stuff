rmdir /S /Q dist\Patent2Net

pyinstaller  --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-FormateExportAttractivityCartography.txt FormateExportAttractivityCartography.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-OPSGatherPatentsv2.txt OPSGatherPatentsv2.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherContentsv2-Iramuteq.txt OPSGatherContentsv2-Iramuteq.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherAugment-Families.txt OPSGatherAugment-Families.py
REM pyinstaller -y --noupx --version-file=version-Compatibilizer.txt Compatibilizer.py

pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-Networks.txt P2N-Networks.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-PreNetworks.txt P2N-PreNetworks.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-NetworksJS.txt P2N-NetworksJS.py

pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionIramuteq2.txt FusionIramuteq2.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Fusion.txt Fusion.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-FreePlane.txt P2N-FreePlane.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTable.txt FormateExportDataTable.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportPivotTable.txt FormateExportPivotTable.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTableFamilies.txt FormateExportDataTableFamilies.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportBiblio.txt FormateExportBiblio.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportCountryCartography.txt FormateExportCountryCartography.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionCarrot2.txt FusionCarrot2.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Interface2.txt Interface2.py
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Parallel3.txt Parallel3.py


rmdir /S /Q  ..\tempocomp\FormateExportAttractivityCartography\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\OPSGatherPatentsv2\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\OPSGatherContentsv2-Iramuteq\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\OPSGatherAugment-Families\setuptools-19.2-py2.7.egg
REM rmdir /S /Q   ..\tempocomp\Compatibilizer\setuptools-19.2-py2.7.egg


rmdir /S /Q  ..\tempocomp\P2N-Networks\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\P2N-Networks\pydot_ng-1.0.1.dev0-py2.7.egg
rmdir /S /Q   ..\tempocomp\P2N-PreNetworks\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\P2N-PreNetworks\pydot_ng-1.0.1.dev0-py2.7.egg
rmdir /S /Q  ..\tempocomp\P2N-NetworksJS\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\P2N-NetworksJS\pydot_ng-1.0.1.dev0-py2.7.egg

rmdir /S /Q  ..\tempocomp\FusionIramuteq2\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\Fusion\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\P2N-FreePlane\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportDataTable\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\FormateExportPivotTable\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportDataTableFamilies\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportBiblio\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\FormateExportCountryCartography\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\FusionCarrot2\setuptools-19.2-py2.7.egg
rmdir /S /Q   ..\tempocomp\Interface2\setuptools-19.2-py2.7.egg
rmdir /S /Q  ..\tempocomp\Parallel3\setuptools-19.2-py2.7.egg


REM xcopy /S /Y ..\distribution\P2N-FamiliesHierarc ..\distribution\Patent2Net\

pyinstaller  --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-FormateExportAttractivityCartography.txt ..\specs\FormateExportAttractivityCartography.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution -y --noupx --version-file=version-OPSGatherPatentsv2.txt ..\specs\OPSGatherPatentsv2.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherContentsv2-Iramuteq.txt ..\specs\OPSGatherContentsv2-Iramuteq.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-OPSGatherAugment-Families.txt ..\specs\OPSGatherAugment-Families.spec
REM pyinstaller -y --noupx --version-file=version-Compatibilizer.txt ..\specs\Compatibilizer.spec

pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-Networks.txt ..\specs\P2N-Networks.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-PreNetworks.txt ..\specs\P2N-PreNetworks.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-NetworksJS.txt ..\specs\P2N-NetworksJS.spec

pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionIramuteq2.txt ..\specs\FusionIramuteq2.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Fusion.txt ..\specs\Fusion.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-P2N-FreePlane.txt ..\specs\P2N-FreePlane.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTable.txt ..\specs\FormateExportDataTable.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportPivotTable.txt ..\specs\FormateExportPivotTable.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportDataTableFamilies.txt ..\specs\FormateExportDataTableFamilies.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportBiblio.txt ..\specs\FormateExportBiblio.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FormateExportCountryCartography.txt ..\specs\FormateExportCountryCartography.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-FusionCarrot2.txt ..\specs\FusionCarrot2.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Interface2.txt ..\specs\Interface2.spec
pyinstaller --workpath=..\tempocomp  --specpath=..\specs --distpath=..\distribution  -y --noupx --version-file=version-Parallel3.txt ..\specs\Parallel3.spec


mkdir  ..\distribution\Patent2Net\

xcopy /S /Y ..\distribution\FormateExportAttractivityCartography ..\distribution\Patent2Net\ 
xcopy /S /Y ..\distribution\OPSGatherPatentsv2 ..\distribution\Patent2Net\ 
xcopy /S /Y ..\distribution\OPSGatherContentsv2-Iramuteq ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\OPSGatherAugment-Families ..\distribution\Patent2Net\
REM xcopy /S /Y ..\distribution\Compatibilizer ..\distribution\Patent2Net\


xcopy /S /Y ..\distribution\P2N-Networks ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\P2N-PreNetworks ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\P2N-NetworksJS ..\distribution\Patent2Net\

xcopy /S /Y ..\distribution\FusionIramuteq2 ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\Fusion ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\P2N-FreePlane ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportDataTable ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportPivotTable ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportDataTableFamilies ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportBiblio ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FormateExportCountryCartography ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\FusionCarrot2 ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\Interface2 ..\distribution\Patent2Net\
xcopy /S /Y ..\distribution\Parallel3 ..\distribution\Patent2Net\


REM xcopy /S /Y ..\distribution\P2N-FamiliesHierarc ..\distribution\Patent2Net\

xcopy /Y root\* ..\distribution\

copy /y cacert.pem ..\distribution\Patent2Net\
copy /y countries.json ..\distribution\patent2Net
copy /y P2N.css ..\distribution\patent2Net
copy /y ModeleCarto.html ..\distribution\patent2Net
copy /y ModeleCartoDeposant.html ..\distribution\patent2Net
copy /y NameCountryMap.csv ..\distribution\Patent2Net\
copy /y scriptSearch.js ..\distribution\Patent2Net\
copy /y Searchscript.js ..\distribution\Patent2Net\
copy /y config.js ..\distribution\Patent2Net\
copy /y CollecteETRaite.bat dist
copy /y Modele.html ..\distribution\Patent2Net\Modele.html
copy /y Graphe.html ..\distribution\Patent2Net\Graphe.html
copy /y OpenNav.bat ..\distribution\Patent2Net\OpenNav.bat
copy /y ModeleFamille.html ..\distribution\Patent2Net\ModeleFamille.html
copy /y ModeleFamillePivot.html ..\distribution\Patent2Net\ModeleFamillePivot.html
copy /y Pivot.html ..\distribution\Patent2Net\Pivot.html
copy /y ModeleIndex.html ..\distribution\Patent2Net\ModeleIndex.html
copy /y ModeleContenuIndex.html ..\distribution\Patent2Net\ModeleContenuIndex.html
copy /y ModeleIndexRequete.html ..\distribution\Patent2Net\
copy /y cles-epo.txt dist
mkdir ..\distribution\Patent2Net\lib2to3
xcopy /S /Y lib2to3 ..\distribution\Patent2Net\lib2to3
mkdir ..\distribution\Patent2Net\extensions
mkdir ..\distribution\Patent2Net\media
xcopy /S /Y extensions ..\distribution\Patent2Net\extensions
xcopy /S /Y media ..\distribution\Patent2Net\media
