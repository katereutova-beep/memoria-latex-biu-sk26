"""Synthetic restoration experiment (no external images).

Builds a procedural 'photograph', degrades it (grain + scratches), applies a classical
baseline (box filter, numpy only) and reports PSNR/SSIM-like metrics. It is an honest
illustration of how quality is *measured*; it is not the AI pipeline itself.
Run: python code/quality_demo.py   -> figures/quality_demo.pdf, quality_curve.pdf, quality.tex
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import model  # reuse palette / rcParams

FIG = model.FIG
rng = np.random.default_rng(2611)


def make_photo(n=160):
    y, x = np.mgrid[0:n, 0:n] / n
    img = 0.55 + 0.25 * np.sin(5 * x + 2 * y) * np.cos(3 * y)           # soft background
    cx, cy = 0.5, 0.45
    face = ((x - cx) ** 2 / 0.05 + (y - cy) ** 2 / 0.08) < 1            # oval 'face'
    img[face] = 0.82
    for ex in (0.42, 0.58):                                             # 'eyes'
        img[((x - ex) ** 2 + (y - 0.40) ** 2) < 0.0012] = 0.25
    img[(abs(y - 0.55) < 0.01) & (abs(x - 0.5) < 0.07)] = 0.3           # 'mouth'
    img[y > 0.78] = 0.35 + 0.1 * np.sin(14 * x)[y > 0.78]               # 'clothes'
    return np.clip(img, 0, 1)


def degrade(img, sigma):
    out = img + rng.normal(0, sigma, img.shape)
    for _ in range(6):                                                  # vertical scratches
        c = rng.integers(5, img.shape[1] - 5)
        out[:, c] = np.clip(out[:, c] + rng.choice([-0.5, 0.5]), 0, 1)
    return np.clip(out, 0, 1)


def box(img, k=3):
    pad = k // 2
    p = np.pad(img, pad, mode="edge")
    out = np.zeros_like(img)
    for i in range(k):
        for j in range(k):
            out += p[i:i + img.shape[0], j:j + img.shape[1]]
    return out / (k * k)


def median_cols(img):
    """Repair scratches: replace each pixel by the median of its horizontal 5-neighbourhood."""
    p = np.pad(img, ((0, 0), (2, 2)), mode="edge")
    stack = np.stack([p[:, i:i + img.shape[1]] for i in range(5)])
    return np.median(stack, axis=0)


def psnr(a, b):
    mse = np.mean((a - b) ** 2)
    return float(10 * np.log10(1.0 / mse))


def ssim_global(a, b):
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    ma, mb = a.mean(), b.mean()
    va, vb = a.var(), b.var()
    cov = ((a - ma) * (b - mb)).mean()
    return float(((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2)))


def main():
    clean = make_photo()
    noisy = degrade(clean, 0.10)
    restored = box(median_cols(noisy), 3)
    fig, ax = plt.subplots(1, 3, figsize=(6.8, 2.5))
    for a, im, title in zip(ax, (clean, noisy, restored),
                            ("Original", f"Degraded  PSNR {psnr(clean, noisy):.1f} dB",
                             f"Restored  PSNR {psnr(clean, restored):.1f} dB")):
        a.imshow(im, cmap="copper", vmin=0, vmax=1); a.set_title(title, fontsize=9); a.axis("off")
    plt.tight_layout(); plt.savefig(FIG / "quality_demo.pdf", bbox_inches="tight"); plt.close()

    sig = np.linspace(0.02, 0.25, 12)
    before, after = [], []
    for s in sig:
        n = degrade(clean, s)
        before.append(psnr(clean, n)); after.append(psnr(clean, box(median_cols(n), 3)))
    plt.figure(figsize=(5.8, 2.9))
    plt.plot(sig, before, color=model.SEPIA, lw=2.2, label="Degraded")
    plt.plot(sig, after, color=model.TEAL, lw=2.6, label="Classical baseline")
    plt.xlabel("Noise level (sigma)"); plt.ylabel("PSNR, dB"); plt.legend(frameon=False)
    plt.tight_layout(); plt.savefig(FIG / "quality_curve.pdf", bbox_inches="tight"); plt.close()

    macros = {
        "PsnrBefore": f"{psnr(clean, noisy):.1f}", "PsnrAfter": f"{psnr(clean, restored):.1f}",
        "SsimBefore": f"{ssim_global(clean, noisy):.2f}", "SsimAfter": f"{ssim_global(clean, restored):.2f}",
    }
    (FIG / "quality.tex").write_text("\n".join(f"\\newcommand{{\\Q{k}}}{{{v}}}" for k, v in macros.items()) + "\n")
    print(macros)


if __name__ == "__main__":
    main()
