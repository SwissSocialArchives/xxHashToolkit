# xxHashTool

xxHash3 64 validieren


## Installation

Es wird empfohlen, die Installation via setuptools auszuführen. Damit ist sichergestellt, 
dass alle benötigten Drittkomponenten mit installiert werden, ausserdem werden Konsolen-Skripte
eingerichtet, die sich bequem von jedem Ort her ausführen lassen.
<br>
<br>
Anleitung (für Windows beachten: Eingabeaufforderung _als Administrator_ ausführen!):
https://packaging.python.org/tutorials/installing-packages/

```pip install -e .```
<br>
installiert Skripte und alle benötigten Bibliotheken im Stammverzeichnis

Farben für Windows:

```
reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f
```

Siehe auch: https://www.codeproject.com/Tips/5255355/How-to-Put-Color-on-Windows-Console

## Command line scripts:
<br>

```xx_validate [--flags]```
<br>
validiert xxHash3 64-Checksummen (Dateiname: 'manifest-cache-xxh364.txt')


<br>
<br>

```path```
<br>
Als erstes Argument muss der Quellordner angegeben werden.<br>
<br>
 Beispiel:<br>
xx_validate /Volumes/Example/xxHashTest
<br>
<br>

## Linksammlung

* https://github.com/Cyan4973/xxHash
