#!/usr/bin/env python3
"""Entrypoint: copy the finished front page to /output/entry.png.

Standard library only; the image is drawn by render.py at build time and
shipped in this repository, so both runs write identical bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit(f"copy mismatch: {dst} differs from {src}")
    print(f"wrote {dst} ({len(data)} bytes, verified)")


if __name__ == "__main__":
    sys.exit(main())
