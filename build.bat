echo Setup packages
pip install -r requirements.txt

echo Building
pyinstaller --name "Bender" --clean --onefile --noconsole --uac-admin --hiddenimport win32timezone --upx-dir "upx-4.2.2-win64" --add-data "assets\gifs\*.*:assets\gifs" --add-data "assets\qss\*.*:assets\qss" --add-data "assets\icons\*.*:assets\icons"--add-data "assets\images\*.*:assets\images" --add-data "assets\ui\*.*:ui" --paths C:\Windows\System32\downlevel --icon ".\assets\icons\bender.ico" --upx-exclude "api-ms-win-*.dll" --upx-exclude "_uuid.pyd" --upx-exclude "python3.dll" main.py
move "dist\Bender.exe" "Bender.exe"

del main.spec