# mpaudio.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
mpaudio module: a wrapper for 'mutagen' mp3
"""

# pylint: disable=missing-function-docstring

import mutagen.mp3
from mutagen.mp3 import MP3
import func.id3tag as id3tag


class ID3v2():
    """ Abstract class to hold generic ID3v2 (or ID3v1) info
    id3.org/
    """
    # pylint: disable=too-few-public-methods

    _exclude_tag_keys = id3tag.TAG_KEYS_XTRA

    def is_excluded(self, akey: str) -> bool:
        name = akey.split("::")[0]
        return name in self._exclude_tag_keys


class Audio(ID3v2):
    """ Generic Audio class, tailored for mp3 files.
    """
    _original_name = ""
    _obj = None
    _ids = None
    _millis = -1	# milliseconds

    def __init__(self, fname="", trymp3=True):
        self._original_name = fname
        if fname and trymp3:
            self._parse_mp3obj(fname)
        else:
            self._obj = None
        self.reharse()

    def get_mp3(self):
        assert self._obj, "No MP3 yet!"
        return self._obj

    def seconds(self) -> int:
        """ Returns the best estimate for seconds (length) """
        if self._obj is None or self._millis < 0:
            return 0
        msec = round(self._millis)
        if msec <= 0:
            return 1
        return msec

    def tag_ids(self):
        return self._ids["id3v2"]

    def reharse(self) -> bool:
        if not self._obj:
            return False
        self._ids = self._convert_to_ids(self._obj.tags)
        return True

    def _parse_mp3obj(self, fname) -> bool:
        try:
            obj = MP3(fname)
        except mutagen.mp3.HeaderNotFoundError:
            return False
        self._obj = obj
        self._millis = obj.info.length
        return True

    def _convert_to_ids(self, tags) -> dict:
        dct = {
            "@id3v2": valid_id3v2(tags),
            "id3v2": dict(),
            }
        for akey in tags:
            if self.is_excluded(akey):
                continue
            dct["id3v2"][akey] = tags[akey]
        return dct

def valid_id3v2(id3tags) -> bool:
    """ Returns True if 'id3tags' seems to be a valid MP3 ID3v2 tag """
    # We simply check if "TPE1" exists
    is_ok = id3tags.get("TPE1") is not None
    return is_ok

if __name__ == '__main__':
    print("Please import dirhal.mpaudio")