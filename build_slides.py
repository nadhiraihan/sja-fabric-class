#!/usr/bin/env python3
"""Render ulang slide materi dari PDF Canva -> slides/NN.webp (2400 px). Jalankan kalau PDF materi berubah.
python3 build_slides.py [path pdf]  (default ~/Downloads/fabric class.pdf). Kalau jumlah slide beda, ganti N di index.html."""
import sys
from pathlib import Path
import fitz
from PIL import Image
pdf = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / "Downloads/fabric class.pdf")
out = Path(__file__).parent / "slides"; out.mkdir(exist_ok=True)
d = fitz.open(pdf)
for i, p in enumerate(d):
    z = 2400 / p.rect.width
    pix = p.get_pixmap(matrix=fitz.Matrix(z, z))
    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(out / f"{i + 1:02d}.webp", "WEBP", quality=82, method=5)
print(d.page_count, "slide ->", out)
