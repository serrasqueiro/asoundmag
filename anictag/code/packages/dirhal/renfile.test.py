# renfile.test.py  (c)2021  Henrique Moreira (part of 'dirhal')

"""
Test renfile.py
"""

import sys
import os.path
import dirhal.renfile as renfile
import dirhal.dirscan as dirscan

DEBUG=0


def main():
    """ Main script! """
    main_test(sys.argv[1:])

def main_test(args: list):
    """ Main module test. """
    is_ok = module_test(args)
    assert is_ok

def module_test(args: list) -> bool:
    """ Module test. """
    assert args, "At least one arg. expected!"
    pat, param = args[0], args[1:]
    debug = DEBUG
    exts = (
        ".mp3",
        )
    if not param:
        param = ['.']
    if pat == "mp-rename":
        is_ok = do_top_rename(param, debug=debug)
        return is_ok
    for adir in param:
        print("Unknown 'pat':", pat)
        tdir = dirscan.Folder(adir, exts=exts)
        msg = tdir.error_string()
        shown = tdir if len(tdir) > 0 else f"Does not contain {exts}"
        if msg:
            print(f"Error at {adir}: {msg}")
        else:
            print("tdir:", shown)
        ndir = dirscan.Folder(adir)
        dirscan.Folder.set_path_list_string("\n")
        print("--\nNo filter, ndir:")
        print(ndir)
    return True

def do_top_rename(param, debug=0) -> bool:
    """ 'top_rename' if possible for all.
    """
    for adir in param:
        if not os.path.isdir(adir):
            return False
    for adir in param:
        #is_ok = renfile.hardcoded_top_rename(adir, r"(\d\d)\. (.+)", debug=1)
        is_ok = renfile.hardcoded_top_rename(adir, debug=debug)
        print("renfile.hardcoded_top_rename() returned", is_ok, "; path:", adir)
    return True


if __name__ == '__main__':
    main()
