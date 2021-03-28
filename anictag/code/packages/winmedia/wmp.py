# wmp.py  (c)2021  Henrique Moreira (part of 'winmedia')
"""
Utilities module: OS independent functions
"""

# pylint: disable=missing-function-docstring

import dirhal.util
from dirhal.vars import EnvVars

WIN32_WMP_DATA_PATH = "%LOCALAPPDATA%/Microsoft/Media Player"
WIN32_WMP_LAST_PLAYED_PL = "lastplayed.wpl"


class WMP():
    """ WMP -- media player in Win32 environments """
    _default_lastplay_playlist = WIN32_WMP_DATA_PATH + "/" + WIN32_WMP_LAST_PLAYED_PL
    _lastplay = ""

    def __init__(self, default_playlist=None):
        if default_playlist is None:
            self._lastplay = WMP._default_lastplay_playlist
        else:
            self._lastplay = dirhal.util.clean_path(default_playlist)

    def get_lastplaylist(self):
        return EnvVars().replace_path_vars(self._lastplay)


if __name__ == '__main__':
    print("Please import winmedia.wmp")
    print(WMP().get_lastplaylist())
