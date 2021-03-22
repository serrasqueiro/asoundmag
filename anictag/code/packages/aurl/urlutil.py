# urlutil.py  (c)2021  Henrique Moreira (part of 'aurl')
"""
Wrapper for urllib methods
"""

import urllib.parse


def unquote(astr: str) -> str:
    """ Returns the unquoted string (e.g. %21 = '!') for 'astr'.
    """
    res = urllib.parse.unquote(astr)
    return res

def urlparse(url: str):
    """ Return """
    return urllib.parse.urlparse(url)

def query_style(query: str, except_list: tuple) -> list:
    """ Returns a linear list from (http) query part of a URL.
    """
    if except_list:
        exc = except_list
    else:
        exc = tuple()
    res = [("eq" if "=" in arg else "", arg.split("=")) for arg in query.split("&") if arg.split("=")[0] not in exc]
    return res

def onedrive_style(query: str) -> list:
    """ Returns a linear list from (http) query part of a URL.
    """
    cid = None
    query_list = query_style(query, ('o',))
    dct = {
        "cid": None,
        "id-num": None,
        "par-id": None,
        "tuples": query_list,
    }
    for _, tup in query_list:
        left, right = tup
        if left == "cid":
            cid = right
            dct["cid"] = right
    if not cid:
        return ["all", "", query_list]
    cid_str = cid + "!"
    for _, tup in query_list:
        left, right = tup
        if left == "id":
            dct["id-num"] = right.split("!", maxsplit=1)[1] if right.startswith(cid_str) else right
        elif left == "parId":
            dct["par-id"] = right.split("!", maxsplit=1)[1] if right.startswith(cid_str) else right
    res = ["id", dct.get("id-num"), dct]
    return res

if __name__ == '__main__':
    print("Please import aurl.urlutil")
