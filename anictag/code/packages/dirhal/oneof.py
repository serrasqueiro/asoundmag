# oneof.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
Wrapper for regular expressions on filenames
"""

import re

class NameOf():
    """ NameOf -- naming and pattern handling """
    def __init__(self, name="", reg_exps=None):
        """ Initialize """
        self._name = name
        self._exps = self._initialize(reg_exps) if reg_exps else (name,)

    def is_one_of(self) -> bool:
        """ Returns True if matches expression """
        match = self._one_of(self._name, self._exps)
        return bool(match)

    def _one_of(self, astr, rexps):
        """ Returns True if 'astr' matches one of regular expressions """
        for rexp in rexps:
            match = re.match(rexp, astr)
            if match:
                return match
        return None

    def _initialize(self, tups) -> tuple:
        """ Returns """
        res = list()
        if not tups:
            return tuple()
        assert isinstance(tups, (tuple, list))
        for one in tups:
            assert isinstance(one, str), "Expected list of strings!"
            if not one:
                continue
            nums = one.count("*")
            rexp = None
            if nums == 0:
                rexp = re.compile(f".*{one}.*")
            elif nums == 1:
                if one.endswith("*"):
                    rexp = re.compile(f"^{one}.*")
            if rexp is None:
                rexp = re.compile(one)
            res.append(rexp)
        return tuple(res)


if __name__ == '__main__':
    print("Please import dirhal.oneof")
