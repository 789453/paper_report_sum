"""Integrate the supplied revision; remove superseded decks, retain methods.

Run without arguments to inspect the deletion list. --apply performs the update.
The user's half_material input is never modified.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import runpy
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / 'half_material'
PAPER = ROOT / 'paper/information-set-argument-v2'
OUT = ROOT / 'output/information-set-argument-v2'
QA = ROOT / 'qa/information-set-argument-v2'
LEGACY = ROOT / 'reusable/legacy-tools'
HISTORY = ROOT / 'docs/history'
OLD = ['information-set', 'information-set-redesign-20261117']


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inside(p):
    p = p.resolve()
    if not p.is_relative_to(ROOT.resolve()) or p == ROOT.resolve():
        raise ValueError(f'Unsafe target: {p}')
    if p.is_relative_to(INCOMING.resolve()):
        raise ValueError(f'Input must remain untouched: {p}')
    return p


def old_paths():
    return [ROOT / base / name for base in ['paper', 'output', 'qa'] for name in OLD]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.apply and (QA / 'integration-manifest.json').exists():
        raise SystemExit('This import is already complete. Keep the audit manifest; edit the current source instead.')
    candidates = [f for p in old_paths() for f in p.rglob('*') if f.is_file()]
    print(json.dumps({'superseded_files': len(candidates),
                      'bytes': sum(p.stat().st_size for p in candidates),
                      'directories': [str(inside(p).relative_to(ROOT)) for p in old_paths()]}, ensure_ascii=False))
    if not args.apply:
        return
    for p in [PAPER, OUT, QA, LEGACY, HISTORY]:
        p.mkdir(parents=True, exist_ok=True)
    manifest = {'date': '2026-11-17', 'input': 'half_material',
                'imported': [], 'deleted': [], 'retained_methods': [],
                'input_untouched': True}
    # Materialize the latest content while its inherited 45-page dependency exists.
    # This is the sole execution of the inherited content generator.
    if not (PAPER / 'slides.json').exists():
        source = (INCOMING / 'scripts/scripts/argument_v2_content.py').read_text(encoding='utf-8')
        logical_path = str(ROOT / 'scripts/argument_v2_content.py')
        exec(compile(source, logical_path, 'exec'), {'__name__': '__main__', '__file__': logical_path})
    slides = json.loads((PAPER / 'slides.json').read_text(encoding='utf-8'))
    if len(slides) != 46:
        raise ValueError('Expected 46 source slides; stop before deletion.')
    used_assets = {s['asset'] for s in slides if s.get('asset')}
    # Keep only the original-paper figure crops actually used by this revision.
    asset_manifest = json.loads((PAPER / 'assets_manifest.json').read_text(encoding='utf-8'))
    for p in (PAPER / 'assets').glob('*'):
        if p.stem not in used_assets:
            inside(p).unlink()
    (PAPER / 'assets_manifest.json').write_text(json.dumps(
        {k: v for k, v in asset_manifest.items() if k in used_assets}, ensure_ascii=False, indent=2), encoding='utf-8')
    for name in ['evidence.csv', 'source_version.json']:
        src = ROOT / 'paper/information-set' / name
        if src.exists():
            dest = PAPER / ('legacy_' + name)
            shutil.copy2(src, dest)
    # Preserve reusable code, including prior rendering / verification designs.
    # Full old slide prose is content, even when embedded in a .py file.
    active = {'build.py', 'render_deck.py', 'check_and_render.py',
              'collect_community_skills.py', 'fetch_skill_references.py', Path(__file__).name}
    discard_payload = {'redesign_content.py', 'revise_deck.py'}
    for src in list((ROOT / 'scripts').glob('*')):
        if not src.is_file() or src.suffix not in ['.py', '.mjs'] or src.name in active:
            continue
        if src.name in discard_payload:
            # Retain algorithmic helper designs without the old deck body.
            tree = ast.parse(src.read_text(encoding='utf-8'))
            functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
            dest = LEGACY / (src.stem + '_helpers.py.txt')
            dest.write_text('# Historical helper designs; adapt context before reuse.\n' +
                            '\n\n'.join(ast.unparse(n) for n in functions) + '\n', encoding='utf-8')
            manifest['deleted'].append({'path': str(src.relative_to(ROOT)), 'sha256': digest(src),
                                        'reason': 'old narrative embedded in content-generation script'})
            inside(src).unlink()
        else:
            dest = LEGACY / src.name
            shutil.copy2(src, dest)
            inside(src).unlink()
        manifest['retained_methods'].append(str(dest.relative_to(ROOT)))
    # Retain feedback / process records, not full old slide snapshots or copies.
    for src in candidates:
        rel = str(src.relative_to(ROOT)).replace('\\', '/')
        if src.suffix == '.md' and any(t in src.name for t in ['修订', '验收', 'review-record', 'design-rules']):
            dest = HISTORY / rel.replace('/', '__')
            shutil.copy2(src, dest)
            manifest['retained_methods'].append(str(dest.relative_to(ROOT)))
        manifest['deleted'].append({'path': rel, 'sha256': digest(src), 'bytes': src.stat().st_size})
    # Import latest standalone exporters. The source exporter does not overwrite
    # the user's DOCX unless the caller explicitly requests --documents.
    for name in ['build_argument_v2_generated.py', 'build_argument_v2_generated.mjs']:
        src = INCOMING / 'scripts/scripts' / name
        dest = ROOT / 'scripts' / name
        text = src.read_text(encoding='utf-8')
        if name.endswith('.py'):
            text = text.replace("d.save(O/'02_逐页逐字稿_46页对应.docx')",
                                "if '--documents' in __import__('sys').argv:\n    d.save(O/'02_逐页逐字稿_46页对应.docx')")
        else:
            # The original machine-specific runtime is no longer installed.
            start = text.index("const SKILL = ")
            end = text.index("const data = ", start)
            text = text[:start] + ("const SKILL = process.env.CODEX_PRESENTATIONS_SKILL;\n"
                    "const PYTHON = process.env.CODEX_BUNDLED_PYTHON;\n"
                    "// Optional validation uses the runtime paths supplied by this session.\n") + text[end:]
            text = text.replace("import { Presentation, PresentationFile } from '@oai/artifact-tool';",
                "import { createRequire } from 'node:module';\n"
                "const moduleRoot = process.env.RUNTIME_NODE_MODULES;\n"
                "if (!moduleRoot) throw new Error('Set RUNTIME_NODE_MODULES using load_workspace_dependencies.');\n"
                "const require = createRequire(path.join(moduleRoot, '__artifact_loader__.cjs'));\n"
                "const { Presentation, PresentationFile } = require('@oai/artifact-tool');")
        dest.write_text(text, encoding='utf-8')
        manifest['imported'].append({'source': str(src.relative_to(ROOT)), 'source_sha256': digest(src),
                                     'destination': str(dest.relative_to(ROOT)), 'mode': 'adapted tooling'})
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_argument_v2_generated.py')], cwd=ROOT, check=True)
    # User-supplied deliverables take precedence over regenerated files.
    for src in INCOMING.iterdir():
        if not src.is_file():
            continue
        dest = OUT / src.name
        shutil.copy2(src, dest)
        if digest(src) != digest(dest):
            raise ValueError(f'Import hash mismatch: {src}')
        manifest['imported'].append({'source': str(src.relative_to(ROOT)), 'destination': str(dest.relative_to(ROOT)),
                                    'sha256': digest(src), 'mode': 'byte-for-byte copy'})
    # Ensure all required current assets and outputs exist before removing old work.
    for name in used_assets:
        for ext in ['.pdf', '.png']:
            if not (PAPER / 'assets' / (name + ext)).is_file():
                raise ValueError(f'Missing retained asset: {name}{ext}')
    for target in old_paths():
        resolved = inside(target)
        if resolved.exists():
            shutil.rmtree(resolved)
    # Bytecode may contain removed narrative payloads.
    cache = ROOT / 'scripts/__pycache__'
    if cache.exists():
        shutil.rmtree(inside(cache))
    sources = json.loads((PAPER / 'sources.json').read_text(encoding='utf-8'))
    sources['paper']['path'] = 'On the Information Set of Individual Investors.pdf'
    sources['integration'] = 'Imported from half_material on 2026-11-17; current content is not academically approved.'
    (PAPER / 'sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2), encoding='utf-8')
    manifest['current_assets'] = sorted(used_assets)
    manifest['latest_slide_count'] = len(slides)
    manifest['source_seconds'] = sum(s['seconds'] for s in slides)
    manifest['source_speech_hanzi'] = sum(sum('\u4e00' <= c <= '\u9fff' for c in s['speech']) for s in slides)
    (QA / 'integration-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: manifest[k] for k in ['latest_slide_count', 'source_seconds', 'source_speech_hanzi', 'current_assets']}, ensure_ascii=False))
    print('Integrated current input and removed superseded project artifacts.')


if __name__ == '__main__':
    main()
