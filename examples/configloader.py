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
        "Operating System not supported"

    return path

def create_config(path):
    cwd = os.getcwd()
    shutil.copyfile(f"{cwd}/config.yaml", path)
    print(f"New config file created, edit config file at: {path}")

def load_config(projectname, goal, path):
    with open(f"{path}", 'r') as stream:
        try:
            data = yaml.safe_load(stream)

            for value in data.values():
                for x in range(len(value)):
                    result = value[x]
                    #returns userID and token for the selected project
                    if (result.get("name") == projectname):
                        userid = result.get("userId")
                        token = result.get("token")
        except yaml.YAMLError as exc:
            print(exc)

    if(goal == "id"):
        return userid
    elif(goal == "token"):
        return token

def load_token(project):
    syspath = which_path() + "/config.yaml"
    goal = "token"

    # check if config file exists
    if not os.path.exists(syspath):
        create_config(syspath)
        return load_config(project, goal, syspath)
    else:
        return load_config(project, goal, syspath)


def load_userid(project):
    syspath = which_path() + "/config.yaml"
    goal = "id"

    # check if config file exists
    if not os.path.exists(syspath):
        create_config(syspath)
        return load_config(project, goal, syspath)
    else:
        return load_config(project, goal, syspath)
