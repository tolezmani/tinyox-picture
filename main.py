"""TinyOX cutest-picture-01 entry (Python 3.13, standard library only).

Copies the picture shipped beside this file to /output/entry.png.
Deterministic: same input bytes, same output bytes, every run. The
entry self-checks the competition gate before it finishes: the file
must be a whole JPEG or PNG of at most 1 MiB and 1024x1024.
"""

import os
import shutil

MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8"
PNG_MAGIC = b"\x89PNG"


def _fail(message):
    raise SystemExit(f"gate failed: {message}")


def _jpeg_dimensions(data):
    """(width, height) from the first SOF marker, or None if not found."""
    pos = 2  # skip the SOI marker
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker == 0xFF:  # fill byte before the real marker
            pos += 1
            continue
        if marker in (0xC0, 0xC1, 0xC2):
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD9:
            pos += 2  # standalone marker, no length field
            continue
        length = int.from_bytes(data[pos + 2:pos + 4], "big")
        if length < 2:
            return None
        pos += 2 + length
    return None


def _png_dimensions(data):
    """(width, height) from the IHDR chunk, or None if not found."""
    if len(data) >= 24 and data[12:16] == b"IHDR":
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        return width, height
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        _fail(f"entry.png is {size} bytes, over the 1 MiB gate")
    with open(src, "rb") as handle:
        head = handle.read(65536)
    if head.startswith(JPEG_MAGIC):
        dimensions = _jpeg_dimensions(head)
    elif head.startswith(PNG_MAGIC):
        dimensions = _png_dimensions(head)
    else:
        _fail("entry.png is neither JPEG nor PNG")
    if dimensions is None:
        _fail("entry.png has no readable width/height")
    width, height = dimensions
    if width > 1024 or height > 1024:
        _fail(f"entry.png is {width}x{height}, over the 1024x1024 gate")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
