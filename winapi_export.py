import os
import argparse
from Modules.ListDlls     import get_dllsys32
from Modules.ListFuncDlls import get_funcsys32
from argparse import RawTextHelpFormatter

logo = r"""
 __      ___        _   ___ ___ ___                   _   
 \ \    / (_)_ _   /_\ | _ \_ _| __|_ ___ __  ___ _ _| |_        _.-;;-._
  \ \/\/ /| | ' \ / _ \|  _/| || _|\ \ / '_ \/ _ \ '_|  _|'-..-'|   ||   |
   \_/\_/ |_|_||_/_/ \_\_| |___|___/_\_\ .__/\___/_|  \__|'-..-'|_.-;;-._|
                                       |_|                '-..-'|   ||   |
                                                          '-..-'|_.-''-._|
"""

parser = argparse.ArgumentParser(usage=f"{os.path.basename(__file__)} -h",
description=f"Utility for importing dll names and function "
			"\nnames from the dll export table to json format.", 
			formatter_class=RawTextHelpFormatter)

parser.add_argument("-all_fe",   nargs="?", const=True,  help="Import all function names from dll by (default) path C:\\Windows\\System32.")
parser.add_argument("-base_fe",  nargs="?", const=True,  help="Importing function names only from base dlls specified in ListDlls.py.")
parser.add_argument("-all_de",   nargs="?", const=True,  help="Import only dll names by (default) path C:\\Windows\\System32.")
parser.add_argument("-base_de",  nargs="?", const=True,  help="Import only the base dll names specified in ListDlls.py.")


def main():
	print(logo)
	args  = parser.parse_args()
	calls = (
	(args.all_fe,  get_funcsys32, (False, True)),
	(args.base_fe, get_funcsys32, (True,  True)),
	(args.all_de,  get_dllsys32,  (False, True)),
	(args.base_de, get_dllsys32,  (True,  True)), 
	)

	for clltpl in calls:
		if clltpl[0]:
			clltpl[1](*clltpl[2])
	

if __name__ == '__main__':
	main()