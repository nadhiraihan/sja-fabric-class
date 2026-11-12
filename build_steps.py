#!/usr/bin/env python3
"""Animasi muncul satu-satu di deck web Fabric Class · 12 Nov 2026 (sesuai briefing video Ci Iren).

Briefing (sumber/briefing-video-12nov-transkrip.txt): slide 3 & 30 pertanyaan satu-satu lalu kalimat akhir,
slide 4 alur Benang > Tenunan > Kain > Baju lalu "Pembahasan", slide 15 kotak kanan dikeluarin,
slide 31 & 32 satu-satu dari atas, slide 33 kiri dulu lalu poin kanan satu-satu. Slide lain langsung.
Posisi dari teks PDF materi (koordinat 0..1). Garis + titik timeline dibiarin kelihatan, teksnya yang muncul.
Bikin: slides/NNb.webp (gambar dasar, bagian yang dianimasi dikosongin pakai warna latar) + steps.json.
Jalankan: python3 build_steps.py   (habis build_slides.py kalau PDF berubah)
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

D = Path(__file__).parent
P = 0.006   # padding

STEPS = {
    3: [[(0.062, 0.453, 0.316, 0.483)], [(0.263, 0.525, 0.353, 0.555)], [(0.330, 0.609, 0.462, 0.640)],
        [(0.439, 0.701, 0.533, 0.732)], [(0.478, 0.830, 0.924, 0.898)]],
    4: [[(0.290, 0.226, 0.485, 0.318)], [(0.290, 0.432, 0.495, 0.524)], [(0.290, 0.638, 0.443, 0.732)],
        [(0.290, 0.846, 0.489, 0.940)], [(0.625, 0.528, 0.958, 0.910)]],
    15: [[(0.576, 0.172, 0.950, 0.966)]],
    30: [[(0.062, 0.453, 0.316, 0.483)], [(0.263, 0.525, 0.353, 0.555)], [(0.330, 0.609, 0.462, 0.640)],
         [(0.439, 0.701, 0.533, 0.732)], [(0.475, 0.830, 0.927, 0.898)]],
    31: [[(0.056, 0.315, 0.321, 0.346)], [(0.278, 0.396, 0.668, 0.427)], [(0.118, 0.478, 0.417, 0.509)],
         [(0.331, 0.565, 0.569, 0.596)], [(0.119, 0.654, 0.913, 0.684)], [(0.475, 0.830, 0.927, 0.898)]],
    32: [[(0.056, 0.315, 0.362, 0.346)], [(0.278, 0.396, 0.594, 0.427)], [(0.118, 0.478, 0.524, 0.509)],
         [(0.331, 0.565, 0.651, 0.596)], [(0.278, 0.652, 0.769, 0.683)], [(0.411, 0.689, 0.647, 0.720)],
         [(0.084, 0.794, 0.916, 0.912)]],
    33: [[(0.645, 0.098, 0.905, 0.209)], [(0.645, 0.327, 0.892, 0.510)], [(0.645, 0.556, 0.873, 0.674)],
         [(0.645, 0.787, 0.907, 0.937)]],
}


def pad(r):
    x0, y0, x1, y1 = r
    return (max(0, x0 - P), max(0, y0 - P), min(1, x1 + P), min(1, y1 + P))


def main():
    out = {}
    for n, steps in STEPS.items():
        src = D / "slides" / f"{n:02d}.webp"
        im = Image.open(src).convert("RGB")
        W, H = im.size
        a = np.array(im)
        base = im.copy()
        dr = ImageDraw.Draw(base)
        js = []
        for st in steps:
            rs = []
            for r in st:
                x0, y0, x1, y1 = pad(r)
                X0, Y0, X1, Y1 = int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)
                # warna latar = median pinggiran kotak (di luar teks)
                ring = np.concatenate([a[max(0, Y0 - 3):Y0, X0:X1].reshape(-1, 3), a[Y1:Y1 + 3, X0:X1].reshape(-1, 3)])
                col = tuple(int(v) for v in np.median(ring, axis=0)) if len(ring) else (245, 244, 241)
                dr.rectangle([X0, Y0, X1, Y1], fill=col)
                rs.append([round(x0, 4), round(y0, 4), round(x1 - x0, 4), round(y1 - y0, 4)])
            js.append(rs)
        base.save(D / "slides" / f"{n:02d}b.webp", "WEBP", quality=82, method=5)
        out[n] = js
    (D / "steps.json").write_text(json.dumps(out))
    print({k: len(v) for k, v in out.items()})


if __name__ == "__main__":
    main()
