# renfile.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
renfile module
"""

import os
import re
import dirhal.dirscan as dirscan

def hardcoded_top_rename(adir, debug=0) -> bool:
    """ Renames 'nnn. Xyz.mp3' into Xyz.mp3
    'adir' is a directory.
    Main use-case is: this directory contains .mp3 files.
    """
    assert int(debug) >= 0, "Wrong debug"
    tdir = dirscan.Folder(adir, exts=(".mp3",))
    files = tdir.files()
    if not files:
        return False
    alist, other = list(), ""
    dest = dict()
    reobj = re.compile(r"(\d\d\d)\. (.+)")
    for fname in files:
        mat = re.match(reobj, fname)
        if not mat:
            other = fname
            break
        whole = mat.group(0)
        new = mat.group(2).strip()
        alist.append((whole, new))
        if new in dest:
            if debug > 0:
                print("Duplicate destination:", new)
            return False
        dest[new] = whole
    if other:
        if debug > 0:
            print("Debug: At least one file not matching regexp:", other)
        return False
    for whole, new in alist:
        if debug > 0:
            print(f"I am about to rename '{whole}' to '{new}'")
            key = input("Press enter")
            if key:
                return False
        os.rename(whole, new)
    return True


if __name__ == '__main__':
    print("Please import dirhal.renfile")
