"""Extract and render the named baseline, reference and paper for round-two review."""
from pathlib import Path
import json
import pymupdf as fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'qa/information-set-round2'
SOURCES = {
    'main': ROOT / 'output/information-set-projection-20261120/个人投资者的信息集_11-20组会放映.pdf',
    'claude': Path('D:/softmove/科研汇报项目/InfoSet-Beamer/信息集论文汇报.pdf'),
    'paper': ROOT / 'On the Information Set of Individual Investors.pdf',
}

def inspect_pdf(name, source, render=True):
    target = QA / name
    target.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(source)
    pages = [{'page': i + 1, 'text': p.get_text()} for i, p in enumerate(doc)]
    (target / 'pages.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
    (target / 'text.txt').write_text('\n\n'.join(f'=== {p["page"]} ===\n{p["text"]}' for p in pages), encoding='utf-8')
    if render:
        for i, p in enumerate(doc):
            p.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False).save(target / f'page-{i+1:02}.png')
        for start in range(0, len(doc), 6):
            sheet = Image.new('RGB', (1500, 1220), '#eeeeee')
            draw = ImageDraw.Draw(sheet)
            for k in range(start, min(start + 6, len(doc))):
                im = Image.open(target / f'page-{k+1:02}.png')
                im.thumbnail((740, 555))
                x, y = (k-start) % 2 * 750, (k-start) // 2 * 405
                im.thumbnail((730, 375))
                sheet.paste(im, (x+5, y+25))
                draw.text((x+6, y+5), f'{name} {k+1}', fill='black')
            sheet.save(target / f'contact-{start//6+1:02}.jpg', quality=90)
    print(name, len(doc), 'pages', source)
    return doc

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        inspect_pdf('final', Path(sys.argv[1]))
    else:
        for name, source in SOURCES.items():
            inspect_pdf(name, source, name != 'paper')
