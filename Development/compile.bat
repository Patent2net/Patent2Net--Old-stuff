rmdir /S /Q dist\Patent2Net
pyinstaller -y OPSGatherPatentsv2.py
pyinstaller -y OPSGatherContentsv1-Iramuteq.py
pyinstaller -y OPSGatherAugment-Families.py
pyinstaller -y P2N-Authors.py
pyinstaller -y P2N-AuthorsApplicants.py
pyinstaller -y P2N-CrossTech.py
pyinstaller -y P2N-CountryCrossTech.py
pyinstaller -y P2N-InventorCrossTech.py
pyinstaller -y P2N-Applicants.py
pyinstaller -y P2N-ApplicantsCrossTech.py
pyinstaller -y OPSGatherAugment-Families.py
pyinstaller -y P2N-Families.py
pyinstaller -y P2N-FamiliesHierarc.py
pyinstaller -y FusionIramuteq.py
pyinstaller -y Fusion.py
pyinstaller -y P2N-V5.py
pyinstaller -y FormateExport.py
pyinstaller -y FormateExportFamilies.py
pyinstaller -y CartographyCountry.py
pyinstaller -y Interface.py
pyinstaller -y Interface2.py
pyinstaller -y OPSGatherPatentsv2.spec
pyinstaller -y OPSGatherContentsv1-Iramuteq.spec
pyinstaller -y OPSGatherAugment-Families.spec
pyinstaller -y P2N-Authors.spec
pyinstaller -y P2N-AuthorsApplicants.spec
pyinstaller -y P2N-Applicants.spec
pyinstaller -y P2N-ApplicantsCrossTech.spec
pyinstaller -y P2N-CrossTech.spec
pyinstaller -y CartographyCountry.spec
pyinstaller -y P2N-CountryCrossTech.spec
pyinstaller -y P2N-InventorCrossTech.spec
pyinstaller -y P2N-Families.spec
pyinstaller -y FusionIramuteq.spec
pyinstaller -y FormateExport.spec
pyinstaller -y FormateExportFamilies.spec
pyinstaller -y P2N-V5.spec
pyinstaller -y Fusion.spec
pyinstaller -y P2N-FamiliesHierarc.spec
pyinstaller -y Interface.spec
pyinstaller -y Interface2.spec
mkdir dist\Patent2Net\
copy /Y requete.cql dist
copy /y cacert.pem dist\Patent2Net\
copy /y countries.json dist\patent2Net
copy /y ModeleCarto.html dist\patent2Net
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
xcopy /S /Y dist\OPSGatherPatentsv2 dist\Patent2Net\ 
xcopy /S /Y dist\P2N-FamiliesHierarc dist\Patent2Net\
xcopy /S /Y dist\OPSGatherContentsv1-Iramuteq dist\Patent2Net\
xcopy /S /Y dist\OPSGatherAugment-Families dist\Patent2Net\
xcopy /S /Y dist\P2N-Authors dist\Patent2Net\
xcopy /S /Y dist\P2N-AuthorsApplicants dist\Patent2Net\
xcopy /S /Y dist\P2N-Applicants dist\Patent2Net\
xcopy /S /Y dist\P2N-ApplicantsCrossTech dist\Patent2Net\
xcopy /S /Y dist\P2N-CountryCrossTech dist\Patent2Net\
xcopy /S /Y dist\P2N-CrossTech dist\Patent2Net\
xcopy /S /Y dist\P2N-InventorCrossTech dist\Patent2Net\
xcopy /S /Y dist\OPSGatherAugment-Families dist\Patent2Net\
xcopy /S /Y dist\P2N-Families dist\Patent2Net\
xcopy /S /Y dist\FusionIramuteq dist\Patent2Net\
xcopy /S /Y dist\FormateExport dist\Patent2Net\
xcopy /S /Y dist\FormateExportFamilies dist\Patent2Net\
xcopy /S /Y dist\Fusion dist\Patent2Net\
xcopy /S /Y dist\P2N-V5 dist\Patent2Net\
xcopy /S /Y dist\CartographyCountry dist\Patent2Net\
xcopy /S /Y dist\Interface dist\Patent2Net\
xcopy /S /Y dist\Interface2 dist\Patent2Net\
mkdir dist\Patent2Net\extensions
mkdir dist\Patent2Net\media
xcopy /S /Y extensions dist\Patent2Net\extensions
xcopy /S /Y media dist\Patent2Net\media
rmdir /S /Q dist\OPSGatherPatentsv2
rmdir /S /Q dist\OPSGatherContentsv1-Iramuteq
rmdir /S /Q dist\P2N-Authors
rmdir /S /Q dist\P2N-AuthorsApplicants
rmdir /S /Q dist\P2N-Applicants
rmdir /S /Q dist\P2N-ApplicantsCrossTech
rmdir /S /Q dist\P2N-CountryCrossTech
rmdir /S /Q dist\P2N-CrossTech
rmdir /S /Q dist\P2N-InventorCrossTech
rmdir /S /Q dist\OPSGatherAugment-Families
rmdir /S /Q dist\P2N-Families
rmdir /S /Q dist\FusionIramuteq
rmdir /S /Q dist\Fusion
rmdir /S /Q dist\P2N-V5
rmdir /S /Q dist\FormateExport
rmdir /S /Q dist\FormateExportFamilies
rmdir /S /Q dist\P2N-FamiliesHierarc
rmdir /S /Q dist\CartographyCountry
rmdir /S /Q dist\Interface
rmdir /S /Q dist\Interface2