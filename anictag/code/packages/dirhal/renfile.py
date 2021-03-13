# renfile.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
renfile module
"""

import os
import re
import dirhal.dirscan as dirscan

def hardcoded_top_rename(adir, pattern="", debug=0) -> bool:
    """ Renames 'nnn. Xyz.mp3' into Xyz.mp3
    'adir' is a directory.
    Main use-case is: this directory contains .mp3 files.
    Returns True if rename occurred consistently.
    """
    msg = hardcoded_top_rename_at(adir, pattern, debug)
    return not msg

def hardcoded_top_rename_at(adir, pattern="", debug=0) -> str:
    """ See hardcoded_top_rename()
    Returns an empty string if all ok, or the string at least one regexp failed.
    The following special codes apply:
	@!	No relevant files found
	@s	Single file, no renaming done
	@d	If rename occurred, duplicates would exist
	@q	User did quit of renaming (only when debug=1)
    """
    assert int(debug) >= 0, "Wrong debug"
    tdir = dirscan.Folder(adir, exts=(".mp3",))
    files = tdir.files()
    if not files:
        return "@!"
    if len(files) <= 1:
        return "@s"	# single file
    alist, other = list(), ""
    dest = dict()
    if not pattern:
        dig_pat = r"(\d\d\d)\. (.+)"
    else:
        dig_pat = pattern
    reobj = re.compile(dig_pat)
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
            return "@d"
        dest[new] = whole
    if other:
        if debug > 0:
            print("Debug: At least one file not matching regexp:", other)
        return other
    for whole, new in alist:
        if debug > 0:
            print(f"I am about to rename '{whole}' to '{new}'")
            key = input("Press enter")
            if key:
                return "@q"	# user did quit (did enter anything but empty)
        os.rename(whole, new)
    return ""


if __name__ == '__main__':
    print("Please import dirhal.renfile")
