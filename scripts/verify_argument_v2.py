"""Check migration integrity and document agreement, not academic quality."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
import pymupdf
from docx import Document
from argument_v2_content import load_slides

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/information-set-argument-v2'
QA = ROOT / 'qa/information-set-argument-v2'
data = load_slides()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
normalize = lambda s: re.sub(r'\s+', '', s).replace('−', '-').replace('–', '-')
result = {'import_hashes': {}, 'errors': []}
for source in (ROOT / 'half_material').iterdir():
    if source.is_file():
        target = OUT / source.name
        result['import_hashes'][source.name] = target.exists() and sha(source) == sha(target)
        if not result['import_hashes'][source.name]:
            result['errors'].append(f'Input/output differ: {source.name}')
with pymupdf.open(OUT / '01_组会报告_46页.pdf') as pdf:
    result['pdf_pages'] = len(pdf)
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(OUT / '01_论证重建_46页.pptx') as package:
    result['pptx_slides'] = len([p for p in package.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', p)])
    result['pptx_notes'] = len([p for p in package.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', p)])
    result['speech_note_mismatch'] = []
    result['visible_text_mismatch'] = []
    for i, slide in enumerate(data, 1):
        node = ET.fromstring(package.read(f'ppt/notesSlides/notesSlide{i}.xml'))
        notes = ''.join(n.text or '' for n in node.findall('.//a:t', ns))
        if normalize(slide['speech']) not in normalize(notes):
            result['speech_note_mismatch'].append(i)
        screen_node = ET.fromstring(package.read(f'ppt/slides/slide{i}.xml'))
        screen = normalize(''.join(n.text or '' for n in screen_node.findall('.//a:t', ns)))
        fields = [slide['title']] if slide['kind'] == 'cover' else [
            slide['title'], slide['context'], *slide['lines'],
            *[str(c) for row in (slide.get('table') or []) for c in row]]
        if any(normalize(field) not in screen for field in fields):
            result['visible_text_mismatch'].append(i)
doc = Document(OUT / '02_逐页逐字稿_46页对应.docx')
text = normalize(''.join(p.text for p in doc.paragraphs))
result['speech_docx_mismatch'] = [s['page'] for s in data if normalize(s['speech']) not in text]
result['old_paths_remaining'] = [str(ROOT / base / name) for base in ['paper', 'output', 'qa']
                                 for name in ['information-set', 'information-set-redesign-20261117']
                                 if (ROOT / base / name).exists()]
result['source_seconds'] = sum(s['seconds'] for s in data)
result['status'] = 'integrity checked; academic content requires rewriting'
for name in ['pdf_pages', 'pptx_slides', 'pptx_notes']:
    if result[name] != len(data):
        result['errors'].append(f'{name} != source count')
if any(result[k] for k in ['speech_note_mismatch', 'visible_text_mismatch', 'speech_docx_mismatch', 'old_paths_remaining']):
    result['errors'].append('Source agreement or cleanup check failed')
(QA / 'integration-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
if result['errors']:
    raise SystemExit(1)
