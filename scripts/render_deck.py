"""Render the current PDF; choose other projects explicitly with --paper-id."""
from pathlib import Path
import argparse
import pymupdf
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('revision', nargs='?', default='current')
parser.add_argument('--paper-id', default='information-set-argument-v2')
parser.add_argument('--pdf', type=Path)
args = parser.parse_args()
target = ROOT / 'qa' / args.paper_id / args.revision
if not target.resolve().is_relative_to((ROOT / 'qa').resolve()):
    raise SystemExit('Render target must be within qa.')
source = args.pdf or ROOT / 'output' / args.paper_id / '01_组会报告_46页.pdf'
target.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(source)
for i, page in enumerate(doc):
    page.get_pixmap(matrix=pymupdf.Matrix(1.7, 1.7), alpha=False).save(target / f'slide-{i+1:02}.png')
for first in range(0, len(doc), 12):
    sheet = Image.new('RGB', (1600, 972), '#eeeeee')
    draw = ImageDraw.Draw(sheet)
    for k in range(first, min(first + 12, len(doc))):
        im = Image.open(target / f'slide-{k+1:02}.png')
        im.thumbnail((392, 294))
        x, y = (k-first) % 4 * 400, (k-first) // 4 * 324
        sheet.paste(im, (x + 4, y + 24))
        draw.text((x+6, y+5), str(k+1), fill='black')
    sheet.save(target / f'contact-{first//12+1:02}.jpg', quality=90)
print(f'Rendered {len(doc)} pages from {source} to {target}')
