"""

"""

from typing import Dict
import os
import sys
import inspect
import glob
import importlib
import pkgutil


def _get_all_page_classes() -> Dict[str, any]:
    """
    Function returns a dictionary containing all classes that:
        Are imported and are subclasses of classes defined in the _pyggui.gui.page module

    Returns:
        dict[str, any] where key = str(name_of_class), value = class
    """
    # Fetch all classes defined in the _pyggui.gui.page.py module, save all of its subclasses that are imported
    pages = {}  # Create dictionary with each classes name str as key, class as value
    for module, _ in sys.modules.items():  # Get all imported modules
        for name, cls in inspect.getmembers(sys.modules[module]):  # Get members of each module
            if inspect.isclass(cls):  # Filter only classes
                if cls.__module__ == "_pyggui.gui.page":  # Check if class (parent class) is from correct module
                    for _class in cls.__subclasses__():  # Fetch subclasses
                        pages[str(_class.__name__)] = _class


def get_all_page_classes() -> Dict[str, any]:
    """
    Function returns a dictionary containing all classes that:
        Are imported and are subclasses of classes defined in the _pyggui.gui.page module

    Returns:
        dict[str, any] where key = str(name_of_class), value = class
    """
    # Fetch all classes defined in the _pyggui.gui.page.py module, save all of its subclasses that are imported
    pages = {}  # Create dictionary with each classes name str as key, class as value
    for name, cls in inspect.getmembers(sys.modules["_pyggui.gui.page"]):  # Get members of each module
        if inspect.isclass(cls):  # Filter only classes
            for _class in cls.__subclasses__():  # Fetch subclasses
                pages[str(_class.__name__)] = _class
    return pages


def create_module_import_string(package_name: str, module_path: str) -> str:
    """
    Function creates a module import string (ex. foo.bar.module) based on the package name and file path of python
    file.

    Args:
        package_name (str): Name of package where the python module is contained (root. dir. of project)
        module_path (str): Absolute path of module

    Returns:
        str:
    """
    relative_file_path = os.path.normpath(module_path)  # Normalize path string into proper os path string
    # Create list with directory names, split at os separator, use lambda to remove .py from file names
    path_list = list(map(
        lambda name: name.replace(".py", "") if ".py" in name else name,
        relative_file_path.split(os.sep)
    ))
    # Check if passed module is from package
    if package_name not in path_list:
        pass  # Raise error here
    # Get index of package, return import string from package name on
    package_root_index = path_list.index(package_name)
    return ".".join(path_list[package_root_index + 1:])


def get_all_classes_in_dir(dir_path, called_from_module=""):
    """for (module_loader, name, ispkg) in pkgutil.iter_modules([dir_path]):
        if name not in sys.modules and ispkg:
            sys.path.append(name)"""

    # print(get_all_page_classes())

    print(f"{dir_path=}, {called_from_module=}")
    package_name = os.path.basename(os.path.dirname(called_from_module))
    print(package_name)
    ignore = ["venv", "env"]
    for root, directories, files in os.walk(dir_path):
        directories[:] = [d for d in directories if d not in ignore]
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = os.path.join(root, filename)
                if not os.path.samefile(file_path, called_from_module):
                    module_name = os.path.splitext(os.path.basename(filename))[0]
                    file_path = os.path.join(root, filename)
                    import_str = create_module_import_string(package_name, os.path.join(root, filename))
                    importlib.import_module(import_str)
    print(get_all_page_classes())
