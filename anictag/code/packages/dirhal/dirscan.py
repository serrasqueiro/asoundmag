# dirscan.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
dirscan module
"""

import os


class DirHandler():
    """ Abstract class to handle errors. """
    _msg = ""
    _str_path_list = "; "
    _alpha_crit = "i"	# case-insensitive

    def error_string(self) -> str:
        """ Returns the message stored, as a string """
        return self._msg

    @staticmethod
    def set_path_list_string(astr):
        """ Sets the path list string. """
        assert isinstance(astr, str), "Expected string in 'astr'"
        DirHandler._str_path_list = astr


class Folder(DirHandler):
    """ Folder class -- directory """
    _original_path = ""
    _exts = tuple()
    _entries = list()
    _files, _dirs = list(), list()

    def __init__(self, adir="", scan=True, exts=None):
        """ Initialize Folder() """
        self._msg = ""	# init. parent attr.
        self._original_path = adir
        assert isinstance(adir, str), "adir should be a string"
        assert isinstance(scan, bool), "'scan' should be a bool"
        self._exts = exts if exts else tuple()
        assert isinstance(self._exts, (tuple, list))
        self._entries = list()
        self._files, self._dirs = list(), list()
        if scan:
            self._scan(True)

    def rescan(self) -> bool:
        """ Re-scan directory """
        self._scan(True)
        return True

    def _scan(self, new) -> bool:
        """ Scan files on directory """
        apath = self._original_path
        if apath:
            try:
                os.chdir(apath)
            except PermissionError:
                self._msg = f"Cannot change to dir: {apath}"
                return False
        if new:
            self._entries = list()
        for elem in os.scandir():
            self._entries.append((elem.name, elem, elem.stat()))
        self._files = self._files_within(self._entries)
        self._dirs = [name for name, elem, _ in self._entries if elem.is_dir()]
        return True

    def build_str(self) -> str:
        """ Build string from path list """
        return self._str_path_list.join(self.dirs() + self.files())

    def dirs(self) -> list:
        """ Returns the list of directories (suffixed by '/') """
        dirs = [tic + "/" for tic in sorted(self._dirs, key=str.casefold)]
        return dirs

    def files(self) -> list:
        """ Returns the list of files """
        files = sorted(self._files, key=str.casefold)
        return files

    def __len__(self) -> int:
        """ Returns the number of entries (dirs and files). """
        return len(self.dirs() + self.files())

    def _files_within(self, entries) -> list:
        res = [name for name, elem, _ in entries if not elem.is_dir() and self._criteria(elem)]
        return res

    def __str__(self) -> str:
        """ Returns the string related with elements of a path (dirs+files).
        """
        return self.build_str()

    def _criteria(self, elem, alpha="") -> bool:
        """ Returns True if elem fills up criteria """
        if not self._exts:
            return True
        if not alpha:
            alpha = self._alpha_crit
        for end in self._exts:
            if alpha == "i":
                if elem.name.lower().endswith(end.lower()):
                    return True
            else:
                if elem.name.endswith(end):
                    return True
        return False


if __name__ == '__main__':
    print("Please import dirhal.dirscan")
