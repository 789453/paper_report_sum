"""Export individual plots from the local 2026-04-27 paper as standalone PNGs."""
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'On the Information Set of Individual Investors.pdf'
ASSETS = ROOT / 'paper/information-set-argument-v2/projection-20261120-necessary/assets'

# PDF physical page and rectangle in points, measured from the upper left.
PLOTS = {
    'fig1a-plot.png': (52, (129, 148, 485, 386)),
    'fig1b-plot.png': (52, (129, 418, 485, 655)),
    'fig2a-plot.png': (53, (186, 196, 425, 352)),
    'fig2b-plot.png': (53, (186, 373, 425, 530)),
    'fig2c-plot.png': (53, (186, 550, 425, 707)),
    'fig3-mean-plot.png': (54, (77, 205, 305, 496)),
    'fig3-median-plot.png': (54, (314, 205, 538, 496)),
    'fig4-plot.png': (55, (72, 193, 500, 479)),
    'fig5c-plot.png': (56, (138, 375, 386, 540)),
    'fig5d-plot.png': (56, (409, 376, 653, 540)),
}


def main():
    with pymupdf.open(PAPER) as paper:
        for name, (number, bounds) in PLOTS.items():
            page = paper[number - 1]
            rect = pymupdf.Rect(bounds)
            assert page.rect.contains(rect), name
            # Render just the selection, discarding all off-rectangle PDF objects.
            page.get_pixmap(clip=rect, matrix=pymupdf.Matrix(3, 3), annots=False).save(ASSETS / name)


if __name__ == '__main__':
    main()
