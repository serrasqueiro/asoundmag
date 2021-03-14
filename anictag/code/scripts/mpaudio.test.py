# mpaudio.test.py  (c)2021  Henrique Moreira

"""
Test func.mpaudio.py
"""

import sys
import dirhal.dirscan as dirscan
import dirhal.util as util
import dirhal.oneof as oneof
import func.mpaudio as mpaudio
from waxpage.redit import char_map

SOUND_EXTS = (
    ".mp3",
)

TAGS_TO_EXCLUDE = (
    "TXXX:",
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
    param, exps = list(), list()
    exclude_tags = TAGS_TO_EXCLUDE
    for elem in args:
        if elem.startswith("@"):
            exps.append(elem[1:].strip())
        else:
            param.append(elem)
    for apath in param:
        path = util.clean_path(apath)
        tdir = dirscan.Folder(path, exts=SOUND_EXTS)
        if exps:
            files = [name for name in tdir.files() if oneof.NameOf(name, exps).is_one_of()]
        else:
            files = tdir.files()
        fname = path
        if files:
            for fname in files:
                print("\n::: Showing:", path, fname)
                show_id3_tags(fname, exclude_tags)
        else:
            print("\n::: Showing file tags:", fname)
            show_id3_tags(fname, exclude_tags)
    return True

def show_id3_tags(fname, exclude_tags) -> bool:
    """ Shows id3 tags (raw!)
    """
    aud = mpaudio.Audio(fname)
    if not aud.has_tag_ids():
        print("No tag ids:", fname)
        return False
    is_ok = aud.tag_ids() is not None
    print("Time (seconds):", aud.seconds(), is_ok)
    if not is_ok:
        return False
    for akey in sorted(aud.tag_ids()):
        item = aud.tag_ids()[akey]
        skip =  exclude_tags and mpaudio.tag_str_within(akey, exclude_tags) != ""
        newstr = "[skipped]" if skip else item.pprint()
        shown = char_map.simpler_ascii(newstr, 1)
        print("akey:", type(item), akey, shown)
    return True

if __name__ == '__main__':
    main()
