#!/usr/bin/env python3
"""Ievieto ģenerētos rasējumus index.src.html un uzraksta index.html."""
import pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.src.html").read_text(encoding="utf-8")

for marker, arg in (("<!--ROOF-->", "roof"), ("<!--ELEV-->", "elev")):
    svg = subprocess.run([sys.executable, str(root / "tools" / "drawings.py"), arg],
                         capture_output=True, text=True, check=True).stdout.strip()
    if marker not in src:
        raise SystemExit(f"trūkst atzīmes {marker}")
    src = src.replace(marker, svg)

(root / "index.html").write_text(src, encoding="utf-8")
print(f"index.html: {len(src)} baiti")
