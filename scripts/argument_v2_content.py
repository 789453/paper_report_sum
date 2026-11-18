"""Validate current source; no dependency on a deleted old deck."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'paper/information-set-argument-v2/slides.json'


def load_slides():
    slides = json.loads(SOURCE.read_text(encoding='utf-8'))
    required = {'page', 'title', 'section', 'context', 'lines', 'speech', 'seconds'}
    for number, slide in enumerate(slides, 1):
        if slide['page'] != number or not required.issubset(slide):
            raise ValueError(f'Invalid slide record at {number}')
    return slides


if __name__ == '__main__':
    data = load_slides()
    print(json.dumps({'slides': len(data), 'seconds': sum(s['seconds'] for s in data)}, ensure_ascii=False))
