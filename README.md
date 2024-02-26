Writing a README.md in progress....
# Bender - Windows Vulnerability Scanner

<div align="center">
  <img src="https://raw.githubusercontent.com/trottling/Bender/main/media/bender.png" width="200"/>
</div>

Simple and portable app to search for vulnerabilities Windows system with pretty UI written in Python

### Requirements
- Windows 8* and newer
- That's all!

> *Required by PyQT6 library

## Features

- Scan installed system and user apps for CVEs
- Scan drivers in C:\windows\system32\drivers for vulns
- Save report for each scan


## Current supported vulnerability databases for scanning

### Installed Apps
- vulners.com

### Drivers
- loldrivers.io

## Scan functios
Scan installed system and user apps for CVEs
GIF

Scan drivers
GIF

## Tech

Bender uses a number of open source projects to work properly:

- [PyQT6] - Great UI with animatios and themes
- [windows_tools] - Collection of various interfaces for Windows functionality
- [httpx] - A next-generation HTTP client
- [vulners] - Vulners.com API v3 Python wrapper
- [darkdetect] - Detect OS Dark Mode from Python

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
    
   [PyQT6]: <https://doc.qt.io/qtforpython-6/>
   [windows_tools]: <https://github.com/netinvent/windows_tools>
   [httpx]: <https://www.python-httpx.org/>
   [vulners]: <https://pypi.org/project/vulners/>
   [darkdetect]: <https://github.com/albertosottile/darkdetect>
