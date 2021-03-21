# txlist.py  (c)2021  Henrique Moreira

"""
Checks txc references with real path.
"""

# pylint: disable=missing-function-docstring, unused-argument


import sys
import dirhal.dirscan as dirscan
import aurl.urlutil as urlutil
from waxpage.txc import FileTXC

IGNORED_FILES_EXT = (
    ".lnk",
    ".ini",
    )


def main():
    """ Main test script! """
    prog = __file__
    code = runner(sys.stdout, sys.stderr, sys.argv[1:])
    if code is None:
        print(f"""Usage:

{prog} check [options] real_path txc-filename1 [txc-filenameN ...]

Options are:
   -v          Verbose mode (shows Latin-1 accents, etc.)
   -d          Dump paths
   -e          Exclude dirs with pattern (colon separated list of strings)
""")
    sys.exit(code if code else 0)


def runner(out, err, args) -> int:
    """ Basic run """
    verbose = 0
    do_dump = False
    exclude_pats = list()
    if not args:
        return None
    param = args
    while param and param[0].startswith("-"):
        if param[0] in ("-v", "--verbose"):
            del param[0]
            verbose += 1
            continue
        if param[0] in ("-d", "--dump"):
            del param[0]
            do_dump = True
            continue
        if param[0] in ("-e", "--exclude"):
            exclude_pats = param[1].split(":")
            del param[:2]
            continue
        return None
    if len(param) < 2:
        return None
    apath = param[0].rstrip("/")
    if not apath:
        return None
    opts = {
        "verbose": verbose,
        "dump": do_dump,
        "dir": apath,
        "excl": exclude_pats,
        }
    code = check(out, err, param[1:], opts)
    return code


def check(out, err, txc_files, opts) -> int:
    """ Check TXC file content with URLs, and local directory """
    result = 0
    #verbose = opts["verbose"]
    apath = opts["dir"]
    #paths = recurse_dirs(apath, opts["excl"])
    if opts["dump"]:
        for path in paths:
            print(path)
    for fname in txc_files:
        tfile = FileTXC(fname)
        tfile.set_style("text")
        if tfile.error:
            return 1
        is_ok = tfile.parse()
        if not is_ok:
            print(f"TXC file not parsed: {fname}")
            print("msg:", tfile.msg)
            return 3
        code, msg = check_context(tfile, apath)
        if msg:
            print("Warn:", msg)
    return 0


def check_context(tfile, apath, debug=0) -> tuple:
    if debug > 0:
        for node in tfile.nodes:
            print("NODE:", node.kind, node.lines)
    items = [(node.lines[0], node.lines[1:]) for node in tfile.nodes if node.kind == "item"]
    for item, tups in items:
        shown = [urlutil.unquote(tups[0])] + [tups[1:]]
        if debug > 0:
            print("Debug:", "ITEM:", item, shown)
    return 0, None


def recurse_dirs(apath, excl, level=0, debug=0) -> list:
    if debug > 0:
        print(f"recurse_dirs(), {level}:", apath)
    assert level < 100, "recurse_dirs() depth too far"
    res = list()
    pre = " " * 2 * level
    _, dirs, files = scan_dir(apath)
    for name, _ in files:
        res.append(f"{pre}{name}")
    for adir in dirs:
        #print(f"{pre}{apath}/{adir}")
        s_path = apath + "/" + adir
        do_it = True
        for s_excl in excl:
            pos = s_excl.find('/')
            if (s_excl in adir) or (pos >= 0 and s_excl in s_path):
                do_it = False
                break
        if not do_it:
            continue
        assert adir.endswith("/")
        res.append(f"{pre}{adir}")
        newpath = apath + "/" + adir[:-1]
        these = recurse_dirs(newpath, excl, level+1)
        res += these
    return res


def scan_dir(apath) -> tuple:
    assert not apath.endswith("/"), "No trailing slash!"
    folder = dirscan.Folder(apath)
    files = [(name, path_join(apath, name)) for name in folder.files() if eligible(name, apath)]
    #for adir in folder.dirs():
    #    print(f"{apath}", adir)
    #for name, _ in files:
    #    print(f"{apath}/", name)
    return (apath, folder.dirs(), files)


def path_join(path: str, name: str) -> str:
    """ Returns fixed path/name, always (not dependent on OS) """
    return path + "/" + name

def eligible(name, path) -> bool:
    if name.lower().endswith(IGNORED_FILES_EXT):
        return False
    return not name.startswith(".")


# Main script
if __name__ == "__main__":
    main()
