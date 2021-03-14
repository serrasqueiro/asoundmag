# util.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
Utilities module: OS independent functions
"""

import os.path

def clean_path(path) -> str:
    """ Returns a cleaner path """
    if not isinstance(path, str):
        return ""
    res = os.path.realpath(path)
    res = res.replace("\\", "/")
    return res

if __name__ == '__main__':
    print("Please import dirhal.util")
