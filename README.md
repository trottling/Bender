[![OS - Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows&logoColor=white)](https://www.microsoft.com/")
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MIT](https://img.shields.io/github/license/trottling/Bender)](https://github.com/trottling/Bender?tab=MIT-1-ov-file#)
[![Commits](https://img.shields.io/github/commit-activity/m/trottling/Bender)](https://github.com/trottling/Bender/commits/main/)
[![Downloads](https://img.shields.io/github/downloads/trottling/Bender/total)](https://github.com/trottling/Bender/releases/latest)
[![Last release](https://img.shields.io/github/v/release/trottling/Bender)](https://github.com/trottling/Bender/releases/latest)

# Bender - Windows Vulnerability Scanner

<div align="center">
  <img src="https://raw.githubusercontent.com/trottling/Bender/main/media/bender.png" width="200"/>
</div>

**Simple and portable app for search vulnerabilities in Windows system with pretty UI, written in Python 3.12**
> **NOTE**
> This application is designed for scan ONLY YOUR PC. The author is not responsible for illegal actions in which Bender was used.
> Also, Bender is Free Open Source Software project, that does not conduct any commercial activities. 

![START](https://raw.githubusercontent.com/trottling/Bender/main/media/start.png)

## Table of contents
1. [Requirements](https://github.com/trottling/Bender?tab=readme-ov-file#requirements)
2. [How to install](https://github.com/trottling/Bender?tab=readme-ov-file#how-to-install)
3. [Features](https://github.com/trottling/Bender?tab=readme-ov-file#features)
4. [Scan functios](https://github.com/trottling/Bender?tab=readme-ov-file#scan-functios)
5. [Tech](https://github.com/trottling/Bender?tab=readme-ov-file#tech)
6. [Current supported vulnerability databases for scanning](https://github.com/trottling/Bender?tab=readme-ov-file#current-supported-vulnerability-databases-for-scanning)
7. [TODO](https://github.com/trottling/Bender?tab=readme-ov-file#todo)
8. [How can I help this project?](https://github.com/trottling/Bender?tab=readme-ov-file#how-can-i-help-this-project)
9. [Run or Build from source](https://github.com/trottling/Bender/edit/main/README.md#run-or-build-from-source)

## Requirements
- Windows 8* and newer
- That's all!  

> *Required by PyQT6 library and limited to avoid errors when using system calls from older versions of Windows

## How to install
1. Download [latest build](https://github.com/trottling/Bender/releases/latest)
2. Add to antivirus exclusion if you get messages about Bender.exe, see [first TODO message](https://github.com/trottling/Bender#todo)
3. Run as Admin
4. Done!

## Features

- Scan installed system and user apps for CVEs
- Scan drivers in C:\windows\system32\drivers for vulns
- Save report for each scan

## Scan functios
- Scan installed system and user apps for CVEs

![CIA](https://github.com/trottling/Bender/blob/main/media/CIA.gif?raw=true)

- Scan drivers for vulnerabilities

![CCD](https://github.com/trottling/Bender/blob/main/media/CCD.gif?raw=true)


## Tech

Bender uses a number of open source projects to work properly:

- [PyQT6] - Great UI with animatios and themes
- [windows_tools] - Collection of various interfaces for Windows functionality
- [httpx] - A next-generation HTTP client
- [vulners] - Vulners.com API v3 Python wrapper
- [darkdetect] - Detect OS Dark Mode from Python

## Current supported vulnerability databases for scanning

- Installed Apps
  
| Database | Api key | Key retrieval | Notes |
| ------ | ------ | ------ | ------ |
| vulners.com | Required | [Easy](https://vulners.com/docs/apikey/) | Select "API" on step 3 | 

- Drivers
  
| Database | Api key | Key retrieval | Notes |
| ------ | ------ | ------ | ------ |
| loldrivers.io | No needed | - | - |

## TODO
- Do something about the false antivirus message about Bender.exe
> Thanks to detects on any build through pyinstaller because of schoolchildren writing RATs and Miners in Python
- Make UI adaptive and resizeble
- Add local network scanning
- Add Windows KB CVE scanner 
- Add more DB to scanners
- Add translate

## How can I help this project?
- First, look at [TODO list](https://github.com/trottling/Bender/tree/main#todo)
- If you have ideas for tweaks, write me in the [Telegram](https://t.me/trottling) or open a [new issue](https://github.com/trottling/Bender/issues/new/choose)
- Research FREE vulnerability databases with API, like vulners.com or vulmon.com (They doesn't have API docs)

## Run or Build from source
1. Clone or [Download](https://github.com/trottling/Bender/archive/refs/heads/main.zip) source code
> git clone https://github.com/trottling/Bender/tree/main
2. Go to source code folder
> cd Bender
3. Install requirements
> pip install -r requirements.txt
4. Run
> python main.py
5. Build
> build.bat

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
    
   [PyQT6]: <https://doc.qt.io/qtforpython-6/>
   [windows_tools]: <https://github.com/netinvent/windows_tools>
   [httpx]: <https://www.python-httpx.org/>
   [vulners]: <https://pypi.org/project/vulners/>
   [darkdetect]: <https://github.com/albertosottile/darkdetect>
