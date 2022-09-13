#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import struct


empty = struct.pack("I", 0xFFFFFFFF)
head  = [empty for n in range(128)]

def parse_dtb(dtb):
    dtb_entry = []

    with open(dtb, "rb") as dtb_file:
        data = dtb_file.read()
        size = dtb_file.tell()
        offset = 0

        while offset <= size - 8:
            magic = struct.unpack(">I", data[ offset : offset + 4 ])[0]

            if magic == 0xD00DFEED:
                dtb_size = struct.unpack(">I", data[ offset + 4 : offset + 8 ])[0]
                dtb_entry.append(offset)
                offset = offset + dtb_size
            else:
                offset += 1
    return dtb_entry

def write_header(of, inf, entry):
    head[0] = struct.pack("I", 0xdeaddead)           # Magic number (very strange)
    head[1] = struct.pack("I", os.path.getsize(inf)) # DTBO size
    head[2] = struct.pack("I", 512)                  # Header size
    head[3] = struct.pack("I", 2)                    # Header version
    head[4] = struct.pack("I", len(entry))           # dtbo entry count

    # Reserved
    head[5] = empty
    head[6] = empty
    head[7] = empty

    i = 0

    for offset in entry:
        head[8 + i] = struct.pack("I", offset)
        i += 1

    with open(of, 'wb') as off:
        for item in head:
            off.write(item)

        with open(inf, 'rb') as inff:
            for line in inff.readlines():
                off.write(line)

def main(argv):
    if len(argv) < 2:
        print("Usage: python3 mkodmdtbo.py overlay.dtb odmdtbo.img")
        sys.exit(1)

    in_img  = argv[1]
    out_img = argv[2]

    dtb = parse_dtb(in_img)

    write_header(out_img, in_img, dtb)

if __name__ == "__main__":
    main(sys.argv)
