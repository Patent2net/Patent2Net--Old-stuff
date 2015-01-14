pyinstaller -y OPSGatherPatentsv2.py
pyinstaller -y OPSGatherContentsv1-Iramuteq.py
pyinstaller -y OPSGatherAugment-Families.py
pyinstaller -y P2N-Authors.py
pyinstaller -y P2N-AuthorsApplicants.py
pyinstaller -y P2N-CountryCrossTech.py
pyinstaller -y P2N-InventorCrossTech.py
pyinstaller -y OPSGatherAugment-Families.py
pyinstaller -y P2N-Families.py
pyinstaller -y P2N-FamiliesHierarc.py
pyinstaller -y FusionIramuteq.py
pyinstaller -y Fusion.py
pyinstaller -y P2N-V5.py
pyinstaller -y FormateExport.py
pyinstaller -y FormateExportFamilies.py
pyinstaller -y OPSGatherPatentsv2.spec
pyinstaller -y OPSGatherContentsv1-Iramuteq.spec
pyinstaller -y OPSGatherAugment-Families.spec
pyinstaller -y P2N-Authors.spec
pyinstaller -y P2N-AuthorsApplicants.spec
pyinstaller -y P2N-CountryCrossTech.spec
pyinstaller -y P2N-InventorCrossTech.spec
pyinstaller -y P2N-Families.spec
pyinstaller -y FusionIramuteq.spec
pyinstaller -y FormateExport.spec
pyinstaller -y FormateExportFamilies.spec
pyinstaller -y P2N-V5.spec
pyinstaller -y Fusion.spec
pyinstaller -y P2N-FamiliesHierarc.spec
xcopy dist\OPSGatherPatentsv2 dist\Patent2Net\ /S /Y 
xcopy /Y requete.cql dist
mkdir dist\Patent2Net\
xcopy /y cacert.pem dist\Patent2Net\
xcopy /S /Y dist\P2N-FamiliesHierarc dist\Patent2Net\
xcopy /S /Y dist\OPSGatherContentsv1-Iramuteq dist\Patent2Net\
xcopy /S /Y dist\OPSGatherAugment-Families dist\Patent2Net\
xcopy /S /Y dist\P2N-Authors dist\Patent2Net\
xcopy /S /Y dist\P2N-AuthorsApplicants dist\Patent2Net\
xcopy /S /Y dist\P2N-CountryCrossTech dist\Patent2Net\
xcopy /S /Y dist\P2N-InventorCrossTech dist\Patent2Net\
xcopy /S /Y dist\OPSGatherAugment-Families dist\Patent2Net\
xcopy /S /Y dist\P2N-Families dist\Patent2Net\
xcopy /S /Y dist\FusionIramuteq dist\Patent2Net\
xcopy /S /Y dist\FormateExport dist\Patent2Net\
xcopy /S /Y dist\FormateExportFamilies dist\Patent2Net\
xcopy /S /Y dist\Fusion dist\Patent2Net\
xcopy /S /Y dist\P2N-V5 dist\Patent2Net\
mkdir dist\Patent2Net\extensions
mkdir dist\Patent2Net\media
xcopy /y ModeleDist.html dist\Patent2Net\Modele.html
xcopy /y ModeleFamilleDist.html dist\Patent2Net\ModeleFamille.html
xcopy /y PivotDist.html dist\Patent2Net\Pivot.html

xcopy /y cles-epo.txt dist
xcopy /S /Y extensions dist\Patent2Net\extensions
xcopy /S /Y media dist\Patent2Net\media
rmdir /S /Q dist\OPSGatherPatentsv2
rmdir /S /Q dist\OPSGatherContentsv1-Iramuteq
rmdir /S /Q dist\P2N-Authors
rmdir /S /Q dist\P2N-AuthorsApplicants
rmdir /S /Q dist\P2N-CountryCrossTech
rmdir /S /Q dist\P2N-InventorCrossTech
rmdir /S /Q dist\OPSGatherAugment-Families
rmdir /S /Q dist\P2N-Families
rmdir /S /Q dist\FusionIramuteq
rmdir /S /Q dist\Fusion
rmdir /S /Q dist\P2N-V5
rmdir /S /Q dist\FormateExport
rmdir /S /Q dist\FormateExportFamilies
rmdir /S /Q dist\P2N-FamiliesHierarc