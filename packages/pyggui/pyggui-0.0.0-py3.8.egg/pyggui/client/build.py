"""
Module for building current game into an executable using pyinstaller.
"""

from typing import List
import os

from pyggui.configure.pages import get_all_page_import_strings


def get_arguments_dict(args: List[str], separator: str = "="):
    args_dict = {}
    for arg in args:
        split_arg = arg.split(separator)
        if len(split_arg) == 2:
            args_dict[split_arg[0]] = split_arg[1]
    return args_dict


def main(argv: List[str]) -> int:
    """
    Main function for creating the structure needed to start developing a game using pyggui.

    Args:
        argv (List[str]): sys.argv, not including "build".

    Returns:
        int: Exit code
    """
    call_path = argv[0]  # Get path of where call originated from, either some sort of venv or pythons path
    args_dict = get_arguments_dict(args=argv)
    print(call_path)
    if "-m" in args_dict:
        main_file_path = args_dict["-m"]
        print(get_all_page_import_strings(
            dir_path=os.path.basename(os.path.dirname(main_file_path)),
            called_from_module=main_file_path
        ))
    return 0
