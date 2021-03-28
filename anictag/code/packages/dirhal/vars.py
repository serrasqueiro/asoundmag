# vars.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
vars: variable substitution
"""

# pylint: disable=missing-function-docstring, no-self-use

from os import environ
import dirhal.util

USE_VARS = (
    "PATH", "PYTHONPATH",
    "LOCALAPPDATA", "APPDATA",
)

class EnvVars():
    """ Environment variables. """
    def __init__(self):
        self._vars = self._relevant_vars(USE_VARS)

    def env(self, name):
        return self._vars.get(name)

    def _relevant_vars(self, used) -> dict:
        res = dict()
        for avar in used:
            res[avar] = environ.get(avar) if environ.get(avar) else ""
        return res

    def replace_path_vars(self, path: str, linear: bool=True) -> str:
        # pylint: disable=line-too-long
        vdict = self._vars
        pot_var = [("%" + name + "%", vdict[name]) for name in vdict if valid_var_value(vdict.get(name))]
        res = path
        for avar, value in pot_var:
            res = cleaner_path(res.replace(avar, value)) if linear else res.replace(avar, value)
        return res


def valid_var_value(astr) -> bool:
    """ Returns True if 'astr' string is not empty (and not None) """
    if astr is None:
        return False
    return astr != ""

def cleaner_path(astr: str) -> str:
    if '\\' not in astr:
        return astr
    res = dirhal.util.clean_path(astr)
    return res


if __name__ == '__main__':
    print("Please import dirhal.vars")
