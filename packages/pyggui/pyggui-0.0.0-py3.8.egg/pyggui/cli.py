"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -m pyggui` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``pyggui.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``pyggui.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys
import os
import shutil

from pyggui.defaults import structures  # Import the structures package so we can fetch its path


def find_environment_directory(path: str) -> str:
    """
    Function finds venv in passed path and returns path to its parent directory. If venv or env not found, returns
    None.

    Args:
        path (str): Path to find venv or env in.
    """
    path_list = path.split(os.sep)
    venv_dir = []
    for i, _dir in enumerate(path_list):
        if _dir in ["venv", "env"]:
            break
        elif i == len(path_list) - 1:
            return None
        else:
            venv_dir.append(_dir)

    return os.sep.join(venv_dir)


def copy_folder(from_dir: str, to_dir: str, indent: int = 1) -> None:
    ignore = ["__pycache__", ".ignore"]
    for file_name in os.listdir(from_dir):
        if file_name not in ignore:
            from_file_path = os.path.join(from_dir, file_name)
            to_file_path = os.path.join(to_dir, file_name)
            if os.path.isdir(from_file_path):  # If folder, recursive call
                if not os.path.isdir(to_file_path):  # Make dir if not exists
                    os.mkdir(to_file_path)
                print(indent * " " + f"Copying: {file_name} ...")
                copy_folder(from_file_path, to_file_path, indent=indent+1)
                print(indent * " " + " ... done")
            if os.path.isfile(from_file_path):
                print(indent * " " + f"Copying: {file_name} ...")
                shutil.copy(from_file_path, to_file_path)
                print(indent * " " + " ... done")


def copy_structure(from_dir: str, to_dir: str) -> None:
    """
    Function copies one structure to the next without copying already set directories / files.

    Args:
        from_dir ():
        to_dir ():
    """
    ignore_files = [".pyc"]
    indent = " " * 4
    print("PyGgui: Creating your project...")
    for item in os.listdir(from_dir):
        item_from_path = os.path.join(from_dir, item)
        item_end_path = os.path.join(to_dir, item)
        if os.path.isfile(item_from_path):
            # Check if that file does not exist -> copy it
            if not os.path.isfile(item_end_path):
                print(indent + f"Copying: {item}", end="")
                shutil.copy(item_from_path, item_end_path)
                print(" ... done.")
            else:
                print(indent + f"File {item} already exists, skipping.")
        if os.path.isdir(item_from_path):
            if not os.path.isdir(item_end_path):
                os.mkdir(item_end_path)
                print(indent + f"Copying: {item}")
                copy_folder(item_from_path, item_end_path, indent=2)
            else:
                print(indent + f"Directory {item} already exists, skipping.")


structures_path = structures.PATH  # Path of projects structures directory
base_structure_path = os.path.join(structures_path, "base")  # Path of base structure directory


def main(argv=sys.argv):
    """
    Creates a base directory structure for your project / game.

    Args:
        argv (list): List of arguments

    Returns:
        int: A return code
    """
    if "build" in argv:  # TODO: Used for calling script for building with pyinstaller
        print("Building...")
        return
    argument_dict = {
        "-t": None,
        "-p": None
    }
    call_path = argv[0]  # Get path of where call originated from, either some sort of venv or pythons path
    argv = argv[1:]  # Update arguments
    # Parse args into argument dictionary
    for arg in argv:
        split_arg = arg.split("=")
        argument_dict[split_arg[0]] = split_arg[1]

    # Check arguments are okay
    # Check path
    if not argument_dict["-p"]:  # If no path passed to create the structure in, try fetching venv position
        venv_parent_path = find_environment_directory(call_path)
        if not venv_parent_path:
            print("No directory path was specified and the call did not originate from inside a venv. "
                  "Pass a path by the -p argument; ex.: -p=some/path/to/directory, or call from inside a virtual "
                  "environment.")
            return
        else:
            argument_dict["-p"] = venv_parent_path

    # Check type of structure
    if not argument_dict["-t"]:
        argument_dict["-t"] = base_structure_path

    # Start copying files from specified type of directory into set directory.
    copy_structure(from_dir=argument_dict["-t"], to_dir=argument_dict["-p"])

    return 0
