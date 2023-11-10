# WinapiExport
WinapiExport - is a small utility designed to extract the names of system libraries and 
their functions from a directory in C:\\Windows\\System32 either of ListDlls.py saved in json format.
This script can help researchers in the field of reverse engineering.
```
 __      ___        _   ___ ___ ___                   _
 \ \    / (_)_ _   /_\ | _ \_ _| __|_ ___ __  ___ _ _| |_        _.-;;-._
  \ \/\/ /| | ' \ / _ \|  _/| || _|\ \ / '_ \/ _ \ '_|  _|'-..-'|   ||   |
   \_/\_/ |_|_||_/_/ \_\_| |___|___/_\_\ .__/\___/_|  \__|'-..-'|_.-;;-._|
                                       |_|                '-..-'|   ||   |
                                                          '-..-'|_.-''-._|

usage: winapi_export.py -h

Utility for importing dll names and function
names from the dll export table to json format.

options:
  -h, --help          show this help message and exit
  -all_fe [ALL_FE]    Import all function names from dll by (default) path C:\Windows\System32.
  -base_fe [BASE_FE]  Importing function names only from base dlls specified in ListDlls.py.
  -all_de [ALL_DE]    Import only dll names by (default) path C:\Windows\System32.
  -base_de [BASE_DE]  Import only the base dll names specified in ListDlls.py.
```
Example:
```
python winapi_export.py -all_fe
```
![cmdwinapiexport](https://github.com/d0x65viant/Images/blob/main/winapiexport2.png)

The result of the script is saved in a json file.

![resultjson](https://github.com/d0x65viant/Images/blob/main/res.png)

The contents of the json file looks like this.
<p align="center">
<img width=800, src="https://github.com/d0x65viant/Images/blob/main/resfuncjson.png">
</p>
