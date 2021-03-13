# id3tag.py  (c)2021  Henrique Moreira (part of 'dirhal')
"""
id3tag module: simple ID3v2 constants/ functions.
a wrapper for 'mutagen' mp3
"""

from mutagen.mp3 import MP3

TAG_KEYS_XTRA = (
    "SYLT",	# (4.10) Synchronised lyrics/text
    "USLT",	# (Unsychronized lyric/text transcription
    )


if __name__ == '__main__':
    print("Please import dirhal.id3tag")
