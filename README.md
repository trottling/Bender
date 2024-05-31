[![OS - Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows&logoColor=white)](https://www.microsoft.com/")
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MIT](https://img.shields.io/github/license/trottling/Bender)](https://github.com/trottling/Bender?tab=MIT-1-ov-file#)
[![Commits](https://img.shields.io/github/commit-activity/m/trottling/Bender)](https://github.com/trottling/Bender/commits/main/)
[![Downloads](https://img.shields.io/github/downloads/trottling/Bender/total)](https://github.com/trottling/Bender/releases/latest)
[![Last release](https://img.shields.io/github/v/release/trottling/Bender)](https://github.com/trottling/Bender/releases/latest)

EN | [RU](https://github.com/trottling/Bender/blob/main/.docs/RU/README.md)

# Bender - Windows Vulnerability Scanner

<div align="center">
  <img alt="page" src="https://raw.githubusercontent.com/trottling/Bender/main/media/bender.png" width="200"/>
</div>

**Simple and portable app for search vulnerabilities in Windows system with pretty UI, written in Python 3.12** (earlier versions are also supported)  

**Many thanks to vulners.com for supporting the project!**
> **NOTE**
>  
> This application is designed to scan ONLY YOUR PC. The author is not responsible for illegal actions in which Bender was used.
> 
> Bender is a Free Open Source Software project that does not conduct any commercial activities.
>
> Bender performs ONLY READING ONLY system files, folder or registry.

![START](https://raw.githubusercontent.com/trottling/Bender/main/media/start.png)

## Table of contents
1. [Requirements](#requirements)
2. [How to install](#how-to-install)
3. [Features](#features)
4. [Scan report example](#scan-report-example)
5. [Tech](#tech)
6. [Current supported vulnerability databases](#current-used-vulnerability-databases)
7. [TODO](#todo)
8. [How can I help this project?](#how-can-i-help-this-project)
9. [Run or Build from source](#run-or-build-from-source)

## Requirements
- Windows 8, 8.1, 10 or 11 and newer*
- Admin privileges for access to system info
- That's all!  
> *Required by PyQT6 library and limited to avoid errors when using system calls from older versions of Windows

## How to install
1. Download [latest build](https://github.com/trottling/Bender/releases/latest)
2. Get Vulners.com API key, see [help page](https://github.com/trottling/Bender/blob/main/VULNERS-API-KEY-HELP.md)
3. Add to antivirus exclusion if you get messages about Bender.exe
  > This happens because pyinstaller unzips files and the python interpreter in the temp folder, so antiviruses don't like such programs
4. Run as Admin
5. Done!


## Features

- Scan installed system and user apps for CVEs
- Scan drivers in C:\windows\system32\drivers for vulnerabilities
- Scan installed Windows KB for CVEs
- Scan Local and External ports
- Scan common system information
- Save report as image

## Scan report example
![image](https://raw.githubusercontent.com/trottling/Bender/main/media/scan_result.png)

## Tech

| Project Part          | Autor(s)        | Desc                                                         |
|-----------------------|-----------------|--------------------------------------------------------------|
| Pretty Icons          | icons8.com      | Curated graphics, design apps, and AI tools                  |
| StyleSheets           | [GTRONICK/QSS]  | QT Style Sheets templates                                    |
| CVE Info DB Api       | [mitre.org]     | Solving Problems for a Safer World                           |
| Vulnerable drivers DB | [loldrivers.io] | curated list of all abused Windows drivers                   |
| GUI                   | [PyQT6]         | official Python bindings for Qt                              |
| Dark theme detect     | [darkdetect]    | Detect OS Dark Mode from Python                              |
| Network               | [httpx]         | A next-generation HTTP client                                |
| Windows interactions  | [windows_tools] | Collection of various interfaces for Windows functionality   |
| Vulners.com API       | [vulners]       | Vulners.com API v3 Python wrapper                            |
| HW Info               | [cpuinfo]       | A module for getting CPU info with pure Python               |
| MAC adress            | [getmac]        | Platform-independent pure-Python module to get a MAC address |
| Port scanner          | [PortScan]      | command line port scan utility written in python             |

## Current used vulnerability databases
  
- vulners.com
- loldrivers.io

## TODO
- As long as it's empty

## How can I help this project?
- First, look at [TODO list](#todo)
- If you have ideas for tweaks, write me in the [Telegram](https://t.me/trottling) or open a [new issue](https://github.com/trottling/Bender/issues/new/choose)
- Research-FREE vulnerability databases with API, like vulners.com or vulmon.com (They don't have API docs)

## Run or Build from source
1. Clone or [Download](https://github.com/trottling/Bender/archive/refs/heads/main.zip) source code
`git clone https://github.com/trottling/Bender/tree/main`
2. Go to source code folder
`cd Bender`
3. Install requirements
`pip install -r requirements.txt`
- Run
`python main.py`
- Build
`build.bat`

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
    
   [PyQT6]: <https://doc.qt.io/qtforpython-6/>
   [windows_tools]: <https://github.com/netinvent/windows_tools>
   [httpx]: <https://www.python-httpx.org/>
   [vulners]: <https://pypi.org/project/vulners/>
   [darkdetect]: <https://github.com/albertosottile/darkdetect>
   [GTRONICK/QSS]: <github.com/GTRONICK/QSS>
   [mitre.org]: <mitre.org>
   [loldrivers.io]: <loldrivers.io>
   [cpuinfo]: <https://github.com/workhorsy/py-cpuinfo>
   [getmac]: <https://github.com/GhostofGoes/getmac>
   [PortScan]: <https://github.com/Aperocky/PortScan>
