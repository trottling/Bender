echo Setup packages
pip install -r requirements.txt

echo Building --noconsole
pyinstaller --name "Bender" --clean --onefile --noupx --uac-admin --add-data "assets\qss\*.*:assets\qss" --add-data "assets\icons\*.*:assets\icons"--add-data "assets\images\*.*:assets\images" --add-data "assets\app.ui:assets" --paths C:\Windows\System32\downlevel --icon ".\assets\icons\bender.ico" main.py
move "dist\main.exe" "main.exe"

del main.spec