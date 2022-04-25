import shutil
import sys
import os.path
import yaml

#TODO: change active project
project = "somthing-else"

def which_path():
    #check if os is linux
    if(sys.platform in ("linux", "linux2")):
        path = "~/.config/gridscale"
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            os.makedirs(path)
    #check if os is windows
    elif(sys.platform in ("win32", "cygwin", "msys")):
        path = "%APPDATA%\gridscale"
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            os.makedirs(path)
    #check if os is mac os
    elif(sys.platform in ("darwin", "os2", "os2emx")):
        path = "~/Library/Application Support/gridscale"
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        print("Operating System not supported")

    return path

def create_config(path):
    cwd = os.getcwd()
    shutil.copyfile(f"{cwd}/config.yaml", syspath)
    print(f"New config file created, edit config file at: {syspath}")

def load_config(path):
    syspath = which_path() + "/config.yaml"

    if not os.path.exists(syspath):
        create_config(syspath)

    with open(f"{syspath}", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            #return list of dictionaries for all projects
            for value in data.values():
                return(value)

        except yaml.YAMLError as exc:
            print(exc)
