# renfile.test.py  (c)2021  Henrique Moreira (part of 'dirhal')

"""
Test renfile.py
"""

import sys
import dirhal.renfile as renfile
import dirhal.dirscan as dirscan

def main():
    """ Main script! """
    main_test()

def main_test():
    """ Main module test. """
    is_ok = module_test(sys.argv[1:])
    assert is_ok

def module_test(args: list) -> bool:
    """ Module test. """
    assert args, "At least one arg. expected!"
    pat, param = args[0], args[1:]
    exts = (
        ".mp3",
        )
    if not param:
        param = ['.']
    for adir in param:
        if pat == "mp-rename":
            is_ok = renfile.hardcoded_top_rename(adir, debug=1)
            print("renfile.hardcoded_top_rename() returned", is_ok)
            continue
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


if __name__ == '__main__':
    main()
