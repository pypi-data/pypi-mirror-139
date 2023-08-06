import os
from math import floor, ceil
import ctypes
import platform
import argparse
import re

from progressbar import Bar, AdaptiveETA, FormatCustomText, progressbar

NUM_SLICES = 4096
FILENAME = 'loaf'


def to_gb(num_bytes: int) -> float:
    return num_bytes / 2 ** 30


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Makes a really big file (a loaf) and deletes it. Intended to wipe a hard drive. '
                    'Powers of 2 are used for all sizes.'
    )

    parser.add_argument('directory', nargs='?', default='.', help='Where should the loaf go? (a loafcation)')

    parser.add_argument(
        '-f', '--free-space', dest='space_to_leave', default='8K',
        help='Leave this amount of space free. Examples: 2.4M, 20 k, 0b. Default is 8K'
    )

    parser.add_argument(
        '-b', '--byte', dest='hex_byte', default='00',
        help='Write this hex value to disk. Possible values: 00-FF.'
    )

    parser.add_argument(
        '-s', '--size', dest='loaf_size',
        help='Instead of filling up most of disk with the file, write a specific size file. Examples: 5G, 12.4 k'
    )

    parser.add_argument(
        '-l', '--leave-loaf', action='store_true', dest='leave_loaf',
        help='Don\'t delete the loaf after creating it'
    )

    return parser.parse_args()


def get_byte_to_write(hex_string: str) -> bytes:
    byte = bytes.fromhex(hex_string)

    if len(byte) != 1:
        raise ValueError('Please specify a singe byte (00-FF) to be written')

    return byte


def size_string_to_num_bytes(size_string: str) -> int:
    postfixes = {'T': 40, 'G': 30, 'M': 20, 'K': 10, 'B': 0}

    size_string = size_string.upper().strip()
    match = re.match(r'^(\d+\.?\d*)\s*([T,G,M,K,B])I?B?$', size_string)

    if not match:
        raise ValueError(f'Unsure how to parse "{size_string}" as a size. Try a format like "12 K"')

    num_bytes = float(match.group(1)) * 2 ** postfixes[match.group(2)]
    return floor(num_bytes)


def get_free_space_bytes(directory='.') -> int:
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(directory), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        free_space_info = os.statvfs(directory)
        return floor(free_space_info.f_bavail * free_space_info.f_frsize)


def main():
    args = get_args()
    free_space = get_free_space_bytes(args.directory)

    if args.loaf_size:
        loaf_size = size_string_to_num_bytes(args.loaf_size)
        if free_space < loaf_size:
            raise ValueError(
                f'There is not enough space on disk ({to_gb(free_space):.2f} GiB) '
                f'to bake a loaf that big ({to_gb(loaf_size):.2f} GiB)'
            )
    else:
        space_to_leave = size_string_to_num_bytes(args.space_to_leave)
        loaf_size = free_space - space_to_leave
        if loaf_size <= 0:
            raise ValueError(
                f'The amount of space to leave ({to_gb(space_to_leave):.2f} GiB) '
                f'was greater than or equal to the amount of space on disk ({to_gb(free_space):.2f} GiB).'
            )

    print(f'About to write {to_gb(loaf_size):.2f} GiB out of {to_gb(free_space):.2f} GiB free on this disk')

    byte_to_write = get_byte_to_write(args.hex_byte)

    gb_written_widget = FormatCustomText("%(gb_written)6.2f GiB written", {'gb_written': 0})
    widgets = [Bar(), ' ', AdaptiveETA(), ' | ', gb_written_widget]

    loaf_path = os.path.join(args.directory, FILENAME)
    loaf = open(loaf_path, 'wb')
    try:
        slice_size = ceil(loaf_size / NUM_SLICES)
        bytes_written = 0

        for slice_index in progressbar(range(NUM_SLICES), widgets=widgets):
            if bytes_written + slice_size > loaf_size:
                slice_size = loaf_size - bytes_written

            loaf.write(byte_to_write * slice_size)

            bytes_written += slice_size
            gb_written_widget.update_mapping(gb_written=to_gb(bytes_written))

    finally:
        loaf.close()
        if not args.leave_loaf:
            print('Cleaning up')
            os.remove(loaf_path)


if __name__ == '__main__':
    main()
