#!/usr/bin/env python3
"""Entry program for the news-image-20261118 bounty (Python 3.13, stdlib only).

The image is rendered at build time by draw_news.py (Pillow) and shipped in
this repository as entry.png. This program just copies it to the output
directory, so both grading runs write byte-identical files.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
