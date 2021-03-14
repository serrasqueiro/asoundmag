# util.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
Utilities module: OS independent functions
"""

import os.path

def maybe_audio(path) -> str:
    """ Returns True if file at path may be an audio file. """
    return os.path.isfile(path)

def clean_path(path) -> str:
    """ Returns a cleaner path """
    if not isinstance(path, str):
        return ""
    res = os.path.realpath(path)
    res = res.replace("\\", "/")
    return res

if __name__ == '__main__':
    print("Please import dirhal.util")
