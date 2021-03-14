# mpaudio.test.py  (c)2021  Henrique Moreira

"""
Test func.mpaudio.py
"""

import sys
import dirhal.dirscan as dirscan
import dirhal.util as util
import func.mpaudio as mpaudio

SOUND_EXTS = (
    ".mp3",
)

def main():
    """ Main script! """
    main_test(sys.argv[1:])

def main_test(args):
    """ Main module test. """
    is_ok = module_test(args)
    assert is_ok

def module_test(args: list) -> bool:
    """ Module test. """
    assert args, "At least one arg. expected!"
    param = args
    for apath in param:
        path = util.clean_path(apath)
        tdir = dirscan.Folder(path, exts=SOUND_EXTS)
        files = tdir.files()
        fname = path
        if files:
            for fname in files:
                print("\n::: Showing:", path, fname)
                show_id3_tags(fname)
        else:
            print("\n::: Showing file tags:", fname)
            show_id3_tags(fname)
    return True

def show_id3_tags(fname) -> bool:
    """ Shows id3 tags (raw!)
    """
    aud = mpaudio.Audio(fname)
    is_ok = aud.tag_ids() is not None
    print("Time (seconds):", aud.seconds(), is_ok)
    if not is_ok:
        return False
    for akey in sorted(aud.tag_ids()):
        item = aud.tag_ids()[akey]
        shown = item.pprint()
        print("akey:", type(item), akey, shown)
    return True

if __name__ == '__main__':
    main()
