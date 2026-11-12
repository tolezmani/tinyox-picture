"""TinyOX cutest-picture-01 entry (Python 3.13, standard library only).

Copies the picture beside this file to /output/entry.png. Deterministic:
same input bytes, same output bytes, every run. The entry self-checks the
gate before finishing: a whole JPEG or PNG of at most 1 MiB.
"""

import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
if os.path.getsize(src) > 1048576:
    raise SystemExit("entry.png exceeds the 1 MiB gate")
with open(src, "rb") as f:
    magic = f.read(3)
if magic[:2] != b"\xff\xd8" and magic != b"\x89PN":
    raise SystemExit("entry.png is neither JPEG nor PNG")
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
