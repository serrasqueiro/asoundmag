# urlutil.py  (c)2021  Henrique Moreira (part of 'aurl')
"""
Wrapper for urllib methods
"""

import urllib.parse


def unquote(astr) -> str:
    """ Returns the unquoted string (e.g. %21 = '!') for 'astr'.
    """
    res = urllib.parse.unquote(astr)
    return res


if __name__ == '__main__':
    print("Please import aurl.urlutil")
