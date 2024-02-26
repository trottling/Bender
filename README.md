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
