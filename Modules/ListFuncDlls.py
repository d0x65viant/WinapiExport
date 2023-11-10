import time
import json
import os
import pefile
import concurrent.futures
from multiprocessing    import Manager
from Modules.Progress   import Progress
from Modules.ListDlls   import get_dllsys32
from Modules.SplitArray import split_array_into_tuples

def get_all_funcsystdlls(dllnames_list, bar, dct):
    Dir_Dlls = "C:\\Windows\\System32"

    for dllname in dllnames_list:
        exports_list = []
        pe = pefile.PE(Dir_Dlls + "\\" + dllname)
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            try:
                exports_list.append(exp.name.decode('utf-8'))
            except:
                continue

        dct[dllname] = exports_list

        bar.next()


def multiproc_jsonfuncnames(dllnames_list, funcnames_json, bar):
    with concurrent.futures.ProcessPoolExecutor(max_workers = 4) as executor:
        future_proc = [executor.submit(
        get_all_funcsystdlls, names_tuple, bar, funcnames_json
        )for names_tuple in dllnames_list]
        
        for future in concurrent.futures.as_completed(future_proc):
            future.cancel()


def get_funcsys32(
    base_expts = False, 
    update = False, 
    dir_dlls = "C:\\Windows\\System32"):

    # Список имен модулей с таблицей экспорта.
    dlls = [dll for dll in 
    get_dllsys32(
    base_expts=base_expts, update=update, dir_dlls=dir_dlls)]
    
    json_funcnames = Manager().dict()
    Manager().register('Progress', Progress)

    types_json = {base_expts: "based_func_names.json",
              not base_expts: "func_names.json"}

    dllsnames_tupllist = split_array_into_tuples(dlls, len(dlls)//30)
    json_exist = os.path.exists(types_json[True])
    bar = Manager().Progress(len(dlls))

    if  json_exist:
        try:
            with open(types_json[True]) as file:
                json_funcnames = json.load(file)
        
        except json.decoder.JSONDecodeError:
            json_exist = False

    if  not json_exist or update:
        mes = {not json_exist: f"[+] create {types_json[True]}",
                   update:     f"[+] updating data for {types_json[True]}"}

        print(mes[True])

        gen_names = multiproc_jsonfuncnames(
        dllsnames_tupllist, json_funcnames, bar)

        with open(f"{types_json[True]}", "w") as file:
            file.write(json.dumps(json_funcnames.copy(), indent=2))

    return json_funcnames.copy()

    

def main():
    json_funcnames = get_funcsys32(base_expts=True, update=False)
    for key in json_funcnames:
        print(key, end=", ")
    

if __name__ == '__main__':
    main()
