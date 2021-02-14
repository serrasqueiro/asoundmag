# flacduration.py  (c)2021  Henrique Moreira (part of 'func')
"""
flacduration module
"""
import struct

def duration_str(atime: int) -> str:
    """ Returns a human readable duration of a song/ media-file. """
    msec = int(atime)
    if msec < 0:
        return "-" + duration_str(-msec)
    secs = round(msec / 1000.0, 0)
    minu = int(secs // 60)
    rem = int(secs % 60)
    secs = rem
    hour = rem // 60
    astr = "" if hour <= 0 else f'{hour}:' # or {hour:.0f} if it was a float
    astr += "" if minu <= 0 else f'{minu}:'
    astr += str(secs)
    return astr

def get_flac_duration_ms(filename: str) -> int:
    """ Returns duration of a FLAC file in milliseconds. """
    secs = get_flac_duration(filename)
    return round(secs * 1000.0, 0)

def get_flac_duration(filename: str) -> float:
    """
    Returns the duration of a FLAC file in seconds
    https://xiph.org/flac/format.html
    Taken from git@gist.github.com:8c474782ed66c7115e10904fecbed86a.git
    """
    with open(filename, 'rb') as stream:
        return flac_duration_stream(stream, filename)

def flac_duration_stream(stream, filename=None) -> float:
    """
    Returns the duration of a FLAC file in seconds
    https://xiph.org/flac/format.html
    Taken from git@gist.github.com:8c474782ed66c7115e10904fecbed86a.git
    """
    msg = f"File is not a FLAC file: {filename}"
    if stream.read(4) != b'fLaC':
        raise ValueError(msg)
    header = stream.read(4)
    while len(header) > 0:
        meta = struct.unpack('4B', header)  # 4 unsigned chars
        block_type = meta[0] & 0x7f  # 0111 1111
        size = bytes_to_int(header[1:4])
        if block_type == 0:  # Metadata Streaminfo
            streaminfo_header = stream.read(size)
            unpacked = struct.unpack('2H3p3p8B16p', streaminfo_header)
            # see xiph_infos()
            samplerate = bytes_to_int(unpacked[4:7]) >> 4
            sample_bytes = [(unpacked[7] & 0x0F)] + list(unpacked[8:12])
            total_samples = bytes_to_int(sample_bytes)
            duration = float(total_samples) / samplerate
            return duration
        header = stream.read(4)
    return 0.0

def bytes_to_int(abytes: list) -> int:
    """ Convert bytes to integer! """
    result = 0
    for byte in abytes:
        result = (result << 8) + byte
    return result

def xiph_infos() -> str:
    """ from xiph.org/

    16 (unsigned short)  | The minimum block size (in samples)
                           used in the stream.
    16 (unsigned short)  | The maximum block size (in samples)
                           used in the stream. (Minimum blocksize
                           == maximum blocksize) implies a
                           fixed-blocksize stream.
    24 (3 char[])        | The minimum frame size (in bytes) used
                           in the stream. May be 0 to imply the
                           value is not known.
    24 (3 char[])        | The maximum frame size (in bytes) used
                           in the stream. May be 0 to imply the
                           value is not known.
    20 (8 unsigned char) | Sample rate in Hz. Though 20 bits are
                           available, the maximum sample rate is
                           limited by the structure of frame
                           headers to 655350Hz. Also, a value of 0
                           is invalid.
    3  (^)               | (number of channels)-1. FLAC supports
                           from 1 to 8 channels
    5  (^)               | (bits per sample)-1. FLAC supports from
                           4 to 32 bits per sample. Currently the
                           reference encoder and decoders only
                           support up to 24 bits per sample.
    36 (^)               | Total samples in stream. 'Samples'
                           means inter-channel sample, i.e. one
                           second of 44.1Khz audio will have 44100
                           samples regardless of the number of
                           channels. A value of zero here means
                           the number of total samples is unknown.
    128 (16 char[])      | MD5 signature of the unencoded audio
                           data. This allows the decoder to
                           determine if an error exists in the
                           audio data even when the error does not
                           result in an invalid bitstream.
    """
    return "https://xiph.org/flac/format.html#metadata_block_streaminfo"

if __name__ == '__main__':
    print("Please import func.flacduration")
