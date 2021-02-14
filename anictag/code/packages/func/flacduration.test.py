# flacduration.test.py  (c)2021  Henrique Moreira (part of 'func')

"""
Test flacduration.py
"""

import sys
import func.flacduration as flacduration

def main():
    """ Main script! """
    main_test()

def main_test():
    """ Main module test. """
    is_ok = module_test(sys.argv[1:])
    assert is_ok

def module_test(args: list) -> bool:
    """ Module test. """
    for param in args:
        dump_flac_duration(param)
    return True

def dump_flac_duration(fname: str) -> int:
    """ Show the FLAC file duration """
    duration = flacduration.get_flac_duration_ms(fname)
    print("FLAC file:", fname, "; duration is {} = {:.0f}ms".
          format(flacduration.duration_str(duration), duration))
    return 0

if __name__ == '__main__':
    main()
