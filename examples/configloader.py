import shutil
import sys
import os.path
import pathlib
import yaml


def default_config_path():
    """

    this checks the operation system of the user.
    this is used to determine the standard save location for the global gridscale config file.

    """
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
        raise RuntimeError("Operating system not supported")

    return path


def create_config(path):
    """
    this will copy the currently used config file in the standard folder
    """
    syspath = default_config_path() + "/config.yaml"
    shutil.copyfile(path, syspath)


def load_config(path):
    """
    First checking "path" to match minimum length and other requirements.

    Then it opens the specified config file and returns all keys which include token and UserId.
    """
    # opens specified file to retrieve config tokens
    if isinstance(path, (pathlib.Path, str)):
        assert path
        with open(f"{path}", 'r') as stream:
            data = yaml.safe_load(stream)
            # return list of dictionaries for all projects
            for value in data.values():
                return (value)
    else:
        raise AssertionError
