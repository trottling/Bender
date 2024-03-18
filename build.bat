echo Setup packages
pip install -r requirements.txt

echo Building
pyinstaller --name "Bender" --clean --onefile --noconsole --uac-admin --hiddenimport win32timezone --add-data "assets\gifs\*.*:assets\gifs" --add-data "assets\qss\*.*:assets\qss" --add-data "assets\icons\*.*:assets\icons"--add-data "assets\images\*.*:assets\images" --add-data "assets\app.ui:assets" --paths C:\Windows\System32\downlevel --icon ".\assets\icons\bender.ico" main.py
move "dist\main.exe" "main.exe"

del main.spec