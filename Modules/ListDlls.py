import time
import os
import pefile
import json
import concurrent.futures as pool
from typing import List, Dict, Generator
from multiprocessing          import Manager, Value
from multiprocessing.managers import ListProxy, ValueProxy, AutoProxy
from Modules.Progress   import Progress
from Modules.SplitArray import split_array_into_tuples

def get_basedmods_tblexpts():
    Based_Dlls = [
    "kernel32.dll", "comctl32.dll", "advapi32.dll", "comdlg32.dll",
    "gdi32.dll",    "msvcrt.dll",   "netapi32.dll", "ntdll.dll",
    "ntoskrnl.exe", "oleaut32.dll", "psapi.dll",    "shell32.dll",
    "shlwapi.dll",  "urlmon.dll",   "user32.dll",   "winhttp.dll",  
    "ws2_32.dll",   "wship6.dll",   "advpack.dll", ]

    return Based_Dlls

def get_dlls(
    filename_list: List[str], 
    dllnames_list: ListProxy, 
    bar: AutoProxy, 
    dir_dlls: str):

    for filename in filename_list:
        try:
            pe = pefile.PE(dir_dlls + "\\" + filename)
            if  hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
                dllnames_list.append(filename)

            bar.next()       
        
        except:
            bar.next()
            continue


def multproc_listdllnames(
    files:    List[tuple[str]], 
    dllnames: ListProxy, 
    bar:      AutoProxy,
    dir_dlls: str):

    with pool.ProcessPoolExecutor(max_workers = 4) as executor:
        future_proc = [executor.submit(
        get_dlls, filenames, dllnames, bar, dir_dlls
        )for filenames in files]
        pool.wait(future_proc)


def get_dllsys32(
    base_expts: bool = False, 
    update:     bool = False, 
    dir_dlls:   str  = "C:\\Windows\\System32") -> Generator:

    dllnames_json: Dict[str, List[str]] = None
    all_files:     List[str] = os.listdir(dir_dlls)
    based_files:   List[str] = get_basedmods_tblexpts()
    dllnames_list: ListProxy = Manager().list()
    codlls: ValueProxy = Manager().Value('codlls', 0)
    Manager().register('Progress', Progress)
    
    types_json = {
    base_expts:     ("based_dll_names.json", based_files),
    not base_expts: ("dll_names.json",         all_files)}
    
    files_tupllist: List[tuple] = split_array_into_tuples(
    types_json[True][1], 
    len(types_json[True][1])//30)

    json_exist: bool = os.path.exists(types_json[True][0])
    bar:   AutoProxy = Manager().Progress(len(types_json[True][1]))
    
    #------------------------------------------------------------------------------
    if  json_exist:
        try:
            with open(types_json[True][0]) as file:
                dllnames_json: dict = json.load(file)
        
        except json.decoder.JSONDecodeError:
            json_exist = False

    if  not json_exist or update:
        mes = {
        not json_exist: f"[+] create {types_json[True][0]}",
            update:     f"[+] updating data for {types_json[True][0]}"}
        
        print(mes[True])

        multproc_listdllnames(
        files_tupllist, 
        dllnames_list, 
        bar, dir_dlls)

        dllnames_json = {"DLL_Names": dllnames_list[:]}
        with open(f"{types_json[True][0]}", "w") as file:
            file.write(json.dumps(dllnames_json, indent=2))


        print(f"[+] found {len(dllnames_json['DLL_Names'])} modules with"
        f" export table from {len(types_json[True][1])}.")

    yield from dllnames_json["DLL_Names"]


def main():
    # Тестирование.
    gen = [i for i in get_dllsys32(base_expts=True, update=True)]

if __name__ == "__main__":
    main()